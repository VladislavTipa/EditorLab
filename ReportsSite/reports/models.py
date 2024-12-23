from django.db import models


class Report(models.Model):
    objects = None
    lab_number = models.CharField(max_length=50)
    goal = models.TextField()
    task = models.TextField()
    conclusion = models.TextField()


class ReportContent(models.Model):
    objects = None
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='contents')
    content_type = models.CharField(max_length=10, choices=(('text', 'Текст'), ('image', 'Изображение'), ('code', 'Код')))
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='report_images/', blank=True, null=True)
    image_caption = models.CharField(max_length=255, blank=True, null=True)
    code = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']
