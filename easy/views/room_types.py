import logging
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views import generic

from ..models import RoomType
from ..forms import RoomTypeForm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def room_type(request):
    if request.method == 'GET':
        room_types = RoomType.objects.order_by('-created_at')[:10]
        context = {'room_types': room_types}
        return render(request, 'easy/room_type/index.html', context)

def room_type_add(request):
    if request.method == 'POST':
        form = RoomTypeForm(request.POST)
        if form.is_valid():
            __room_type = form.save(commit=False)
            __room_type.save()
            logger.info(f"Room type save is successful. Name: {form.cleaned_data['name']}")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = RoomTypeForm()

    return render(request, 'easy/room_type/add.html', {'form': form})

def room_type_delete(request, room_type_id):
    _room_type = RoomType.objects.get(id=room_type_id)
    if guest:
        _room_type.delete()
        messages.success(request, "Room type is deleted")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    logger.warning("Room type could not be found. ID: %s" % room_type_id)
    return HttpResponse(status=204)
