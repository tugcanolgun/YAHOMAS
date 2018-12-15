import logging
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse
from django.views import generic
from django import forms

from ..models import Booking, Rooms, GuestBooking, Guests
from ..forms import BookingForm, SearchBookingForm, AddGuest, GuestBookingForm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def booking(request):
    if request.method == 'GET':
        form = BookingForm()
        bookings = Booking.objects.order_by('-created_at')[:10]
        context = {'bookings': bookings, 'form': form}
        return render(request, 'easy/booking/index.html', context)
    if request.method == 'POST':
        form = SearchBookingForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            print(start, end)
            _time = {
                'start_date': start, 
                'end_date': end,
                'single_bed': form.cleaned_data['single_bed'],
                'double_bed': form.cleaned_data['double_bed'],
                'child_bed': form.cleaned_data['child_bed'],
                }
            # Rooms.objects.filter()
            booked = set(values['room_id'] for values in Booking.objects.filter(
                start_date__lte=end, 
                end_date__gte=start,
                ).values('room_id'))
            rooms = Rooms.objects.exclude(id__in=booked).filter(
                Q(single_bed=form.cleaned_data['single_bed']) |
                Q(double_bed=form.cleaned_data['double_bed']) |
                Q(child_bed=form.cleaned_data['child_bed'])
            )
            form = SearchBookingForm(initial=_time)
            return render(request, 'easy/booking/results.html', {'form': form, 'results': rooms, 'time': _time})
        return render(request, 'easy/booking/results.html', {'form': form})

def booking_add(request, room_id, start_date, end_date):
    if request.method == 'GET':
        _room = Rooms.objects.get(id=room_id)
        form = BookingForm(initial={'room': _room, 'start_date': start_date, 'end_date': end_date})
        form.fields['room'].widget = forms.HiddenInput()
        return render(request, 'easy/common/add.html', {'form': form})
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            _booking = form.save(commit=False)
            _booking.save()
            logger.info(f"Booking save successful")
            return HttpResponseRedirect('/booking/user/add/' + str(_booking.id))
        messages.success(request, "Booking could not be added")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def booking_user_add(request, booking_id):
    instance = get_object_or_404(Booking, id=booking_id)
    form = GuestBookingForm(request.POST or None, initial={'booking': instance})
    if form.is_valid():
        _guest = form.save(commit=False)
        _guest.save()
        _booking = Booking.objects.get(id=_guest.booking.id)
        _booking.active = True
        _booking.save()
        logger.info(f"Booking save successful")
        messages.success(request, "Guest is successfuly added to the booking")
    if request.method == 'POST' and not form.is_valid():
        messages.success(request, "Guest could not be added to the booking")
    return render(request, 'easy/common/add.html', {'form': form})

def booking_delete(request, booking_id):
    _booking = Booking.objects.get(id=booking_id)
    if _booking:
        _booking.delete()
        messages.success(request, "Booking is deleted")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    logger.warning("Bookin could not be found. ID: %s" % (booking_id, ))
    return HttpResponse(status=204)

def booking_update(request, booking_id):
    instance = get_object_or_404(Booking, id=booking_id)
    form = BookingForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
    return render(request, 'easy/common/add.html', {'form': form})

