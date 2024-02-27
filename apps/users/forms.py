from django import forms
from django.core.exceptions import ValidationError

from apps.users.models import User


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(max_length=28, widget=forms.TextInput(
        attrs={"id": "password", "type": "password"}))
    password2 = forms.CharField(max_length=28, widget=forms.TextInput(
        attrs={"id": "password", "type": "password"}))

    avatar = forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    def save(self, commit=True):
        user = super().save(commit)
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 == p2:
            user.set_password(p1)
            user.save()
        else:
            raise ValidationError("Passwords do not match!")

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2", "avatar"]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=28)
    password = forms.CharField(max_length=28)
