from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contacts/', views.get_contacts, name='get_contacts'),
    path('contacts/<str:name>/', views.contact_detail, name='contact_detail'),
    path('api/contacts/', views.get_contacts, name='api_get_contacts'),
    path('api/contacts/<str:name>/', views.contact_detail, name='api_contact_detail'),
] 