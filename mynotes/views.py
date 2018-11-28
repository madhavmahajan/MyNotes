"""
Description: Views are defined in this module
"""

from django.shortcuts import render
from . import utils, dbutils
from . import forms


def settings(request):
    """View for setting page
    """
    context = {
        'settings': dbutils.get_settings(),
        'search_form': forms.SearchForm(),
    }
    return render(request, 'mynotes/settings.html', context)


def notes_view(request, year=None, month=None, day=None):
    """View for notes page
    """
    if request.method == 'POST':
        form = forms.NoteForm(request.POST)
        if not form.is_valid():
            context = {}
            return render(request, 'mynotes/notes_page.html', context)
        notes = form.cleaned_data['content']
        dbutils.save_note(year, month, day, notes.replace('\n', ''))

    if not (year or month or day):
        year, month, day = utils.get_todays_date()
    notes = dbutils.get_notes_for_date(year, month, day)
    stats = dbutils.get_access_and_modify_time_for_notes(year, month, day)
    context = {
        'date': utils.get_formatted_date(year, month, day),
        'notes': notes,
        'list': dbutils.get_list_of_notes(),
        'form': forms.NoteForm(),
        'search_form': forms.SearchForm(),
        'alert': {},
    }
    context.update(stats)
    return render(request, 'mynotes/notes_page.html', context)


def search_view(request):
    """View for search page
    """
    if request.method == 'POST':
        form = forms.SearchForm(request.POST)
        if form.is_valid():
            type = form.cleaned_data['type']
            search_str = form.cleaned_data['search_str']
            documents = dbutils.search_data_in_documents(search_str)
            context = {
                'search_str': search_str,
                'document_type': type,
                'documents': documents,
                'search_form': form,
            }
            return render(request, 'mynotes/search_page.html', context)
    form = forms.SearchForm()
    context = {
        'search_form': form,
    }
    return render(request, 'mynotes/search_page.html', context)
