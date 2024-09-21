from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import BaseUserManager


class EmployeeUserManager(BaseUserManager):
    """Менеджер для подели пользователя кабинета"""

    def create_user(self, email, lastname, firstname, password=None):
        """Создание пользователя"""

        if not email:
            raise ValueError("Для пользователя обязательно указание электронной почты")
        
        email = self.normalize_email(email)
        user = self.model(email=email, lastname=lastname, firstname=firstname)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, lastname, firstname, password):
        """Создание нового администратора"""

        user = self.create_user(email, lastname, firstname, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user



class EmployeeUser(AbstractBaseUser, PermissionsMixin):
    """Модель пользователя кабинета"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Уникальный идентификатор")
    email = models.EmailField(max_length=255, unique=True, verbose_name="Почта")
    firstname = models.CharField(max_length=255, verbose_name="Имя")
    lastname = models.CharField(max_length=255, verbose_name="Фамилия")
    surname = models.CharField(max_length=255, verbose_name="Отчество")
    snils = models.CharField(max_length=11, validators=[MinLengthValidator(11)], verbose_name="Страховой пенсионный номер")

    is_active = models.BooleanField(default=True, verbose_name="Активный")
    is_staff = models.BooleanField(default=False, verbose_name="Администратор")

    objects = EmployeeUserManager()

    USERNAME_FIELD = "email" # авторизация по почте
    REQUIRED_FIELDS = ["firstname", "lastname", ]

    def get_full_name(self):
        return f"{self.lastname} {self.firstname} {self.surname}"
    
    def __str__(self):
        return self.email
