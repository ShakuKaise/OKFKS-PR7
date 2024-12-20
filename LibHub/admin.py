from django.contrib import admin, messages
from django.http import HttpResponse
import csv
from django.utils.translation import gettext_lazy as _

from .models import (Language, Publisher, Genre, Author, Book, User,
                     Comment, Evaluation, Request)

class BaseAdmin(admin.ModelAdmin):
    actions = ['export_to_csv', 'delete_multiple', 'restore_multiple']
    def get_actions(self, request):
        actions = super().get_actions(request)
        if hasattr(self.model, 'is_deleted'):
            return actions
        else:
            # Создаем кортеж для delete_selected, чтобы удовлетворить ожидания метода get_actions()
            delete_selected_tuple = (
            admin.actions.delete_selected, 'delete_selected', _('Delete selected %(verbose_name_plural)s'))
            return {
                'export_to_csv': (self.export_to_csv, 'export_to_csv', _("Export to CSV")),
                'delete_selected': delete_selected_tuple,
            }

    def delete_multiple(self, request, queryset):
        queryset.update(is_deleted=True)
        self.message_user(request, _("Selected objects successfully marked as deleted."), messages.SUCCESS)

    def restore_multiple(self, request, queryset):
        queryset.update(is_deleted=False)
        self.message_user(request, _("Selected objects successfully restored."), messages.SUCCESS)

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

    export_to_csv.short_description = "Export to CSV"

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'chars_code', 'is_deleted')

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'is_deleted')

@admin.register(Genre)
class GenreAdmin(BaseAdmin):
    list_display = ('name', 'is_deleted')

@admin.register(Author)
class AuthorAdmin(BaseAdmin):
    list_display = ('first_name', 'last_name', 'is_deleted')

@admin.register(Book)
class BookAdmin(BaseAdmin):
    list_display = ('name', 'publication_year', 'language', 'is_deleted', 'cover_url', 'quantity')

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'borrow_date', 'return_date', 'book', 'status')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'text', 'is_deleted')

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'evaluation', 'is_deleted')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
