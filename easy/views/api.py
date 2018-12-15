from rest_framework import viewsets
from easy.models import User, Rooms, Booking, RoomService, RoomServiceBooking
from easy.serializers import *
from django.http import Http404
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import datetime

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def room_list(request):
    if request.method == 'GET':
        today = datetime.date.today()
        response = Booking.objects.filter(
            start_date__lte=today,
            end_date__gte=today,
        ).all()
        # rooms = Rooms.objects.all()
        serializer = BookingSerializer(response, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def items_list(request):
    if request.method == 'GET':
        response = RoomService.objects.all()
        serializer = ItemsSerializer(response, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def items(request, booking_id):
    try:
        _booking = Booking.objects.get(pk=booking_id)
    except Booking.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        response = RoomServiceBooking.objects.filter(booking=booking_id).all()
        serializer = RoomServiceBookingSerializer(response, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = RoomServiceBookingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        data = JSONParser().parse(request)
        try:
            _item = RoomServiceBooking.objects.get(id=data['id'])
        except Booking.DoesNotExist:
            return HttpResponse(status=404)
        serializer = RoomServiceBookingSerializer(_item, data=data)
        if serializer.is_valid():
            _item.delete()
            return HttpResponse(status=204)
        return JsonResponse(serializer.errors, status=400)
