import logging
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views import generic

from .models import RoomType, Guests, Booking, Rooms, RoomType
from .forms import BookingForm, AddGuest, NameForm, RoomsForm, RoomTypeForm

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
        form = BookingForm()

    return render(request, 'easy/index.html', {'form': form })

### BOOKING

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


### ROOM TYPES

def room_type(request):
    if request.method == 'GET':
        room_types = RoomType.objects.order_by('-created_at')[:10]
        context = {'room_types': room_types}
        return render(request, 'easy/room_type/index.html', context)

def room_type_add(request):
    if request.method == 'POST':
        form = RoomTypeForm(request.POST)
        if form.is_valid():
            room_type = RoomType(
                name = form.cleaned_data['name'],
                bed_count = form.cleaned_data['bed_count'],
                is_smoke = form.cleaned_data['is_smoke'],
            )
            room_type.save()
            logger.info(f"Room type save is successful. Name: {form.cleaned_data['name']}")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = RoomTypeForm()

    return render(request, 'easy/room_type/add.html', {'form': form })

def room_type_delete(request, room_type_id):
    _room_type = RoomType.objects.get(id=room_type_id)
    if guest:
        _room_type.delete()
        messages.success(request, "Room type is deleted")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        logger.warning("Room type could not be found. ID: ", room_type_id)
        return HttpResponse(status=204)

### ROOMS

# def room(request):
#     if request.method == 'GET':
#         rooms = Rooms.objects.order_by('-created_at')[:10]
#         context = {'rooms': rooms}
#         return render(request, 'easy/room/index.html', context)

def room(request, room_id=None):
    if request.method == 'GET':
        if not room_id:
            rooms = Rooms.objects.order_by('-created_at')[:10]
            context = {'rooms': rooms}
            return render(request, 'easy/room/index.html', context)
        else:
            room = Rooms.objects.get(id=room_id)
            context = {'room': room}
            return render(request, 'easy/room/detail.html', context)

def room_add(request, room_type_id):
    if request.method == 'POST':
        form = RoomsForm(request.POST)
        if form.is_valid():
            room = Rooms(
                room_type = form.cleaned_data['room_type'],
                room_number = form.cleaned_data['room_number'],
                number_of_beds = form.cleaned_data['number_of_beds'],
                is_smoke = form.cleaned_data['is_smoke'],
                is_balcony = form.cleaned_data['is_balcony'],
            )
            room.save()
            logger.info(f"Room save is successful. ")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:

        room_type_instance = RoomType.objects.get(id=room_type_id)
        print(room_type_instance)
        form = RoomsForm(
            request.POST or None, 
            initial={ 
                'room_type': room_type_instance,
                # 'number_of_beds': room_type_instance.bed_count,
                # 'is_smoke': room_type_instance.is_smoke
            })

    return render(request, 'easy/room/add.html', {'form': form, 'room_type_id': room_type_id })

def room_delete(request, room_id):
    _room = Rooms.objects.get(id=room_id)
    if guest:
        _room.delete()
        messages.success(request, "Room is deleted")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        logger.warning("Room could not be found. ID: ", room_id)
        return HttpResponse(status=204)



### GUEST 

def guest_search(request):
    logger.info(f"Request arrived for search =====================================================")
    guest_name = request.GET.get('guest_name', None)
    data = {
        'is_taken': Guests.objects.filter(name__startswith=guest_name).exists()
    }
    return JsonResponse(data)
    if request.is_ajax():
        logger.info(f"Request arrived for the ajax search")
        q = request.GET.get('term', '').capitalize()
        search_qs = Guests.objects.filter(name__startswith=q)
        results = []
        for r in search_qs:
            results.append(r.FIELD)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def guest(request):
    if request.method == 'GET':
        guests = Guests.objects.order_by('-created_at')[:10]
        context = {'guests': guests}
        return render(request, 'easy/guest/index.html', context)

def guest_add(request):
    if request.method == 'POST':
        form = AddGuest(request.POST)
        if form.is_valid():
            guest = Guests(
                name = form.cleaned_data['name'],
                surname = form.cleaned_data['surname']
            )
            guest.save()
            logger.info(f"Guest save successful")
            return redirect(request.META['HTTP_REFERER'])
            # return HttpResponseRedirect('/thanks/')
    else:
        form = AddGuest()
    return render(request, 'easy/guest/add.html', {'form': form})

def guest_delete(request, guest_id):
    _guest = Guests.objects.get(id=guest_id)
    if guest:
        _guest.delete()
        logger.info(f"Guest delete successful. ID: {guest_id}")
        messages.success(request, "Your data has been saved!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        logger.warning("Guest could not be found. ID: ", guest_id)
        return HttpResponse(status=204)