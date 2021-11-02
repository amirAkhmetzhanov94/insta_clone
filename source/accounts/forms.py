from django import forms
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    avatar = forms.ImageField()

    about = forms.CharField(required=False, max_length=30)

    phone_number = forms.CharField(required=False)

    gender_user = forms.ChoiceField(required=False)

    last_name = forms.CharField(required=False)

    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        fields = ["username", "email", "avatar", "password1", "password2",
                  "last_name", "about", "phone_number", "gender_user"]
