"""
Description: This setup script will initial newly created database with all the required entries in various tables.
To run this script execute, python manage.py setup
"""

from django.core.management.base import BaseCommand
from django.db import connection

from mynotes import models


class Command(BaseCommand):
    help = 'Sets up the newly created database with all the required entries in various tables'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Setting up the MyNotes database"))

        # 1. Record default encryption key
        models.Encryption(algo='', key='').save()

        # 2. Record default data-types (text and file)
        models.DataType(type="text").save()
        models.DataType(type="file").save()

        # 3. Record default tags (daily-notes and personal)
        models.Tag(tag="daily-notes").save()
        models.Tag(tag="personal").save()

        # 4. Record deafult document-types (directory, daily-notes, notes)
        models.DocumentType(type="directory").save()
        models.DocumentType(type="daily-notes").save()
        models.DocumentType(type="notes").save()

        # 5. Record "root" directory in tree
        cmd= "insert into mynotes_tree values(0, 'root', null, 0);"
        cursor = connection.cursor()
        cursor.execute(cmd)
        cursor.close()

        # 6. Record 2 directories (daily-notes and personal) in root directory
        root = models.Tree.objects.get(entity__exact="root")
        models.Tree(entity="daily-notes", parent=root, document=None).save()
        models.Tree(entity="personal", parent=root, document=None).save()

        self.stdout.write(self.style.SUCCESS("Successfully setup MyNotes database"))
