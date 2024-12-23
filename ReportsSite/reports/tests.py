from django.test import TestCase
from django.urls import reverse
from .models import Report, ReportContent
import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings


class ReportCreationTest(TestCase):
    def test_create_report(self):
        # Данные для формы
        form_data = {
            'lab_number': '1',
            'goal': 'Цель эксперимента',
            'task': 'Описание задания',
            'conclusion': 'Заключение эксперимента',
            'sections_order': '["text", "image", "code"]',
            'sections_text[]': ['Текстовый контент'],
            'sections_image_caption[]': ['Подпись к изображению'],
            'sections_code[]': ['Код программы']
        }

        # Загружаем тестовое изображение из папки test_assets
        test_image_path = os.path.join(settings.BASE_DIR, 'reports/test_assets/test_image.jpg')
        with open(test_image_path, 'rb') as image_file:
            form_files = {
                'sections_image[]': SimpleUploadedFile(
                    name='test_image.jpg',
                    content=image_file.read(),
                    content_type='image/jpeg'
                )
            }

            response = self.client.post(reverse('create_report'), data=form_data, files=form_files)
        print(f"Form files: {form_files}")


        self.assertEqual(response.status_code, 302)

        report = Report.objects.get(lab_number='1')
        self.assertEqual(report.goal, 'Цель эксперимента')
        self.assertEqual(report.task, 'Описание задания')
        self.assertEqual(report.conclusion, 'Заключение эксперимента')

        contents = ReportContent.objects.filter(report=report)
        self.assertEqual(contents.count(), 2)
        self.assertEqual(contents.first().content_type, 'text')
        self.assertEqual(contents.first().text, 'Текстовый контент')


class PDFGenerationTest(TestCase):
    def setUp(self):
        self.report = Report.objects.create(
            lab_number='1',
            goal='Цель эксперимента',
            task='Описание задания',
            conclusion='Заключение эксперимента'
        )
        ReportContent.objects.create(
            report=self.report,
            content_type='text',
            text='Текстовый контент',
            order=0
        )

    def test_download_pdf(self):
        response = self.client.get(reverse('download_pdf', args=[self.report.id]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

        self.assertIn(b'%PDF', response.content[:4])
