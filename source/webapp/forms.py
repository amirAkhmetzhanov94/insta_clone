from django import forms
from django.forms import widgets

from webapp.models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["picture", "description"]


class CommentForm(forms.ModelForm):
    text = forms.CharField(max_length=100, label="", widget=widgets.Input(attrs={"class": "mt-3",
                                                                                 "placeholder": "Write your comment",
                                                                                 "style": "border: none; "
                                                                                          "border-color: none; "
                                                                                          "box-shadow: none;"}))

    class Meta:
        model = Comment
        fields = ["text"]
