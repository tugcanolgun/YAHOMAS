import logging
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views import generic

from ..models import Guests
from ..forms import AddGuest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def guest(request):
    if request.method == 'GET':
        guests = Guests.objects.order_by('-created_at')[:10]
        context = {'guests': guests}
        return render(request, 'easy/guest/index.html', context)

def guest_add(request):
    if request.method == 'POST':
        form = AddGuest(request.POST)
        if form.is_valid():
            __guest = form.save(commit=False)
            __guest.save()
            logger.info(f"Guest save successful")
            return redirect(request.META['HTTP_REFERER'])
            # return HttpResponseRedirect('/thanks/')
    else:
        form = AddGuest()
    return render(request, 'easy/guest/add.html', {'form': form})

def guest_delete(request, guest_id):
    """ Delete the guest if exists
    Args:
        guest_id (str): Guest<uuid>
    Returns:
        success
            ? Redirects to the previous page
            : returns 204
    """
    _guest = Guests.objects.get(id=guest_id)
    if _guest:
        _guest.delete()
        logger.info(f"Guest delete successful. ID: {guest_id}")
        messages.success(request, "Your data has been saved!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    logger.warning(f"Guest could not be found. ID: {guest_id} ")
    return HttpResponse(status=204)