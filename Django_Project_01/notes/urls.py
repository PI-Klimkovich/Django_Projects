from django.urls import path
from . import views

urlpatterns = [
    path('', views.about_create, name='create_ok'),
    path('create', views.create_note_view, name='create'),
    path('<note_uuid>', views.show_note_view, name='note'),
    # path('user', views.user_notes, name='user_notes'),
    path("<note_uuid>/update", views.update_note_view, name="update"),
    path("<note_uuid>/delete", views.delete_note_view, name="delete"),
]