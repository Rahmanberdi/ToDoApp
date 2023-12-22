from django import forms


class CreateForm(forms.Form):
    title = forms.CharField(max_length=200)
    date = forms.DateTimeField()