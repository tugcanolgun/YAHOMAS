import logging
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views import generic

from ..models import Booking, Rooms
from ..forms import BookingForm, SearchBookingForm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def booking(request):
    if request.method == 'GET':
        form = BookingForm()
        bookings = Booking.objects.order_by('-created_at')[:10]
        context = {'bookings': bookings, 'form': form}
        return render(request, 'easy/booking/index.html', context)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            __booking = form.save(commit=False)
            __booking.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        logger.warning("Could not add the booking")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def booking_delete(request, booking_id):
    _booking = Booking.objects.get(id=booking_id)
    if _booking:
        _booking.delete()
        messages.success(request, "Booking is deleted")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        logger.warning("Bookin could not be found. ID: %s" % (booking_id, ))
        return HttpResponse(status=204)

def booking_search(request):
    form = SearchBookingForm(request.POST)
    if form.is_valid():
        start = form.cleaned_data['start_date']
        end = form.cleaned_data['end_date']
        # Rooms.objects.filter()
        booked = set(values['room_id'] for values in Booking.objects.filter(start_date__lte=end, end_date__gte=start).values('room_id'))
        rooms = Rooms.objects.exclude(id__in=booked)
        form = SearchBookingForm(initial={'start_date': start, 'end_date': end})
        return render(request, 'easy/booking/results.html', {'form': form, 'results': rooms})
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'easy/booking/results.html', {'form': form})
