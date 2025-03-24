from django import forms
from .models import MileageReport


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class MileageReportForm(forms.ModelForm):
    class Meta:
        model = MileageReport
        fields = ['mileage', 'driving_condition']