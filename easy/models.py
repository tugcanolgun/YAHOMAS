from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


class RoomType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=30)
    bed_count = models.PositiveSmallIntegerField(default=1)
    is_smoke = models.BooleanField(default=False)
    is_balcony = models.BooleanField(default=False)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

class Rooms(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=30)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)

class Guests(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    id_number = models.CharField(max_length=250)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)

class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
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


class Profile(models.Model):
    USER_TYPE_CHOICES = (
        (1, 'admin'),
        (2, 'manager'),
        (3, 'receptionist'),
        (4, 'roomservicer'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=2)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()