from django.urls import path
from . import views

urlpatterns = [
            path('', views.api_info, name='api_info'),
            path('xml_to_excel_api', views.xml_to_excel, name=''),
]

""""Developed by Matesh Divekar 07-08-2022"""