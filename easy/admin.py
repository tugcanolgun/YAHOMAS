from django.contrib import admin
from .models import Booking, Guests, Profile, Rooms, RoomType

admin.site.register(Booking)
admin.site.register(Guests)
admin.site.register(Profile)
admin.site.register(Rooms)
admin.site.register(RoomType)
