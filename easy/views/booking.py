import logging
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views import generic

from ..models import Booking
from ..forms import BookingForm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def booking(request):
    if request.method == 'GET':
        bookings = Booking.objects.order_by('-created_at')[:10]
        context = {'bookings': bookings}
        return render(request, 'easy/booking/index.html', context)

def booking_add(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = Booking(
                start_date = form.cleaned_data['start_date'],
                end_date = form.cleaned_data['end_date'],
                price = form.cleaned_data['price'],
                amount_paid = form.cleaned_data['amount_paid'],
                is_checked_in = form.cleaned_data['is_checked_in']
            )
            booking.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = BookingForm()

    return render(request, 'easy/booking/add.html', {'form': form })

def booking_delete(request, booking_id):
    _booking = Booking.objects.get(id=booking_id)
    if guest:
        _booking.delete()
        messages.success(request, "Booking is deleted")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        logger.warning("Bookin could not be found. ID: ", booking_id)
        return HttpResponse(status=204)

