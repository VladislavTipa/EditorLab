# Generated by Django 5.1.4 on 2024-12-22 13:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0005_remove_report_workflow'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reportimage',
            name='report',
        ),
        migrations.DeleteModel(
            name='ReportCodeBlock',
        ),
        migrations.DeleteModel(
            name='ReportImage',
        ),
    ]