from django.urls import path
from . import views

app_name = 'vault'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('add/', views.credential_create_view, name='add_credential'),
    path('edit/<int:pk>/', views.credential_edit_view, name='edit_credential'),
    path('delete/<int:pk>/', views.credential_delete_view, name='delete_credential'),
]
