from django import forms
from .models import Role, User, Language, Publisher, Genre, Author, Book, Request, Comment, Evaluation
from django.contrib.auth.forms import AuthenticationForm

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name', 'description']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name', 'role',
            'is_active'
        ]


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['name', 'chars_code', 'is_deleted']


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ['name', 'address', 'is_deleted']


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name', 'is_deleted']


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'middle_name', 'is_deleted']


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'name', 'publication_year', 'language', 'cover_url',
            'quantity', 'is_deleted', 'publishers', 'genres', 'authors'
        ]


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['user', 'borrow_date', 'return_date', 'book', 'status']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'book', 'text', 'is_deleted']


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['user', 'book', 'evaluation', 'is_deleted']


class AuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
    )


class BookFilterForm(forms.Form):
    category = forms.ModelChoiceField(
        label='Жанры',
        queryset=Genre.objects.all(),
        required=False,
        empty_label='Все жанры',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    author = forms.ModelChoiceField(
        label='Авторы',
        queryset=Author.objects.all(),
        required=False,
        empty_label='Все авторы',
        widget=forms.Select(attrs={'class': 'form-control'})
    )