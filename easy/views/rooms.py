import logging
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views import generic

from ..models import Rooms, RoomType
from ..forms import RoomsForm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def room(request, room_id=None):
    if request.method == 'GET':
        if not room_id:
            form = RoomsForm()
            form.helper.form_action = reverse('easy:room_add_w')
            rooms = Rooms.objects.order_by('-created_at')[:10]
            context = {'rooms': rooms, 'form': form}
            return render(request, 'easy/room/index.html', context)
        else:
            room = Rooms.objects.get(id=room_id)
            context = {'room': room}
            return render(request, 'easy/room/detail.html', context)

def room_add_w(request):
    if request.method == 'POST':
        form = RoomsForm(request.POST)
        if form.is_valid():
            __room = form.save(commit=False)
            __room.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def room_add(request, room_type_id):
    if request.method == 'POST':
        form = RoomsForm(request.POST)
        if form.is_valid():
            __room = form.save(commit=False)
            __room.save()
            logger.info(f"Room save is successful. ")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    room_type_instance = RoomType.objects.get(id=room_type_id)
    form = RoomsForm(
        request.POST or None, 
        initial={
            'room_type': room_type_instance,
        })

    return render(request, 'easy/room/add.html', {'form': form, 'room_type_id': room_type_id})

def room_delete(request, room_id):
    _room = Rooms.objects.get(id=room_id)
    if _room:
        _room.delete()
        messages.success(request, "Room %s is deleted" % _room.room_number)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        logger.warning("Room could not be found. ID: %s" % (room_id, ))
        return HttpResponse(status=204)
