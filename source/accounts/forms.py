from django import forms
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    avatar = forms.ImageField()

    about = forms.CharField()

    phone_number = forms.CharField()

    gender_user = forms.ChoiceField()

    last_name = forms.CharField()

    class Meta(UserCreationForm.Meta):
        fields = ["username", "email", "avatar", "password1", "password2", "last_name", "about", "phone_number", "gender_user"]
