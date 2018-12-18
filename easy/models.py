from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import uuid

class Rooms(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    room_number = models.CharField(max_length=30)
    square_meter = models.FloatField(default=10.0, null=False)
    price = models.FloatField(default=100.0, null=False)
    floor = models.IntegerField(default=1)
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
    image = models.ImageField(upload_to='images/guests/', null=True)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name + ' ' + self.surname

class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    amount_paid = models.FloatField(default=0)
    is_checked_in = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.room.room_number + ' - ' + str(self.start_date) + ' ' + str(self.end_date)

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.booking.room.room_number + ' ' + self.item.name

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'admin'),
        (2, 'manager'),
        (3, 'receptionist'),
        (4, 'roomservicer'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=2)
    image = models.ImageField(upload_to='images/users/', null=True)
