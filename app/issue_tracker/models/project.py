from django.db import models


class Project(models.Model):
    name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        verbose_name="Название"
    )
    description = models.TextField(
        max_length=1000,
        null=False,
        blank=False,
        verbose_name="Описание"
    )
    start_date = models.DateField(
        null=False,
        blank=False,
        verbose_name='Дата начала'
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата окончания'
    )
    is_deleted = models.BooleanField(
        verbose_name="Удалено",
        null=False,
        default=False
    )

    def __str__(self):
        return f"{self.name} - {self.start_date}"

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()
