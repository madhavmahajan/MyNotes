"""
Description: Utilities around database models to perform CRUD operations followed by business logic
"""

import datetime

from . import models
from . import utils


def get_settings():
    """Return settings from Settings table

    Returns:
        Dictionary containing settings
    """
    return {
        'key1': 'value1',
        'key2': 'value2',
    }


def get_list_of_document_types():
    """Get list of document types from db

    Returns:
        List of document types
    """
    types = []
    all = models.DocumentType.objects.all()
    for type in all:
        types.append(type.type)
    return types


def get_list_of_notes():
    """Get list of notes from db

    Returns:
        List of notes
    """
    list_of_notes = []
    documents = models.Document.objects.filter(type__type='daily-notes')
    for document in documents:
        list_of_notes.append(document.name.replace('-', '/'))
    return list_of_notes


def fetch_note_object_for_date(year, month, day):
    """Get note document object for a particular date

    Args:
        year (int): Year
        month (int): Month
        day (int): Day

    Returns:
        Model object for a note
    """
    document_name = utils.generate_notes_file_name(year, month, day)
    document = models.Document.objects.get(name=document_name)
    return document


def get_notes_for_date(year, month, day):
    """Get note for a particular date

    Args:
        year (int): Year
        month (int): Month
        day (int): Day

    Returns:
        Note's content
    """
    try:
        notes = fetch_note_object_for_date(year, month, day)
        return notes.data.data
    except models.Document.DoesNotExist:
        return ["Notes not found for date {}.\n".format(utils.get_formatted_date(year, month, day)),
                 "Please edit this document and save."
                 ]


def get_access_and_modify_time_for_notes(year, month, day):
    """Get attributes of a note

    Args:
        year (int): Year
        month (int): Month
        day (int): Day

    Returns:
        Attributes of a note in a form of dictionary
    """
    try:
        document = fetch_note_object_for_date(year, month, day)
        return {
                'size': len(document.data.data),
                'ctime': document.atime,
                'mtime': document.mtime,
                'format': document.data.type.type,
        }
    except models.Document.DoesNotExist:
        return {
            'size': 0,
            'ctime': '',
            'mtime': '',
            'format': None,
        }


def save_note(year, month, day, notes):
    """Create new note or update previously saved note

    Args:
        year (int): Year
        month (int): Month
        day (int): Day

    Returns:
        None
    """
    document_name = utils.generate_notes_file_name(year, month, day)

    try:
        document = fetch_note_object_for_date(year, month, day)
        data = document.data
        data.data = notes
        data.mtime = document.mtime = datetime.datetime.now()
        data.save()
        document.save()
    except:
        # save data
        datatype = models.DataType.objects.get(type='text')
        encrypt_key = models.Encryption.objects.get(algo='')
        ctime = datetime.datetime.now()
        data = models.Data.objects.create(type=datatype, data=notes, flag=0, encrypt_key=encrypt_key, mtime=ctime)
        data.save()

        # save document
        document_type = models.DocumentType.objects.get(type='daily-notes')
        document = models.Document.objects.create(name=document_name, type=document_type, data=data, ctime=ctime,
                                                  atime=ctime, mtime=ctime)
        document.save()

        # save it in tree
        parent = models.Tree.objects.get(entity='daily-notes')
        tree = models.Tree.objects.create(entity=document_name, document=document, parent=parent)
        tree.save()


def search_data_in_documents(search_str):
    """Search data in all the documents

    Args:
        search_str (str): String to be search in all the documents

    Returns:
        List of tuples containing document object and content
    """
    list_of_documents = []
    data_list = models.Data.objects.filter(data__icontains=search_str)
    for data in data_list:
        try:
            document = models.Document.objects.get(data=data)
        except models.Document.DoesNotExist:
            continue
        list_of_documents.append((document.name.replace('-', '/'), data.data))
    return list_of_documents
