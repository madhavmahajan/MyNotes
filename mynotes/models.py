"""
Description: Models are defined in this module
"""

from django.db import models


class Encryption(models.Model):
    algo = models.CharField(max_length=30)
    key = models.CharField(max_length=64)


class DataType(models.Model):
    type = models.CharField(max_length=30)


class Data(models.Model):
    type = models.ForeignKey(to=DataType, on_delete=models.CASCADE)
    data = models.CharField(max_length=1024)
    flag = models.CharField(max_length=30)
    encrypt_key = models.ForeignKey(to=Encryption, on_delete=models.CASCADE)
    mtime = models.TimeField()


class Tag(models.Model):
    tag = models.CharField(max_length=30)


class DocumentType(models.Model):
    type = models.CharField(max_length=30)


class Document(models.Model):
    name = models.CharField(max_length=30)
    type = models.ForeignKey(to=DocumentType, on_delete=models.CASCADE)
    data = models.ForeignKey(to=Data, on_delete=models.CASCADE)
    ctime = models.TimeField()
    atime = models.TimeField()
    mtime = models.TimeField()


class Tree(models.Model):
    entity = models.CharField(max_length=30)
    parent = models.ForeignKey(to='self', on_delete=models.CASCADE)
    document = models.ForeignKey(to=Document, on_delete=models.CASCADE, null=True)


class Mapping(models.Model):
    document = models.ForeignKey(to=Document, on_delete=models.CASCADE)
    tag = models.ForeignKey(to=Tag, on_delete=models.CASCADE)
