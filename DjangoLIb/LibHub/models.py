from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.contrib.auth.password_validation import validate_password
from django.db import models

# Менеджер пользователя
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Необходимо указать email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        validate_password(password, user)  # Validate password
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


# Пользовательская модель пользователя
class User(AbstractBaseUser, PermissionsMixin):
    password = models.CharField(max_length=128, validators=[validate_password, MinLengthValidator(6)])  # Apply password validation
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True, null=True,
                                  validators=[MinLengthValidator(2), MaxLengthValidator(20),
                                              RegexValidator(regex=r'^[a-zA-Zа-яА-Я\s]*$', message="Имя может содержать только буквы и пробелы.")])
    last_name = models.CharField(max_length=150, blank=True, null=True,
                                 validators=[MinLengthValidator(2), MaxLengthValidator(20),
                                             RegexValidator(regex=r'^[a-zA-Zа-яА-Я\s]*$', message="Фамилия может содержать только буквы и пробелы.")])

    def clean(self):
        if self.first_name and not self.first_name.strip():
            raise ValidationError("Имя не может быть пустым или содержать только пробелы.")
        if self.last_name and not self.last_name.strip():
            raise ValidationError("Фамилия не может быть пустой или содержать только пробелы.")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set_permissions', blank=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return self.email


# Модель языка
class Language(models.Model):
    name = models.CharField(max_length=30, unique=True,
                            validators=[MinLengthValidator(3), MaxLengthValidator(20),
                                        RegexValidator(regex=r'^[a-zA-Zа-яА-Я\s]*$', message="Название языка может содержать только буквы.")])
    chars_code = models.CharField(max_length=5, unique=True,
                                  validators=[MinLengthValidator(2), MaxLengthValidator(5),
                                              RegexValidator(regex=r'^[A-Z]*$', message="Код языка может содержать только заглавные буквы.")])

    def clean(self):
        if not self.name.strip():
            raise ValidationError("Название языка не может быть пустым или содержать только пробелы.")
        if not self.chars_code.strip():
            raise ValidationError("Код языка не может быть пустым или содержать только пробелы.")

    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# Модель издателя
class Publisher(models.Model):
    name = models.CharField(max_length=30, unique=True,
                            validators=[MinLengthValidator(2), MaxLengthValidator(20),
                                        RegexValidator(regex=r'^[a-zA-Zа-яА-Я\s]*$', message="Название издательства может содержать только буквы и пробелы.")])
    address = models.CharField(max_length=100,
                               validators=[MinLengthValidator(5), MaxLengthValidator(100),
                                           RegexValidator(regex=r'^[a-zA-Zа-яА-Я0-9\s,.-]*$', message="Адрес издательства может содержать только буквы, цифры и знаки препинания.")])

    def clean(self):
        if not self.name.strip():
            raise ValidationError("Название издательства не может быть пустым или содержать только пробелы.")
        if not self.address.strip():
            raise ValidationError("Адрес издательства не может быть пустым или содержать только пробелы.")

    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# Модель жанра
class Genre(models.Model):
    name = models.CharField(max_length=30, unique=True,
                            validators=[MinLengthValidator(2), MaxLengthValidator(30),
                                        RegexValidator(regex=r'^[a-zA-Zа-яА-Я\s]*$', message="Название жанра может содержать только буквы.")])
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# Модель автора
class Author(models.Model):
    first_name = models.CharField(max_length=30,
                                  validators=[MinLengthValidator(2), MaxLengthValidator(20),
                                              RegexValidator(regex=r'^[a-zA-Zа-яА-Я\s]*$', message="Имя автора может содержать только буквы и пробелы.")])
    last_name = models.CharField(max_length=30,
                                 validators=[MinLengthValidator(2), MaxLengthValidator(20),
                                             RegexValidator(regex=r'^[a-zA-Zа-яА-Я\s]*$', message="Фамилия автора может содержать только буквы и пробелы.")])
    middle_name = models.CharField(max_length=30, blank=True, null=True,
                                   validators=[MinLengthValidator(1), MaxLengthValidator(20),
                                               RegexValidator(regex=r'^[a-zA-Zа-яА-Я\s]*$', message="Отчество автора может содержать только буквы и пробелы.")])

    def clean(self):
        if not self.first_name.strip():
            raise ValidationError("Имя автора не может быть пустым или содержать только пробелы.")
        if not self.last_name.strip():
            raise ValidationError("Фамилия автора не может быть пустой или содержать только пробелы.")
        if self.middle_name and not self.middle_name.strip():
            raise ValidationError("Отчество автора не может содержать только пробелы.")

    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Модель книги
class Book(models.Model):
    name = models.CharField(max_length=255,
                            validators=[MinLengthValidator(3), MaxLengthValidator(255),
                                        RegexValidator(regex=r'^[a-zA-Zа-яА-Я0-9\s]*$', message="Название книги может содержать только буквы, цифры и пробелы.")])
    publication_year = models.IntegerField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    cover_url = models.URLField()

    def clean(self):
        if not self.name.strip():
            raise ValidationError("Название книги не может быть пустым или содержать только пробелы.")
        if self.publication_year <= 0:
            raise ValidationError("Год публикации должен быть положительным числом.")
        if not self.cover_url.strip():
            raise ValidationError("URL обложки книги не может быть пустым или содержать только пробелы.")

    is_deleted = models.BooleanField(default=False)
    publishers = models.ManyToManyField(Publisher, blank=True)
    genres = models.ManyToManyField(Genre, blank=True)
    authors = models.ManyToManyField(Author, blank=True)

    def __str__(self):
        return self.name


# Модель запроса
class Request(models.Model):
    class RequestStatus(models.TextChoices):
        RENTED = 'RENTED'
        EXPIRED = 'EXPIRED'
        RETURNED = 'RETURNED'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    borrow_date = models.DateField()
    return_date = models.DateField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=RequestStatus.choices,
                              validators=[MinLengthValidator(3), MaxLengthValidator(8)])

    def clean(self):
        if self.return_date and self.return_date < self.borrow_date:
            raise ValidationError("Дата возврата не может быть раньше даты выдачи.")

    def __str__(self):
        return f"Request #{self.id} - {self.user} - {self.book} - {self.status}"
