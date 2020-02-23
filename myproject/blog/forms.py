from django import forms
from .models import Comment

class UserCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content','Poster','author']
        widgets = {'Poster': forms.HiddenInput(), 'author': forms.HiddenInput()}
