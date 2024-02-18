import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Func


class GroupConcat(Func):
    function = 'GROUP_CONCAT'
    template = '%(function)s(%(expressions)s)'


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    objects = models.Manager()  # Он подключается к базе.

    def __str__(self):
        return self.name


def upload_to(instance: "Note", filename: str) -> str:
    """Путь для файла относительно корня медиа хранилища."""
    return f"{instance.uuid}/{filename}"


class Note(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name="Заголовок", help_text="Не более 255 символов")
    anons = models.CharField(max_length=255, verbose_name="Анонс", help_text="Не более 255 символов")
    content = models.TextField(verbose_name="Содержание заметки")
    created_at = models.DateTimeField(auto_now_add=True)
    # auto_now_add=True автоматически добавляет текущую дату и время.
    mod_time = models.DateTimeField(null=True, blank=True, auto_now=True, db_index=True)

    # image = models.FileField(upload_to=upload_to, null=True)
    image = models.ImageField(upload_to=upload_to, null=True, blank=True, verbose_name="Превью")

    tags = models.ManyToManyField(Tag, related_name="notes", verbose_name="Теги")

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="Владелец")
    # `on_delete=models.CASCADE`
    # При удалении пользователя, удалятся все его записи.

    # Менеджер объектов (Это и так будет по умолчанию добавлено).
    # Но мы указываем явно, чтобы понимать, откуда это берется.
    objects = models.Manager()  # Он подключается к базе.

    class Meta:
        # db_table = 'notes'  # Название таблицы в базе.
        # ordering = ['-created_at']  # Дефис это означает DESC сортировку (обратную).
        ordering = ['-mod_time']  # Сортировка по умолчанию.
        indexes = [
            models.Index(fields=("created_at",), name="created_at_index"),
            models.Index(fields=("mod_time",), name="mod_at_index")
        ]

    def __str__(self):
        return f"Заметка: \"{self.title}\""
