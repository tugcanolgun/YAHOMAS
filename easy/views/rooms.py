import logging
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views import generic

from ..models import Rooms, Booking, RoomCleaning
from ..forms import RoomsForm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def room(request, room_id=None):
    if request.method == 'GET':
        form = RoomsForm()
        form.helper.form_action = reverse('easy:room')
        rooms = Rooms.objects.order_by('-created_at')
        context = {'rooms': rooms, 'form': form}
        return render(request, 'easy/room/index.html', context)
    if request.method == 'POST':
        form = RoomsForm(request.POST, request.FILES)
        if form.is_valid():
            __room = form.save(commit=False)
            __room.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        logger.warning("Could not add the room")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def room_detail(request, room_id):
    if request.method == 'GET':
        room = Rooms.objects.get(id=room_id)
        bookings = Booking.objects.filter(room=room).order_by('-created_at').all()
        form = RoomsForm(request.POST or None, instance=room)
        form.helper.form_action = reverse('easy:room_detail', kwargs={'room_id': room_id})
        cleaning = RoomCleaning.objects.filter(room=room).order_by('-cleaning_time').all()
        context = {'room': room, 'bookings': bookings, 'form': form, 'cleaning': cleaning}
        return render(request, 'easy/room/detail.html', context)
    if request.method == 'POST':
        instance = get_object_or_404(Rooms, id=room_id)
        form = RoomsForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            logger.warning("Changes are saved")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        logger.warning("Changes could not be saved")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def room_delete(request, room_id):
    _room = Rooms.objects.get(id=room_id)
    if _room:
        _room.delete()
        messages.success(request, "Room %s is deleted" % _room.room_number)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        logger.warning("Room could not be found. ID: %s" % (room_id, ))
        return HttpResponse(status=204)
