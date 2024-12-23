# Generated by Django 5.1.4 on 2024-12-21 15:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lab_number', models.CharField(max_length=100)),
                ('goal', models.TextField()),
                ('task', models.TextField()),
                ('workflow', models.TextField()),
                ('conclusion', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('caption', models.CharField(max_length=255)),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='reports.report')),
            ],
        ),
    ]
