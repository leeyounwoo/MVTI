from django import forms
from .models import Review, ReviewComment


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('title', 'content', 'rank',)

class ReviewCommentForm(forms.ModelForm):
    content = forms.CharField(
        min_length=2,
        max_length=200,
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    class Meta:
        model = ReviewComment
        fields = ('content', )