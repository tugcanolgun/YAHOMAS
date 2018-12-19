from rest_framework import serializers
from easy.models import User, Rooms, Booking, RoomService, RoomServiceBooking, RoomCleaning


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'groups')

class RoomCleaningSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomCleaning
        fields = '__all__'

class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    room = RoomsSerializer(read_only=True)
    class Meta:
        model = Booking
        fields = '__all__'

class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomService
        fields = ('id', 'name', 'price', 'image')

class RoomServiceBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomServiceBooking
        fields = '__all__'
