from django.db import models


class Issue(models.Model):
    summary = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        verbose_name="Краткое описание"
    )
    description = models.TextField(
        max_length=1000,
        null=True,
        blank=True,
        verbose_name="Полное описание"
    )
    status = models.ForeignKey(
        to='issue_tracker.Status',
        on_delete=models.PROTECT,
        related_name='status',
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Время обновления'
    )
    type = models.ManyToManyField(
        to='issue_tracker.Type',
        related_name='type',
        verbose_name='Тип',
        blank=True
    )
    project = models.ForeignKey(
        to='issue_tracker.Project',
        on_delete=models.PROTECT,
        related_name='project',
        verbose_name='Проект',
        default=2
    )

    def __str__(self):
        return f"{self.summary} - {self.status}"
