# from django.shortcuts import get_object_or_404
# from rest_framework import generics
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from notes.api.permissions import IsOwnerOrReadOnly
from notes.api.serializers import NoteSerializer, TagSerializer, UserSerializer
from notes.models import Note, Tag
from user.models import User


class NoteListAPIView(ListCreateAPIView):
    queryset = Note.objects.all()[:5]
    serializer_class = NoteSerializer


class NoteDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    permission_classes = [IsOwnerOrReadOnly]


class TagListCreateAPIViews(ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]


class UserListCreateAPIViews(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
