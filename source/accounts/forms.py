from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from accounts.models import Profile


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        required=True,
        strip=False,
        widget=forms.PasswordInput
    )
    password_confirm = forms.CharField(
        label="Confirm password",
        required=True,
        strip=False,
        widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords are not equal")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ["username", "password", "password_confirm", "email", "last_name"]


class ProfileRegistrationForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ["user", "followers"]

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email"]
        labels = {"first_name": "Name", "last_name": "Surname", "email": "Email"}


class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ["user", "followers"]


class SearchForm(forms.Form):
    q = forms.CharField(max_length=100, required=False, label="Search")


