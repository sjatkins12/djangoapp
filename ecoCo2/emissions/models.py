from django.db import models


class Co2Timestamp(models.Model):
    datetime = models.DateTimeField(primary_key=True)
    value = models.IntegerField()
