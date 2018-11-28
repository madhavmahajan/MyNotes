"""
Description: Forms are defined in this module
"""

from django import forms

from . import dbutils


class NoteForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)


class SearchForm(forms.Form):
    types = dbutils.get_list_of_document_types()
    document_type = [(type, type) for type in types]

    type = forms.ChoiceField(choices=document_type)
    search_str = forms.CharField(min_length=5, max_length=50, strip=True)
