from django import forms


class CommentForm(forms.Form):
    author = forms.CharField(
        max_length = 60,
        widget = forms.TextInput(attrs={
            "class": "field-row",
            "placeholder": "Your Name"
        })
    )
    body = forms.CharField(widget=forms.Textarea(
        attrs = {
            "class": "field-row-stacked",
            "placeholder": "Leave a comment."
        }
    ))
    verification = forms.CharField(
        max_length = 10,
        widget = forms.TextInput(attrs={
            "class": "field-row",
            "placeholder": "Input verification code"
        })
    )