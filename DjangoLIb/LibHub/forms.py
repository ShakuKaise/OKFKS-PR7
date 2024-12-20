from django import forms
from .models import User, Language, Publisher, Genre, Author, Book, Request
from django.contrib.auth.forms import AuthenticationForm

class FileUploadForm(forms.Form):
    file = forms.FileField(label="Загрузите файл для импорта")

class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш пароль'})
    )

    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name', 'password'
        ]
        labels = {
            'email': 'Электронная почта',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'password': 'Пароль',
        }

class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['name', 'chars_code', 'is_deleted']
        labels = {
            'name': 'Название',
            'chars_code': 'Символьный Код',
            'is_deleted': 'Удалено',
        }


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ['name', 'address', 'is_deleted']
        labels = {
            'name': 'Название',
            'address': 'Адрес',
            'is_deleted': 'Удалено',
        }


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name', 'is_deleted']
        labels = {
            'name': 'Название',
            'is_deleted': 'Удалено',
        }


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'middle_name', 'is_deleted']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'middle_name': 'Отчество',
            'is_deleted': 'Удалено',
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'name', 'publication_year', 'language', 'cover_url',
            'is_deleted', 'publishers', 'genres', 'authors'
        ]
        labels = {
            'name': 'Название',
            'publication_year': 'Год публикации',
            'language': 'Язык',
            'cover_url': 'Ссылка на обложку',
            'is_deleted': 'Удалено',
            'publishers': 'Издатели',
            'genres': 'Жанры',
            'authors': 'Авторы',
        }


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['user', 'borrow_date', 'return_date', 'book', 'status']
        labels = {
            'user': 'Пользователь',
            'borrow_date': 'Дата выдачи',
            'return_date': 'Дата возврата',
            'book': 'Книга',
            'status': 'Статус',
        }


class AuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваше имя пользователя'}),
    )
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш пароль'}),
    )


class BookFilterForm(forms.Form):
    category = forms.ModelChoiceField(
        label='Категория',
        queryset=Genre.objects.all(),
        required=False,
        empty_label='Все категории',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    author = forms.ModelChoiceField(
        label='Автор',
        queryset=Author.objects.all(),
        required=False,
        empty_label='Все авторы',
        widget=forms.Select(attrs={'class': 'form-control'})
    )