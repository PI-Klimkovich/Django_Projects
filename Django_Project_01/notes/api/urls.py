from django.urls import path
from .views import NoteListAPIView, NoteDetailAPIView, TagListCreateAPIViews, UserListCreateAPIViews

# /api/notes/
app_name = 'posts:api'

urlpatterns = [
    path('', NoteListAPIView.as_view(), name='notes'),
    path('<uuid:pk>/', NoteDetailAPIView.as_view(), name='note-detail'),
    path('tags/', TagListCreateAPIViews.as_view(), name='tags'),
    path('users/', UserListCreateAPIViews.as_view(), name='users'),

]