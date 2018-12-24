import logging
import os
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse
from django import forms
from django.conf import settings as djangoSettings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.auth.decorators import login_required
from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator
from InvoiceGenerator.pdf import SimpleInvoice

from ..models import Booking, Rooms, GuestBooking, Guests, RoomServiceBooking
from ..forms import BookingForm, SearchBookingForm, AddGuest, GuestBookingForm, CreateInvoiceForm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_rooms(booked: set, single: bool, double: bool, child: bool) -> Rooms:
    """Gets the rooms from the given query"""
    if not double and child:
        return Rooms.objects.exclude(id__in=booked).filter(
            Q(child_bed=child)
        )
    if double and not child:
        return Rooms.objects.exclude(id__in=booked).filter(
            Q(double_bed=double)
        )
    if double and child:
        return Rooms.objects.exclude(id__in=booked).filter(
            Q(double_bed=double) &
            Q(child_bed=child)
        )
    if single and not double and not child:
        return Rooms.objects.exclude(id__in=booked).filter(
            Q(single_bed=single)
        )
    return Rooms.objects.exclude(id__in=booked).filter(
        Q(single_bed=single) &
        Q(double_bed=double) &
        Q(child_bed=child)
    )


def booking(request):
    if request.method == 'GET':
        Booking.objects.filter(active=False).delete()
        form = BookingForm()
        bookings = Booking.objects.order_by('created_at')
        context = {'bookings': bookings, 'form': form}
        return render(request, 'easy/booking/index.html', context)
    if request.method == 'POST':
        Booking.objects.filter(active=False).delete()
        form = SearchBookingForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            single = form.cleaned_data['single_bed']
            double = form.cleaned_data['double_bed']
            child = form.cleaned_data['child_bed']
            _time = {
                'start_date': start,
                'end_date': end,
                'single_bed': single,
                'double_bed': double,
                'child_bed': child,
                }
            # Rooms.objects.filter()
            booked = set(values['room_id'] for values in Booking.objects.filter(
                start_date__lte=end,
                end_date__gte=start,
                ).values('room_id'))
            rooms = get_rooms(booked, single, double, child)
            form = SearchBookingForm(initial=_time)
            return render(request, 'easy/booking/results.html', {'form': form, 'results': rooms, 'time': _time})
        return render(request, 'easy/booking/results.html', {'form': form})


class InvoiceItems:
    def __init__(self, name, number, price):
        self.name = name
        self.number = number
        self.price = price


def booking_detail(request, booking_id):
    if request.method == 'GET':
        booking = Booking.objects.get(id=booking_id)
        guests = GuestBooking.objects.filter(booking=booking).all()
        # search form
        search_form = GuestBookingForm(request.POST or None, initial={'booking': booking})
        search_form.fields['booking'].widget = forms.HiddenInput()
        search_form.helper.form_action = reverse('easy:booking_user_add', kwargs={'booking_id': booking.id})
        # invoice form
        invoice_form = CreateInvoiceForm(request.POST or None)
        invoice_form.helper.form_action = reverse('easy:booking_invoice', kwargs={'booking_id': booking.id})
        # booking update form
        form = BookingForm(request.POST or None, instance=booking)
        form.helper.form_action = reverse('easy:booking_update', kwargs={'booking_id': booking_id})
        items = RoomServiceBooking.objects.filter(booking=booking).all()

        days = abs((booking.start_date - booking.end_date).days)
        if days <= 0:
            days = 1
        _invoice = [InvoiceItems(booking.room.room_number, days, booking.room.price * days)]
        for item in items:
            _invoice.append(InvoiceItems(item.item.name, 1, item.item.price))
        _invoice.append(InvoiceItems('Sum', '-', sum([i.price for i in _invoice])))
        context = {
            'booking': booking,
            'guests': guests,
            'form': form,
            'items': items,
            'search_form': search_form,
            'invoice_form': invoice_form,
            'invoices': _invoice
            }
        return render(request, 'easy/booking/detail.html', context)
    if request.method == 'POST':
        instance = get_object_or_404(Rooms, id=booking_id)
        form = BookingForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            logger.warning("Changes are saved")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        logger.warning("Changes could not be saved")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def xstr(s):
    """Converts None to '' if the object's value is None"""
    if s is None:
        return ''
    return str(s)


