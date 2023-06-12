from django import forms

class ImageForm(forms.Form):
    data = forms.CharField(widget=forms.Textarea)
