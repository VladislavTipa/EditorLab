from django.shortcuts import render, redirect
import json
from .forms import ReportForm, ConclusionForm
import asyncio
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from playwright.async_api import async_playwright
from .models import Report, ReportContent
import shutil
import platform


def home(request):
    return render(request, 'reports/home.html')


def get_default_browser_path():
    system = platform.system()
    if system == "Windows":
        return shutil.which("chrome") or "C:/Program Files/Google/Chrome/Application/chrome.exe"
    elif system == "Linux":
        return shutil.which("google-chrome") or shutil.which("chromium-browser")
    elif system == "Darwin":
        return "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    else:
        raise Exception("Операционная система не поддерживается")


def create_report(request):
    if request.method == "POST":
        print("POST data:", request.POST)
        print("FILES data:", request.FILES)
        report_form = ReportForm(request.POST)
        conclusion_form = ConclusionForm(request.POST)

        if report_form.is_valid() and conclusion_form.is_valid():
            report = report_form.save(commit=False)
            report.conclusion = conclusion_form.cleaned_data['conclusion']
            report.save()

            sections_order = request.POST.get('sections_order', '[]')
            try:
                sections_order = json.loads(sections_order)
            except ValueError:
                sections_order = []

            text_sections = request.POST.getlist('sections_text[]')
            image_files = request.FILES.getlist('sections_image[]')
            image_captions = request.POST.getlist('sections_image_caption[]')
            code_sections = request.POST.getlist('sections_code[]')

            order = 0

            for section_type in sections_order:
                if section_type == 'text' and text_sections:
                    text = text_sections.pop(0)
                    if text.strip():
                        ReportContent.objects.create(
                            report=report,
                            content_type='text',
                            text=text,
                            order=order
                        )
                        order += 1

                elif section_type == 'image' and image_files:
                    image = image_files.pop(0)
                    caption = image_captions.pop(0) if image_captions else ''
                    if image:
                        content = ReportContent(
                            report=report,
                            content_type='image',
                            image=image,
                            image_caption=caption,
                            order=order
                        )

                        content.save()

                        order += 1

                elif section_type == 'code' and code_sections:
                    code = code_sections.pop(0)
                    if code.strip():
                        ReportContent.objects.create(
                            report=report,
                            content_type='code',
                            code=code,
                            order=order
                        )
                        order += 1
                print(f"Processed sections: {order}")

            return redirect('view_report', report_id=report.id)

    else:
        report_form = ReportForm()
        conclusion_form = ConclusionForm()

    return render(request, 'reports/create_report.html', {
        'report_form': report_form,
        'conclusion_form': conclusion_form,
    })


def view_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report_contents = report.contents.all().order_by('order')
    return render(request, 'reports/view_report.html', {'report': report, 'contents': report_contents})


async def generate_pdf(html_content):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.set_content(html_content, wait_until="networkidle")

        # Генерация PDF
        pdf = await page.pdf(format='A4', print_background=True)

        await browser.close()
        return pdf


def generate_pdf_sync(html_content):
    return asyncio.run(generate_pdf(html_content))


def download_pdf(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    contents = report.contents.all().order_by('order')

    for content in contents:
        if content.content_type == 'image' and content.image:
            print("Изображение")
            content.image_url = request.build_absolute_uri(content.image.url)
            print(content.image_url)

    html_string = render_to_string(
        'reports/pdf_template.html',
        {'report': report, 'contents': contents},
        request=request
    )

    pdf = generate_pdf_sync(html_string)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="report_{report_id}.pdf"'
    return response
