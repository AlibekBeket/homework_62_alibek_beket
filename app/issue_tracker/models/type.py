from django.db import models


class Type(models.Model):
    type_name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        verbose_name="Название"
    )

    def __str__(self):
        return self.type_name
