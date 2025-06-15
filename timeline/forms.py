from django import forms
from .models import Comment
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.forms import AuthenticationForm

class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=CKEditorWidget(), label="Your comment")

    class Meta:
        model = Comment
        fields = ['comment', 'parent']  # if you want parent replies support; else just ['comment']
        widgets = {
            'parent': forms.HiddenInput(),  # hide parent input, set via JS if needed
        }

class TailwindLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'bg-stone-400 text-stone-800 border border-stone-700 rounded px-2 py-1 w-full focus:outline-none focus:ring-2 focus:ring-amber-400'
        }),
        label='Username'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'bg-stone-400 text-stone-800 border border-stone-300 rounded px-2 py-1 w-full focus:outline-none focus:ring-2 focus:ring-amber-400'
        }),
        label='Password'
    )