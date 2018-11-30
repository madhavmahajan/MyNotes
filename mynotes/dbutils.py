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


def create_tree(path, document=None):
    """Create desired as per path and save document as leaf node

    Args:
        path (list): List of nodes build up using absolute path
        document (models.Document): Document object, if leaf node is not a directory
    """
    if path[0] != "root":
        raise Exception("Invalid path '{}' of the document to be saved in the tree".format(path))

    # if path[1] element itself is new, it's parent wil be set as "root" directory
    try:
        entity_object = models.Tree.objects.get(entity="root")
    except:
        raise Exception("Entry '{}' not found in the tree! Please check if setup is executed.".format('root'))

    if not document:
        # If document is not being saved at a leaf node of the path, it is assumed that leaf is also a directory
        directory_path = path[:]
    else:
        # If document is to be saved at a leaf node, it is assumed that path till second last entries are directory
        directory_path = path[:-1]

    # Create required directory hierarchy
    for entity in directory_path:
        parent = entity_object
        try:
            entity_object = models.Tree.objects.get(entity=entity, parent=parent)
        except models.Tree.DoesNotExist:
            entity_object = models.Tree.objects.create(entity=entity, document=None, parent=parent)
            entity_object.save()
            try:
                entity_object = models.Tree.objects.get(entity=entity, parent=parent)
            except Exception as e:
                raise Exception("Failed to create node '{}' in tree. Reason - {}".format(entity, e))

    if document:
        # Save document as a leaf node in the tree
        try:
            entity_object = models.Tree.objects.create(entity=path[-1], document=document, parent=entity_object)
            entity_object.save()
        except Exception as e:
            raise Exception("Failed to save document. Reason - {}".format(e))


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

        # Create tree and save it as a leaf node
        path = ["root", "daily-notes", str(year), str(month), str(day)]
        create_tree(path, document)


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
        list_of_documents.append(
            (document.name.replace('-', '/'), utils.format_certain_string_in_content(data.data, search_str))
        )
    return list_of_documents
