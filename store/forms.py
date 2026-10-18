from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class RumisaLoginForm(AuthenticationForm):
    username = forms.CharField(label='نام کاربری', widget=forms.TextInput(attrs={'autocomplete': 'username'}))
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))


class RumisaSignupForm(UserCreationForm):
    first_name = forms.CharField(label='نام', max_length=150, required=True)
    last_name = forms.CharField(label='نام خانوادگی', max_length=150, required=True)
    email = forms.EmailField(label='ایمیل', required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('این ایمیل قبلاً ثبت شده است.')
        return email
