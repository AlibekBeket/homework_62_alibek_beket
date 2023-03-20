from django.db import models


class Status(models.Model):
    status_name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        verbose_name="Название"
    )

    def __str__(self):
        return self.status_name