def booking_invoice(request, booking_id):
    if request.method == 'POST':
        form = CreateInvoiceForm(request.POST or None)
        if form.is_valid():
            booking = Booking.objects.get(id=booking_id)
            gs = GuestBooking.objects.filter(booking=booking).first()
            items = RoomServiceBooking.objects.filter(booking=booking).all()
            os.environ["INVOICE_LANG"] = "en"
            client = Client(
                xstr(gs.guest.name) + " " + xstr(gs.guest.surname),
                phone=xstr(gs.guest.phone),
                email=xstr(gs.guest.email),
                vat_id=xstr(gs.guest.id_number),
                address=xstr(gs.guest.address),
                zip_code=xstr(gs.guest.zip_code)
            )
            provider = Provider(
                    'Yahomas',
                    bank_account='22946662932',
                    bank_code='210',
                    city="Istanbul",
                    zip_code="34700",
                    phone="+9002122443262",
                    # logo_filename="/home/tugcan/Dropbox/SWE/Yahomas/yahomas_stamp_small.png"
                )
            creator = Creator(
                    'Yahomas',
                    # stamp_filename="/home/tugcan/Dropbox/SWE/Yahomas/YahomasStamp.png"
                )
            invoice = Invoice(client, provider, creator)
            invoice.currency = "$"
            invoice.number = str(booking_id)[:13]
            days = abs((booking.start_date - booking.end_date).days)
            if days <= 0:
                days = 1
            invoice.add_item(Item(days, booking.room.price * (100 - float(form.cleaned_data['discount'])) / 100, description="Room 1"))
            for item in items:
                invoice.add_item(Item(1, item.price, description=item.name))

            pdf = SimpleInvoice(invoice)
            file_path = f"{djangoSettings.STATIC_ROOT}/{str(booking_id)}.pdf"
            pdf.gen(file_path, generate_qr_code=True)

            with open(file_path, 'rb') as file:
                response = HttpResponse(file.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=invoice.pdf'
                return response

def booking_add(request, room_id, start_date, end_date):
    if request.method == 'GET':
        _room = Rooms.objects.get(id=room_id)
        booking = Booking(
            room=_room,
            start_date=start_date,
            end_date=end_date,
        )
        booking.save()
        return redirect(reverse('easy:booking_user_add', kwargs={'booking_id': booking.id}))
        form = BookingForm(initial={'room': _room, 'start_date': start_date, 'end_date': end_date})
        form.fields['room'].widget = forms.HiddenInput()
        form.fields['start_date'].widget = forms.HiddenInput()
        form.fields['end_date'].widget = forms.HiddenInput()
        return render(request, 'easy/common/add.html', {'form': form})
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            _booking = form.save(commit=False)
            _booking.save()
            logger.info(f"Booking save successful")
            return HttpResponseRedirect('/booking/user/add/' + str(_booking.id))
        messages.success(request, "Booking could not be added")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def booking_user_add(request, booking_id):
    instance = get_object_or_404(Booking, id=booking_id)
    search_form = GuestBookingForm(request.POST or None, initial={'booking': instance})
    form = AddGuest(request.POST or None)
    search_form.fields['booking'].widget = forms.HiddenInput()
    guests = GuestBooking.objects.filter(booking=booking_id).all()
    if search_form.is_valid():
        _guest = search_form.save(commit=False)
        if _guest.guest in (gst.guest for gst in guests):
            messages.success(request, "Guest is already added")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        _guest.save()
        _booking = Booking.objects.get(id=_guest.booking.id)
        _booking.active = True
        _booking.save()
        logger.info(f"Booking save successful")
        guests = GuestBooking.objects.filter(booking=booking_id).all()
        messages.success(request, "Guest is successfuly added to the booking")
    if request.method == 'POST' and not search_form.is_valid():
        messages.success(request, "Guest could not be added to the booking")
    return render(request, 'easy/booking/add.html', {
        'form': form,
        'search_form': search_form,
        'guests': guests,
        'booking': instance
        })


def booking_user_delete(request, guest_booking_id):
    instance = GuestBooking.objects.get(id=guest_booking_id)
    if instance:
        instance.delete()
        messages.success(request, "Guest is successfuly deleted from this booking")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def booking_delete(request, booking_id):
    _booking = Booking.objects.get(id=booking_id)
    if _booking:
        _booking.delete()
        messages.success(request, "Booking is deleted")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    logger.warning("Bookin could not be found. ID: %s" % (booking_id, ))
    return HttpResponse(status=204)


def booking_update(request, booking_id):
    instance = get_object_or_404(Booking, id=booking_id)
    form = BookingForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, "Booking is updated")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'easy/common/add.html', {'form': form})
