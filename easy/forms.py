from django import forms
from .models import Booking, Guests, Rooms, RoomService, GuestBooking, User
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.conf import settings

class AddGuest(forms.ModelForm):
    name = forms.CharField(max_length=40)
    image = forms.ImageField(required=False)
    class Meta:
        model = Guests
        fields = ('name', 'surname', 'id_number', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Guest'))

class GuestBookingForm(forms.ModelForm):
    class Meta:
        model = GuestBooking
        fields = ('guest', 'booking')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Guest'))

class BookingForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))  
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))  

    class Meta:
        model = Booking
        fields = ('room', 'start_date', 'end_date', 'amount_paid', 'is_checked_in')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Booking'))

class SearchBookingForm(forms.Form):
    start_date = forms.DateField(widget=forms.HiddenInput())  
    end_date = forms.DateField(widget=forms.HiddenInput())  
    single_bed = forms.BooleanField(required=False)
    double_bed = forms.BooleanField(initial=True, required=False)
    child_bed = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Search'))

class RoomsForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    has_view = forms.BooleanField(required=False, initial=False)
    smokable = forms.BooleanField(required=False, initial=False)
    has_balcony = forms.BooleanField(required=False, initial=True)
    has_air_cond = forms.BooleanField(required=False, initial=True)
    has_tv = forms.BooleanField(required=False, initial=True)
    class Meta:
        model = Rooms
        fields = ('room_number', 
            'price',
            'square_meter',
            'floor',
            'image',
            'single_bed',
            'double_bed',
            'child_bed',
            'has_view',
            'smokable',
            'has_balcony',
            'has_air_cond',
            'has_tv',
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Room'))

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Sign up'))

class RoomServiceForm(forms.ModelForm):
    class Meta:
        model = RoomService
        fields = ('name', 'price', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Item'))

class UsersForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'user_type')
