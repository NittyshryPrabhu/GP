from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class RegisterForm(UserCreationForm):

    email = forms.EmailField(required=True)
    mobile = forms.CharField(max_length=10, required=True)
    dob = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    subscription = forms.ChoiceField(
        choices=UserProfile.SUBSCRIPTION_CHOICES,
        required=True
    )

    # 🔥 Simple password error only
    error_messages = {
        'password_mismatch': 'Password wrong',
    }

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'mobile',
            'dob',
            'subscription',
            'password1',
            'password2',
        )
