from django.urls import path
from .views import extract_pdf_data,image_to_url

urlpatterns = [
    path('extract/', extract_pdf_data, name='extract_pdf_data'),
    path('imagetourl/',image_to_url,name='image_to_url'),
    
]