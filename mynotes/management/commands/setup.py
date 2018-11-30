"""
Description: This setup script will initial newly created database with all the required entries in various tables.
To run this script execute, python manage.py setup
"""

from django.core.management.base import BaseCommand
from django.db import connection

from mynotes import models
from mynotes import constants


class Command(BaseCommand):
    help = 'Sets up the newly created database with all the required entries in various tables'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Setting up the MyNotes database"))

        # 1. Record default encryption key
        models.Encryption(algo=constants.NO_ENCRYPTION_ALGORITHM, key=constants.NO_ENCRYPTION_KEY).save()

        # 2. Record default data-types (text and file)
        models.DataType(type=constants.TEXT_DATA_TYPE).save()
        models.DataType(type=constants.FILE_DATA_TYPE).save()

        # 3. Record default tags (daily-notes and personal)
        models.Tag(tag=constants.DAILY_NOTE_TAG).save()
        models.Tag(tag=constants.PERSONAL_TAG).save()

        # 4. Record deafult document-types (directory, daily-notes, notes)
        # models.DocumentType(type="directory").save()
        models.DocumentType(type=constants.DAILY_NOTES_DOCUMENT_TYPE).save()
        models.DocumentType(type=constants.NOTES_DOCUMENT_TYPE).save()

        # 5. Record "root" directory in tree
        cmd= "insert into mynotes_tree values(0, 'root', null, 0);"
        cursor = connection.cursor()
        cursor.execute(cmd)
        cursor.close()

        # 6. Record 2 directories (daily-notes and personal) in root directory
        root = models.Tree.objects.get(entity__exact=constants.ROOT_DIRECTORY)
        models.Tree(entity=constants.DAILY_NOTES_DIRECTORY, parent=root, document=None).save()
        models.Tree(entity=constants.PERSONAL_DIRECTORY, parent=root, document=None).save()

        self.stdout.write(self.style.SUCCESS("Successfully setup MyNotes database"))
