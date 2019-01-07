from django import forms

from modeling.models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['document', ]
        labels = None



#####################################################################
#####################################################################
