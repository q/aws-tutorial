from django import forms

from lolaws.uploadr.models import StoredImage

class StoredImageUploadForm(forms.ModelForm):
    class Meta:
        model = StoredImage

class EmailImageForm(forms.Form):
    address = forms.EmailField(required=True)
