from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label= 'Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']