from django import forms
from .models import Booking, Guests, RoomType, Rooms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class AddGuest(forms.ModelForm):
    name = forms.CharField(max_length=40)
    class Meta:
        model = Guests
        fields = ('name', 'surname')

class BookingForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.TextInput(attrs={'id':'datepicker'}))

    class Meta:
        model = Booking
        fields = ('start_date', 'end_date', 'price', 'amount_paid', 'is_checked_in')

class RoomTypeForm(forms.ModelForm):
    class Meta:
        model = RoomType
        fields = ('name', 'bed_count', 'is_smoke')

class RoomsForm(forms.ModelForm):
    # number_of_beds = forms.IntegerField( widget=forms.TextInput(attrs={'placeholder': 'Input_A', 'style': 'margin-left: 50px'}))
    number_of_beds = forms.IntegerField(required=False)
    class Meta:
        model = Rooms
        fields = ('room_type', 'room_number', 'number_of_beds', 'is_smoke', 'is_balcony')

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)