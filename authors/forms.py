from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'username': 'Username',
            'email': 'E-mail',
            'password': 'Password',
        }
        help_texts = {
            'username': 'Required. 150 characters or less.',
        }
        error_messages = {
            'username': {
                'required': 'This field must not be empty',
                'max_length': "This field must have less than 65 characters",
            },
            'password': {
                'required': 'This field must not be empty',
            },
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your first name here.'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password here.'
            })
        }
