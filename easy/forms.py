from django import forms
from .models import Booking, Guests
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class AddGuest(forms.ModelForm):
    name = forms.CharField(max_length=40)
    class Meta:
        model = Guests
        fields = ('name', 'surname')

class PostForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.TextInput(attrs={'id':'datepicker'}))

    class Meta:
        model = Booking
        fields = ('start_date', 'end_date', 'price', 'amount_paid', 'is_checked_in')

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