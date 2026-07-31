from django.urls import path
from . import views

app_name = 'generator'

urlpatterns = [
    path('', views.generate_password_view, name='generate'),
    path('api/generate/', views.generator_api_view, name='api_generate'),
]
