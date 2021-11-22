from django import forms
from .models import Recruit, Comment


class RecruitForm(forms.ModelForm):

    class Meta:
        model = Recruit
        fields = ('title', 'content', 'max_cnt', 'public_id', 'public_pw',)

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        min_length=2,
        max_length=200,
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    class Meta:
        model = Comment
        fields = ('content', )