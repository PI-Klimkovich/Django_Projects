from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required

from .models import Note


def home_page_view(request):
    return render(request, "home.html")


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
        return HttpResponseRedirect(reverse('note', args=[note.uuid]))

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
        Note.objects.filter(uuid=note_uuid).delete()
    return HttpResponseRedirect(reverse("home"))

