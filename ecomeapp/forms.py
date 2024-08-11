from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta :
        model = Contact
        fields  = ["name", "email", "desc", "phone_number"]
        widgets ={
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'desc': forms.Textarea(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }