from django import forms
from .models import Tweets

class TweetForm(forms.ModelForm):
    body = forms.CharField( required=True,widget=forms.widgets.Textarea(
        attrs={
        "placeholder":"Enter your tweets here",
        "class":"form-control",
        }
    ),
    label="",
    )

    class Meta:
        model= Tweets
        exclude=("user",)