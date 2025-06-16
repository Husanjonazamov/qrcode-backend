from django import forms

from core.apps.api.models import GenerateModel


class GenerateForm(forms.ModelForm):

    class Meta:
        model = GenerateModel
        fields = "__all__"
