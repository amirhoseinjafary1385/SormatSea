from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from .models import NFT, Category
from django.contrib.auth.models import User
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    MinLengthValidator,
    MaxLengthValidator,
)
from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form



class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            css_classes = widget.attrs.get('class', '').split()

            if isinstance(widget, forms.CheckboxInput):
                css_classes.append('form-check-input')
            elif isinstance(widget, forms.FileInput):
                css_classes.append('form-control')
            else:
                default_class = 'form-control'
                css_classes.append(default_class)
                
            widget.attrs['class'] = ' '.join(css_classes).strip()

class RegisterForm(BootstrapFormMixin, UserCreationForm):
    username = forms.CharField(
        max_length=150, 
        label="Username",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'})
    )
    first_name = forms.CharField(
        max_length=50, 
        label="First Name",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'})
    )
    last_name = forms.CharField(
        max_length=50, 
        label="Last Name",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'})
    )
    email = forms.EmailField(
        label="Email", 
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
        label="Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),
        label="Confirm Password"
    )

    class Meta:
        model = User
        # Removed country, city and user_id fields per request
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]

class LoginForm(BootstrapFormMixin, AuthenticationForm):
    username = forms.CharField(label="Username or Email")
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    class Meta:
        fields = ['username', 'password', 'remember_me']

class NFTForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = NFT
        # Use the actual field names from your NFT model
        fields = ['name', 'description', 'image', 'price_irt', 'price_polygon']
        
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'NFT Name'}),  # Changed from title to name
            'description': forms.Textarea(attrs={'placeholder': 'NFT Description', 'rows': 3}),
            'image': forms.FileInput(attrs={'placeholder': 'Upload NFT Image'}),
            'price_irt': forms.NumberInput(attrs={'placeholder': 'Price in IRT', 'step': '0.01'}),
            'price_polygon': forms.NumberInput(attrs={'placeholder': 'Price in Polygon (MATIC)', 'step': '0.01'}),
        }

        labels = {
            'name': "NFT Name",  # Changed from title to name
            'description': "Description",
            'image': "NFT Image",
            'price_irt': "Price (IRT)",
            'price_polygon': "Price (MATIC)"
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {


            
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Category Description', 'rows': 3}),
        }