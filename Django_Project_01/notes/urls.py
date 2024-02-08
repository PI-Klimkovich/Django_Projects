from django.urls import path
from . import views

urlpatterns = [
    path('create_ok', views.about_create, name='create_ok'),
    path('create', views.create_note_view, name='create'),
    path('tags', views.show_tags_view, name='all_tags'),
    # path('tag_notes', views.show_tags_view, name='tag_notes'),
    path('<uuid:note_uuid>', views.show_note_view, name='note'),
    path("<note_uuid>/update", views.update_note_view, name="update"),
    path("<note_uuid>/delete", views.delete_note_view, name="delete"),
    path("<username>/notes", views.user_notes_view, name="user_notes"),
    path("<username>/u_notes", views.your_notes_view, name="your_notes"),
]
