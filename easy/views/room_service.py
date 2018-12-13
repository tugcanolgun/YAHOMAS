import logging
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views import generic

from ..models import RoomService
from ..forms import RoomServiceForm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def room_service(request, room_id=None):
    if request.method == 'GET':
        form = RoomServiceForm()
        # form.helper.form_action = reverse('easy:room_add')
        items = RoomService.objects.order_by('-created_at')[:10]
        context = {'items': items, 'form': form}
        return render(request, 'easy/room_service/index.html', context)

def room_service_add(request):
    if request.method == 'POST':
        form = RoomServiceForm(request.POST, request.FILES)
        if form.is_valid():
            # print(request.FILES['photo'])
            __room_service = form.save(commit=False)
            __room_service.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        messages.success(request, "Could not save the item")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def room_service_delete(request, room_service_id):
    _room_service = RoomService.objects.get(id=room_service_id)
    if _room_service:
        _room_service.delete()
        messages.success(request, "Item %s is deleted" % _room_service.name)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        logger.warning("Item could not be found. ID: %s" % (room_service_id, ))
        return HttpResponse(status=204)