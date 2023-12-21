from django import forms

from projects.models import BoardColumn


class BoardColumnForm(forms.ModelForm):
    class Meta:
        model = BoardColumn
        fields = ('name', )
