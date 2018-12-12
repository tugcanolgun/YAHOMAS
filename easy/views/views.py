import logging
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views import generic

# from ..models import RoomType, Guests, Booking, Rooms, RoomType
from ..forms import SearchBookingForm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def index(request):
    # latest_question_list = RoomType.objects.order_by('-pub_date')[:5]
    # context = {'latest_question_list': latest_question_list}
    if request.method == 'POST':
        form = SearchBookingForm(request.POST)
        if form.is_valid():
            return redirect(request.META['HTTP_REFERER'])
    else:
        form = SearchBookingForm()

    return render(request, 'easy/index.html', {'form': form })
