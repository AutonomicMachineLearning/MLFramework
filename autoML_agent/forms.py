from django import forms

from autoML_agent.models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['document', ]
        labels = None