from django import forms
from .models import Post, IcoName
from tinymce import models as tinymce_models
from tinymce.widgets import TinyMCE

"""
from tinymce import models as tinymce_models
from tinymce.widgets import TinyMCE

class PostForm(forms.ModelForm):
    text = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    class Meta:
        model = Post
        exclude = ['text']
"""

class IcoNameForm(forms.ModelForm):
    ICO_name = forms.CharField(required=True,label='ICOs name')
    platform = forms.CharField(required=True)
    info_block = forms.CharField()
    link = forms.CharField(required=True)
    start_date = forms.DateTimeField(widget=forms.SelectDateWidget())
    ICO_image = forms.ImageField(required=True,label='ICOs image')
    class Meta:
        model = IcoName
        fields = ('ICO_name', 'platform','info_block','start_date','link','ICO_image',)

class PostForm(forms.ModelForm):
    title = forms.CharField(required=True)
    text = forms.CharField(required=True,widget=TinyMCE(attrs={'cols': 100, 'rows': 30}))
    published_date = forms.DateTimeField(widget=forms.SelectDateWidget())
    images = forms.ImageField(required=True)
    class Meta:
        model = Post
        fields = ('title', 'text','published_date','images',)

class ContactForm_en(forms.Form):
    full_name = forms.CharField(required=True,label='Full name')
    email = forms.EmailField(required=True,label='Email')
    subject = forms.CharField(required=True,label='Subject')
    message = forms.CharField(widget=forms.Textarea, required=True,label='Message')

class ContactForm(forms.Form):
    full_name = forms.CharField(required=True,label='Teljes név')
    email = forms.EmailField(required=True,label='Email')
    subject = forms.CharField(required=True,label='Tantárgy')
    message = forms.CharField(widget=forms.Textarea, required=True,label='Üzenet')
