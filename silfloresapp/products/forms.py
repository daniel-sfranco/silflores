from django import forms
from . import models

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        required = kwargs.get('required', True)
        kwargs.setdefault("widget", MultipleFileInput())
        kwargs.setdefault("required", required)
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
    def __init__(self, *args, **kwargs):
        required = kwargs.pop('required', True)
        super(PhotoForm, self).__init__(*args, **kwargs)
        self.fields['images'] = MultipleFileField(label="Fotos", required=required)

class ProductForm(forms.ModelForm):
    tags = forms.CharField(required=False, widget=forms.Textarea)
    class Meta:
        model = models.Product
        fields = ['name', 'price', 'desc', 'term', 'stock', 'tags', 'size_type', 'size']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].widget = forms.Textarea()
        self.fields['tags'].help_text = "Insira as tags separadas por vírgula"
        self.fields['size'].help_text = "Insira os tamanhos separados por espaço"
        self.fields['size'].label = "Tamanho(cm)"
        self.fields['size'].required = False

class ProductChangeForm(forms.ModelForm):
    size = forms.CharField(required=False)
    tags = forms.CharField(required=False, widget=forms.Textarea)
    class Meta:
        model = models.Product
        fields = ['name', 'price', 'desc', 'term', 'stock','size_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')

        if instance:
            tag_names = ', '.join(tag.name for tag in instance.tags.all())
            self.fields['tags'].initial = tag_names
        self.fields['tags'].widget = forms.Textarea()
        self.fields['tags'].help_text = "Insira as tags separadas por vírgula"
        self.fields['size'].help_text = "Insira os tamanhos separados por vírgula"
        self.fields['size'].label = "Tamanho(cm)"
        self.fields['size'].required = False
