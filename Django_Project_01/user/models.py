from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Наследуем все поля из `AbstractUser`
    Добавляем новые поля `phone` и 'country'
    """
    phone = models.CharField(max_length=11, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = "users"
