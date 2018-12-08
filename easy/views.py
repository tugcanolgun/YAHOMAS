import logging
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views import generic

from .models import RoomType, Guests, Booking
from .forms import PostForm, AddGuest, NameForm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def index(request):
    latest_question_list = RoomType.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            return redirect(request.META['HTTP_REFERER'])
    else:
        form = PostForm()

    return render(request, 'easy/index.html', {'form': form })

### BOOKING

def booking(request):
    if request.method == 'GET':
        bookings = Booking.objects.order_by('-created_at')[:10]
        context = {'bookings': bookings}
        return render(request, 'easy/booking/index.html', context)

def booking_add(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            price = form.cleaned_data['price']
            amount_paid = form.cleaned_data['amount_paid']
            is_checked_in = form.cleaned_data['is_checked_in']
            booking = Booking(
                start_date = start_date,
                end_date = end_date,
                price = price,
                amount_paid = amount_paid,
                is_checked_in = is_checked_in
            )
            booking.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = PostForm()

    return render(request, 'easy/booking/add.html', {'form': form })

def booking_delete(request, booking_id):
    _booking = Booking.objects.get(id=booking_id)
    if guest:
        _booking.delete()
        messages.success(request, "Booking is deleted")
        # return HttpResponseRedirect(request.path)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        # return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        logger.warning("Bookin could not be found. ID: ", booking_id)
        return HttpResponse(status=204)


### GUEST 

def guest(request):
    if request.method == 'GET':
        guests = Guests.objects.order_by('-created_at')[:10]
        context = {'guests': guests}
        return render(request, 'easy/guest/index.html', context)

def guest_add(request):
    if request.method == 'POST':
        form = AddGuest(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            guest = Guests(
                name = name,
                surname = surname
            )
            guest.save()
            return redirect(request.META['HTTP_REFERER'])
            # return HttpResponseRedirect('/thanks/')
    else:
        form = AddGuest()
    return render(request, 'easy/guest/add.html', {'form': form})

def guest_delete(request, guest_id):
    logger.info(f"Guest delete request. ID: {guest_id}")
    _guest = Guests.objects.get(id=guest_id)
    if guest:
        logger.info(f"Guest is found. Deleting... {guest_id}")
        _guest.delete()
        logger.info(f"Guest deletion is complete. Redirecting...")

        messages.success(request, "Your data has been saved!")
        # return HttpResponseRedirect(request.path)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        # return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        logger.warning("Guest could not be found. ID: ", guest_id)
        return HttpResponse(status=204)