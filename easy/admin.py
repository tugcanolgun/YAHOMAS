from django.contrib import admin
from .models import Booking, Guests, Rooms

admin.site.register(Booking)
admin.site.register(Guests)
admin.site.register(Rooms)
