from django import forms


class FilterForm(forms.Form):
    gender = forms.Select()
