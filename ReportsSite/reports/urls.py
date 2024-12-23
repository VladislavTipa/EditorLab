from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_report, name='create_report'),
    path('report/<int:report_id>/', views.view_report, name='view_report'),
    path('report/<int:report_id>/download/', views.download_pdf, name='download_pdf'),  # Маршрут для загрузки PDF
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
