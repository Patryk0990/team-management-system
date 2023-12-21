from django import forms

from projects.models import Board


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ('name', )
