import logging
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views import generic
from dal import autocomplete

from ..models import Guests
from ..forms import AddGuest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GuestAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        query = Guests.objects.all()

        if self.q:
            query = query.filter(name__istartswith=self.q)
        return query

def guest(request):
    if request.method == 'GET':
        form = AddGuest()
        guests = Guests.objects.order_by('-created_at')[:10]
        context = {'guests': guests, 'form': form}
        return render(request, 'easy/guest/index.html', context)
    if request.method == 'POST':
        form = AddGuest(request.POST)
        if form.is_valid():
            __guest = form.save(commit=False)
            __guest.save()
            logger.info(f"Guest save successful")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        logger.warning("Could not add the guest")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def guest_update(request, guest_id=None):
    obj = get_object_or_404(Guests, id=guest_id)
    form = AddGuest(request.POST or None,
                        request.FILES or None, instance=obj)
    form.helper.form_action = reverse('easy:guest_update', kwargs={'guest_id': guest_id})
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Guest is updated")
            return redirect('easy:guest')
    return render(request, 'easy/common/add.html', {'form': form})

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