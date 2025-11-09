from django import forms
from django.forms.widgets import FileInput
from .models import Post, Photo, Tag

class MultipleFileInput(FileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={'accept': 'image/*'}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class PostForm(forms.ModelForm):
    tags_text = forms.CharField(required=False, help_text="쉼표(,)로 구분하여 태그 입력")
    images = MultipleFileField(
        required=True,
        label="이미지들"
    )

    class Meta:
        model = Post
        fields = ["caption", "gallery", "is_public"]
        widgets = {
            'caption': forms.Textarea(attrs={'rows': 4}),
        }