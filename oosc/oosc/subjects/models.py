from django.db import models

# Create your models here.

class Subjects(models.Model):
    subject_name = models.CharField(max_length=200)

    def __str__(self):
        return ('subject_name')
