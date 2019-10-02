from django import forms
from django.core.exceptions import ValidationError

class TagForm(forms.Form):
    man_name = forms.CharField(max_length=20)
    woman_name  = forms.CharField(max_length=20)

    man_name.widget.attrs.update({'class':'form-control'})
    woman_name.widget.attrs.update({'class':'form-control'})
