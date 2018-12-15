import logging
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views import generic

from ..models import User
from ..forms import UsersForm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def users(request, room_id=None):
    if request.method == 'GET':
        form = UsersForm()
        # profile_form = ProfileForm(request.POST or None)
        # form.helper.form_action = reverse('easy:room_add')
        users = User.objects.order_by('-date_joined')[:10]
        context = {
            'users': users, 
            'form': form, 
            # 'profile_form': profile_form
            }
        return render(request, 'easy/users/index.html', context)
    if request.method == 'POST':
        form = UsersForm(request.POST or None)
        if form.is_valid():
            __user = form.save(commit=False)
            __user.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        if form.cleaned_data.get('password1') != form.cleaned_data.get('password2'):
            messages.success(request, "Passwords do not match")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        if len(form.cleaned_data.get('password1')) < 8:
            messages.success(request, "Passwords must be at least 8 characters")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        messages.success(request, "Could not save the user")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def user_delete(request, user_id):
    _user = User.objects.get(id=user_id)
    if _user:
        _user.delete()
        messages.success(request, "User %s is deleted" % _user.username)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        logger.warning("User could not be found. ID: %s" % (user_id, ))
        return HttpResponse(status=204)
