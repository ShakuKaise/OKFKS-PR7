from django.contrib import admin, messages
from django.http import HttpResponse
import csv
from django.utils.translation import gettext_lazy as _

from .models import (Language, Publisher, Genre, Author, Book, User, Request)

class BaseAdmin(admin.ModelAdmin):
    actions = ['export_to_csv', 'delete_multiple', 'restore_multiple']
    def get_actions(self, request):
        actions = super().get_actions(request)
        if hasattr(self.model, 'is_deleted'):
            return actions
        else:
            # Создаем кортеж для delete_selected, чтобы удовлетворить ожидания метода get_actions()
            delete_selected_tuple = (
            admin.actions.delete_selected, 'delete_selected', _('Удалить выбранные %(verbose_name_plural)s'))
            return {
                'export_to_csv': (self.export_to_csv, 'export_to_csv', _("Экспортировать в CSV")),
                'delete_selected': delete_selected_tuple,
            }

    def delete_multiple(self, request, queryset):
        queryset.update(is_deleted=True)
        self.message_user(request, _("Выбранные элементы успешно помечены как удалённые."), messages.SUCCESS)

    def restore_multiple(self, request, queryset):
        queryset.update(is_deleted=False)
        self.message_user(request, _("Выбранные элементы успешно восстановлены."), messages.SUCCESS)

    def export_to_csv(self, request, queryset):
        opts = self.model._meta
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{opts.verbose_name_plural}.csv"'
        writer = csv.writer(response)

        # Добавляем заголовки
        field_names = [field.verbose_name for field in opts.fields]
        writer.writerow(field_names)

        # Добавляем данные
        for obj in queryset:
            row = [getattr(obj, field.name) for field in opts.fields]
            writer.writerow(row)

        return response

    export_to_csv.short_description = "Экспортировать в CSV"

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'chars_code', 'is_deleted')
    ordering = ('name', 'chars_code', 'is_deleted')
    verbose_name = _("Язык")
    verbose_name_plural = _("Языки")

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'is_deleted')
    ordering = ('name', 'address', 'is_deleted')
    verbose_name = _("Издатель")
    verbose_name_plural = _("Издатели")

@admin.register(Genre)
class GenreAdmin(BaseAdmin):
    list_display = ('name', 'is_deleted')
    ordering = ('name', 'is_deleted')
    verbose_name = _("Жанр")
    verbose_name_plural = _("Жанры")

@admin.register(Author)
class AuthorAdmin(BaseAdmin):
    list_display = ('first_name', 'last_name', 'is_deleted')
    ordering = ('first_name', 'last_name', 'is_deleted')
    verbose_name = _("Автор")
    verbose_name_plural = _("Авторы")

@admin.register(Book)
class BookAdmin(BaseAdmin):
    list_display = ('name', 'publication_year', 'language', 'is_deleted', 'cover_url')
    ordering = ('name', 'publication_year', 'language', 'is_deleted', 'cover_url')
    verbose_name = _("Книга")
    verbose_name_plural = _("Книги")

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'borrow_date', 'return_date', 'book', 'status')
    ordering = ('user', 'borrow_date', 'return_date', 'book', 'status')
    verbose_name = _("Запрос")
    verbose_name_plural = _("Запросы")

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    ordering = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    verbose_name = _("Пользователь")
    verbose_name_plural = _("Пользователи")
