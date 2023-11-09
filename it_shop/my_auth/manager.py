from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy


class CustomUserManager(BaseUserManager):
    """
    Менеджер кастомной модели User, где электронная почта является уникальным идентификатором,
    для аутентификации, вместо username.
    """
    def create_user(self, username, password, **extra_fields):
        """Добавление обычного пользователя."""
        if not username:
            raise ValueError(gettext_lazy('Не указан никнейм'))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Добавление суперпользователя."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(gettext_lazy('У суперпользователя должно быть is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(gettext_lazy('Суперпользователь должен иметь is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)