from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings

import os
import shutil

from .models import Note
from user.models import User


def home_page_view(request):
    all_notes = Note.objects.all()  # Получение всех записей из таблицы этой модели.
    context: dict = {
        "notes": all_notes
    }
    return render(request, "home.html", context)


def about_view(request):
    return render(request, "about.html")


def about_create(request):
    return render(request, "note/create_ok.html")


@login_required
def create_note_view(request: WSGIRequest):
    if request.method == "POST":
        note = Note.objects.create(
            title=request.POST["title"],
            anons=request.POST["anons"],
            content=request.POST["content"],
            image=request.FILES.get("noteImage"),
            user=request.user,
        )
        return render(request, "note/create_ok.html", {"note": note})
        # return HttpResponseRedirect(reverse('note', args=[note.uuid]))

    # Вернется только, если метод не POST.
    return render(request, "note/create_note.html")


def show_note_view(request: WSGIRequest, note_uuid):
    try:
        note = Note.objects.get(uuid=note_uuid)  # Получение только ОДНОЙ записи.
    except Note.DoesNotExist:
        # Если не найдено такой записи.
        raise Http404

    return render(request, "note/note.html", {"note": note})


def delete_note_view(request: WSGIRequest, note_uuid: str):
    if request.method == "POST":
        Note.objects.get(uuid=note_uuid).image.delete(save=True)
        Note.objects.get(uuid=note_uuid).delete()
        # os.rmdir(image_path)
        image_path = os.path.join(settings.MEDIA_ROOT, note_uuid)
        shutil.rmtree(image_path)
    return HttpResponseRedirect(reverse("home"))


def update_note_view(request: WSGIRequest, note_uuid):
    if request.method == "POST":
        note = Note.objects.get(uuid=note_uuid)
        new_image = request.FILES.get("noteImage")
        if new_image:
            # Удаление старого изображения
            if note.image:
                old_image_path = os.path.join(settings.MEDIA_ROOT, note.image.name)
                if os.path.isfile(old_image_path):
                    os.remove(old_image_path)
            note.image = new_image
        note.title = request.POST.get('title', note.title)
        note.anons = request.POST.get('anons', note.anons)
        note.content = request.POST.get('content', note.content)
        note.mod_time = timezone.now()
        note.save()
        return render(request, "note/update_ok.html", {"note": note})
        # return HttpResponseRedirect(reverse('note', args=[note.uuid]))
    note = Note.objects.get(uuid=note_uuid)
    return render(request, "note/update_note.html", {"note": note})


# заметки выбранного пользователя
def user_notes_view(request: WSGIRequest, username):
    user = User.objects.get(username=username)
    user_notes = Note.objects.filter(user=user)
    print(username)
    return render(request, 'note/user_notes.html', {"notes": user_notes, "username": username})


# заметки авторизованного пользователя
@login_required()
def your_notes_view(request: WSGIRequest, username):
    user = User.objects.get(username=username)
    user_notes = Note.objects.filter(user=user)
    print(username)
    return render(request, 'note/your_notes.html', {"notes": user_notes, "username": username})


def show_your_note_view(request: WSGIRequest, note_uuid):
    try:
        note = Note.objects.get(uuid=note_uuid)  # Получение только ОДНОЙ записи.
    except Note.DoesNotExist:
        # Если не найдено такой записи.
        raise Http404
    return render(request, "note/your_note.html", {"note": note})
