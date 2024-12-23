from django import forms
from .models import Report


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['lab_number', 'goal', 'task']
        labels = {
            'lab_number': 'Номер лабораторной работы',
            'goal': 'Цель',
            'task': 'Задача',
        }


class ConclusionForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['conclusion']
        labels = {
            'conclusion': 'Заключение',
        }
