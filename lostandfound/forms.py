# forms.py
from django import forms
from .models import LostItem, FoundItem

class LostItemForm(forms.ModelForm):
    
    class Meta:
        model = LostItem
        fields = ['name', 'brand', 'color', 'size', 'unique_features', 'date_lost', 'location_lost', 'image']
        error_messages = {
            'name': {'required': 'Please enter the item name'},
            'date_lost': {'required': 'Please enter the date lost'},
            'location_lost': {'required': 'Please enter the location lost'}
             }

class FoundItemForm(forms.ModelForm):
    #lost_item = forms.ModelChoiceField(queryset=LostItem.objects.filter(is_matched=False))

    class Meta:
        model = FoundItem
        fields = ['name', 'brand', 'color', 'size', 'unique_features', 'date_found', 'location_found', 'image']
        error_messages = {
            'name': {'required': 'Please enter the item name'},
            'date_lost': {'required': 'Please enter the date lost'},
            'location_lost': {'required': 'Please enter the location lost'}
             }

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=20)

class SearchLostItemForm(forms.Form):  # Matching form
    name = forms.CharField(max_length=100, required=False, label='Item Name')
    description = forms.CharField(max_length=255, required=False, label='Description')
    location = forms.CharField(max_length=100, required=False, label='Location Lost')
    date_lost = forms.DateField(required=False, widget=forms.SelectDateWidget, label='Date Lost')

class VerificationForm(forms.Form):
    reference_number = forms.CharField(max_length=100, required=True, label='Reference Number')
    purchase_receipt = forms.FileField(required=False, label='Purchase Receipt/Invoice')
    photographs = forms.FileField(required=False, label='Photographs of the Item')
    serial_number_verification = forms.FileField(required=False, label='Serial Number Verification')
    warranty_document = forms.FileField(required=False, label='Warranty/Registration Document')
    other_proof = forms.FileField(required=False, label='Other Proof')
    additional_info = forms.CharField(widget=forms.Textarea, required=False, label='Additional Information')

    def clean_reference_number(self):
        data = self.cleaned_data['reference_number']
        if not data:
            raise forms.ValidationError("This field is required.")
        return data

# lostandfound/forms.py
from django import forms
from django.contrib.auth.models import User

class SignUpForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username',
            'required': 'required'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'required': 'required'
        })
    )
    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'required': 'required'
        })
    )
    confirm_password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password',
            'required': 'required'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

    def save(self):
        cleaned_data = self.cleaned_data
        user = User.objects.create_user(
            username=cleaned_data['username'],
            email=cleaned_data['email'],
            password=cleaned_data['password']
        )
        return user
