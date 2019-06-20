from django.db import models

from datetime import datetime


class FileModel(models.Model):
    file_name = models.CharField(max_length=255)
    original_name = models.CharField(max_length=255)
    upload_time = models.DateTimeField(default=datetime.now)


class ThemeModel(models.Model):
    file = models.ForeignKey(FileModel, on_delete=models.CASCADE)
    # file_id = models.IntegerField()
    title = models.CharField(max_length=255)
    comments = models.TextField(null=True)


class ItemModel(models.Model):
    # theme_id = models.IntegerField()
    # file_id = models.IntegerField()
    theme = models.ForeignKey(ThemeModel, on_delete=models.CASCADE)
    file = models.ForeignKey(FileModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    point = models.DecimalField(max_digits=5, decimal_places=2)
