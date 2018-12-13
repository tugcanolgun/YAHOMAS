from django import forms
from .models import Booking, Guests, Rooms, RoomService
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class AddGuest(forms.ModelForm):
    name = forms.CharField(max_length=40)
    class Meta:
        model = Guests
        fields = ('name', 'surname')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_action = 'add'
        self.helper.add_input(Submit('submit', 'Save Guest'))

class BookingForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))  
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))  

    class Meta:
        model = Booking
        fields = ('room', 'start_date', 'end_date', 'price', 'amount_paid', 'is_checked_in')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_action = 'add'
        self.helper.add_input(Submit('submit', 'Save Booking'))

class SearchBookingForm(forms.Form):
    start_date = forms.DateField(widget=forms.HiddenInput())  
    end_date = forms.DateField(widget=forms.HiddenInput())  

class RoomsForm(forms.ModelForm):
    # number_of_beds = forms.IntegerField( widget=forms.TextInput(attrs={'placeholder': 'Input_A', 'style': 'margin-left: 50px'}))
    class Meta:
        model = Rooms
        fields = ('room_number', 
            'price',
            'square_meter',
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
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
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
        self.helper.form_action = 'add'
        self.helper.add_input(Submit('submit', 'Save Item'))

class UsersForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save User'))
