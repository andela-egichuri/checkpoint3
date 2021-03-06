from django import forms
from django.contrib.auth.models import User
from django.core import validators


class LoginForm(forms.Form):
    """Fields for the login form"""
    username = forms.CharField(
        max_length=100, widget=forms.TextInput(
            attrs={'class': 'validate', 'autocomplete': 'off', 'required': True}
        ))
    password = forms.CharField(
        max_length=32, widget=forms.PasswordInput(
            attrs={'class': 'validate', 'required': True}
        ))
    src = forms.CharField(
        max_length=100, widget=forms.HiddenInput(
            attrs={'value': 'login'}
        ))


class RegistrationForm(forms.ModelForm):
    """Fields for the registration form"""
    error_messages = {
        'password_mismatch': "The two password fields don't match.",
    }
    conf_password = forms.CharField(
        max_length=32, widget=forms.PasswordInput(
            attrs={'class': 'validate', 'required': True}))
    password = forms.CharField(
        max_length=32, widget=forms.PasswordInput(
            attrs={'class': 'validate', 'required': True}))
    src = forms.CharField(
        max_length=100, widget=forms.HiddenInput(
            attrs={'value': 'reg'}
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_conf_password(self):
        """Validate password"""
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("conf_password")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def clean_email(self):
        """Ensure uniqueness of the user email"""
        email = self.cleaned_data.get('email').lower()
        username = self.cleaned_data.get('username')
        if email == '':
            raise forms.ValidationError(u'Email address required.')

        if email and User.objects.filter(email=email).count():
            raise forms.ValidationError(u'Email address taken.')
        return email

    def clean_username(self):
        """Convert username to uppercase to enforce uniqueness"""
        username = self.cleaned_data.get('username')
        return username.lower()
