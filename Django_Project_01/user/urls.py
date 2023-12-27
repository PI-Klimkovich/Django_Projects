from django.urls import path
from . import views

urlpatterns = [
    path('reg_ok', views.about_registration, name='reg_ok'),
]
