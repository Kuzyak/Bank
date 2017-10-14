from django import forms
from .models import Post
"""
from tinymce import models as tinymce_models
from tinymce.widgets import TinyMCE

class PostForm(forms.ModelForm):
    text = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    class Meta:
        model = Post
        exclude = ['text']
"""
class PostForm(forms.ModelForm):
    images = forms.ImageField()
    class Meta:
        model = Post
        fields = ('title', 'text','images',)

class ContactForm(forms.Form):
    full_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
