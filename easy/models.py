from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

class Rooms(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    room_number = models.CharField(max_length=30)
    square_meter = models.FloatField(default=10.0, null=False)
    price = models.FloatField(default=100.0, null=False)
    single_bed = models.BooleanField(default=False)
    double_bed = models.BooleanField(default=False)
    child_bed = models.BooleanField(default=False)
    has_view = models.BooleanField(default=False)
    smokable = models.BooleanField(default=False)
    has_balcony = models.BooleanField(default=False)
    has_air_cond = models.BooleanField(default=False)
    has_tv = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/rooms/', null=True)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.room_number

class Guests(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    id_number = models.CharField(max_length=250)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)

class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.FloatField()
    amount_paid = models.FloatField(default=0)
    is_checked_in = models.BooleanField(default=False)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)

class GuestBooking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    guest = models.ForeignKey(Guests, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)

class RoomService(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=30, null=False)
    price = models.FloatField(default=10.0, null=False)
    image = models.ImageField(upload_to='images/items/', null=True)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

class RoomServiceBooking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    item = models.ForeignKey(RoomService, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)

