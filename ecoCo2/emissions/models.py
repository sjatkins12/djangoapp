from django.db import models


class Co2TimestampQuerySet(models.QuerySet):
    def get(self, *args, **kwargs):
        """
        Accept datetime as valid way to get an instance of Co2 timestamp
        """
        kwargs = self._split_datetime(**kwargs)

        return super().get(*args, **kwargs)

    def get_or_create(self, *args, **kwargs):
        """
        Accept datetime as valid way to get_or_create an instance of Co2 timestamp
        """
        kwargs = self._split_datetime(**kwargs)

        return super().get_or_create(*args, **kwargs)

    def _split_datetime(self, **kwargs):
        """
        Check to see if key 'datetime' is included in kwargs. Split the datetime to a date and hour
        """
        datetime = kwargs.get("datetime")
        if datetime:
            kwargs["hour"] = datetime.hour * 60 + datetime.minute
            kwargs["date"] = datetime.date()
            del kwargs["datetime"]

        return kwargs


class Co2TimestampManager(models.Manager):
    def create(self, datetime, value):
        """
        override create to accept datetime kwarg for object creation
        """
        hour = datetime.hour * 60 + datetime.minute
        date = datetime.date()
        value = value

        return super().create(hour=hour, date=date, value=value)


class Co2Timestamp(models.Model):
    hour = models.SmallIntegerField()
    date = models.DateField()
    value = models.IntegerField()

    class Meta:
        unique_together = ("hour", "date")

    objects = Co2TimestampManager.from_queryset(Co2TimestampQuerySet)()
