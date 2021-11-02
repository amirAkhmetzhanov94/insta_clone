from django import forms
from django.contrib.auth.models import User

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
