import uuid
from django.db import models
from django.contrib.auth import get_user_model

import pathlib
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser


def upload_to(instance: "Note", filename: str) -> str:
    """Путь для файла относительно корня медиа хранилища."""
    return f"{instance.uuid}/{filename}"


class Note(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    anons = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # auto_now_add=True автоматически добавляет текущую дату и время.

    # image = models.FileField(upload_to=upload_to, null=True)
    image = models.ImageField(upload_to=upload_to, null=True, blank=True, verbose_name="Превью")

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    # `on_delete=models.CASCADE`
    # При удалении пользователя, удалятся все его записи.

    # Менеджер объектов (Это и так будет по умолчанию добавлено).
    # Но мы указываем явно, чтобы понимать, откуда это берется.
    objects = models.Manager()  # Он подключается к базе.

    class Meta:
        # db_table = 'notes'  # Название таблицы в базе.
        ordering = ['-created_at']  # Дефис это означает DESC сортировку (обратную).
        indexes = [
            models.Index(fields=("created_at",), name="created_at_index"),
        ]

    def __str__(self):
        return f"Заметка: \"{self.title}\""
