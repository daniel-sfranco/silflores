from django import forms
from . import models

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class PhotoForm(forms.Form):
    images = MultipleFileField(label="Fotos")

class ProductForm(forms.ModelForm):
    tags = forms.CharField(required=False, widget=forms.Textarea)
    class Meta:
        model = models.Product
        fields = ['name', 'price', 'desc', 'size_type', 'size', 'term', 'tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].widget = forms.Textarea()
        self.fields['tags'].help_text = "Insira as tags separadas por vírgula ou espaço"