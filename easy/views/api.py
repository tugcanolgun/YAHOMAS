from rest_framework import viewsets
from easy.models import User, Rooms, Booking, RoomService, RoomServiceBooking, RoomCleaning
from easy.serializers import *
from django.http import Http404
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import datetime
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_401_UNAUTHORIZED,
    HTTP_200_OK
)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def cleaning(request, room_id=None):
    if request.method == 'GET':
        response = RoomCleaning.objects.all()
        serializer = RoomCleaningSerializer(response, many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = RoomCleaningSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def booking_list(request):
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
def room_list(request):
    if request.method == 'GET':
        response = Rooms.objects.all()
        serializer = RoomsSerializer(response, many=True)
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

@csrf_exempt
def item_delete(request, item_id):
    if request.method == 'DELETE':
        try:
            _item = RoomServiceBooking.objects.get(id=item_id)
        except Booking.DoesNotExist:
            return HttpResponse(status=404)
        else:
            _item.delete()
            return HttpResponse(status=204)
        # serializer = RoomServiceBookingSerializer(_item, data=data)
        # if serializer.is_valid():
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_401_UNAUTHORIZED)
    # token, _ = Token.objects.get_or_create(user=user)
    return Response({'user': user.id},
status=HTTP_200_OK)
