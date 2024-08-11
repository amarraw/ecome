from django import forms
from .models import ChangePass
from django.contrib.auth.forms import UserCreationForm

class ChangePass(forms.Form):
    class meta:
        fields = ["oldpass","newpass","compass"]


