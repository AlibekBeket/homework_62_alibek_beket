from django import forms
from django.core.validators import BaseValidator
from issue_tracker.models import Issue, Project


class CustomMaxLengthValidator(BaseValidator):
    def __init__(self, limit_value=200):
        message = 'Максимальная длина заголовка %(limit_value)s. Вы ввели %(show_value)s символов.'
        super().__init__(limit_value=limit_value, message=message)

    def compare(self, value, limit_value):
        return limit_value < value

    def clean(self, x):
        return len(x)


class CustomMinLengthValidator(BaseValidator):
    def __init__(self, limit_value=2):
        message = 'Вы ввели %(show_value)s символов, нужно ввести больше %(limit_value)s символов.'
        super().__init__(limit_value=limit_value, message=message)

    def compare(self, value, limit_value):
        return limit_value > value

    def clean(self, x):
        return len(x)


class IssueForm(forms.ModelForm):
    summary = forms.CharField(
        validators=(CustomMinLengthValidator(), CustomMaxLengthValidator())
    )

    class Meta:
        model = Issue
        fields = ('summary', 'description', 'status', 'type')
        labels = {
            'summary': 'Краткое описание',
            'description': 'Описание',
            'status': 'Статус',
            'type': 'Тип'
        }


class SearchForm(forms.Form):
    search = forms.CharField(
        max_length=200,
        required=False,
        label='Найти'
    )


class ProjectForm(forms.ModelForm):
    name = forms.CharField(
        validators=(CustomMinLengthValidator(), CustomMaxLengthValidator())
    )

    class Meta:
        model = Project
        fields = ('name', 'description', 'start_date', 'end_date')
        labels = {
            'name': 'Имя',
            'description': 'Описание',
            'start_date': 'Начало проекта',
            'end_date': 'Конец проекта'
        }
