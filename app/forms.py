from django import forms

class LoginForm(forms.Form):
    dockerRegistyUrl = forms.CharField(label='dockerRegistyUrl', max_length=100)
    dockerRegistyUsername  = forms.CharField(label='dockerRegistyUsername', max_length=100)
    dockerRegistyPassword  = forms.CharField(label='dockerRegistyPassword', max_length=100)