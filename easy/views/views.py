import logging
import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse
from django.views import generic
from django import forms
from easy.models import Rooms, Booking

# from ..models import RoomType, Guests, Booking, Rooms, RoomType
from ..forms import SearchBookingForm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Stats:
    """Holds information for statistics to relay in the intex page"""
    def __init__(self, title: str, number: int, sub: str="In total", font: str="fas fa-hotel"):
        """Constructor"""
        self.title = title
        self.number = number
        self.sub = sub
        self.font = font


def _stats(rooms: Rooms, bookings: Booking) -> list:
    """Creates statistics from the objects"""
    stats: list = []
    booked_rooms = [booking.room for booking in bookings]
    avail_rooms = [room for room in rooms if room not in booked_rooms]
    stats.append(Stats(
        "Available rooms",
        len(avail_rooms),
    ))
    stats.append(Stats(
        "Occupied rooms",
        len(bookings),
    ))
    stats.append(Stats(
        "Availabe of single bed rooms",
        len([room for room in avail_rooms if room.single_bed]),
        font="fas fa-bed"
    ))
    stats.append(Stats(
        "Availabe of double bed rooms",
        len([room for room in avail_rooms if room.double_bed]),
        font="fas fa-bed"
    ))
    stats.append(Stats(
        "Availabe of child bed rooms",
        len([room for room in avail_rooms if room.child_bed]),
        font="fas fa-bed"
    ))
    stats.append(Stats(
        "Number of rooms",
        len(rooms),
    ))
    stats.append(Stats(
        "Number of single bed rooms",
        len([room for room in rooms if room.single_bed]),
        font="fas fa-bed"
    ))
    stats.append(Stats(
        "Number of double bed rooms",
        len([room for room in rooms if room.double_bed]),
        font="fas fa-bed"
    ))
    # stats.append(Stats(
    #     "Number of child bed rooms",
    #     len([room for room in rooms if room.child_bed]),
    #     font="fas fa-bed"
    # ))
    return stats


def login_user(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('easy:index'))
        else:
            messages.success(request, "Logged in")
    messages.success(request, "Could not log in")
    return render(request, 'easy/common/add.html', {'form': form})


def index(request):
    # latest_question_list = RoomType.objects.order_by('-pub_date')[:5]
    # context = {'latest_question_list': latest_question_list}
    if request.method == 'POST':
        form = SearchBookingForm(request.POST)
        form.fields['start_date'].widget = forms.HiddenInput()
        form.fields['end_date'].widget = forms.HiddenInput()
        if form.is_valid():
            return redirect(request.META['HTTP_REFERER'])
    else:
        form: forms.Form = SearchBookingForm()
        today: datetime = datetime.date.today()
        tomorrow: datetime = today + datetime.timedelta(days=1)
        bookings = Booking.objects.filter(
            start_date__gte=today,
            end_date__gte=tomorrow,
        ).all()
        rooms = Rooms.objects.all()
        stats = _stats(rooms, bookings)
        context = {
            'form': form,
            'bookings': bookings,
            'rooms': rooms,
            'stats': stats
            }

    return render(request, 'easy/index.html', context)


def about(request):
    return render(request, 'easy/common/about.html')
