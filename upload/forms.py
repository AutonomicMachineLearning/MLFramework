from django import forms

from upload.models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['document', ]
        labels = None



#####################################################################
#####################################################################
