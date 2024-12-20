import os
import django

# Указание пути к настройкам Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'LibHub.settings'

# Если необходимо, инициализируем Django

django.setup()

from LibHub.models import (
    User, Language, Publisher, Genre, Author, Book, Request
)

from datetime import datetime, timedelta
from random import choice, randint, sample
# Заполнение моделей тестовыми данными
def populate_data():
    # 2. User
    # Удаление всех существующих записей пользователей с почтой user{n}@example.com, где n от 1 до 6
    email_pattern_qs = User.objects.filter(email__regex=r'^user[0-6]@example\.com$')
    for user in email_pattern_qs:
        user.delete()

    users = [
        {"email": f"user{n}@example.com",
         "first_name": f"FirstName{n}",
         "last_name": f"LastName{n}",
         "is_active": True,
         "is_staff": False if n % 2 == 0 else True}
        for n in range(1, 6)
    ]
    user_objects = [User.objects.create(**user) for user in users]

    # 3. Language
    languages = [
        {"name": lang, "chars_code": lang[:2], "is_deleted": False}
        for lang in ["English", "Spanish", "French", "German", "Russian"]
    ]
    language_objects = [Language.objects.create(**language) for language in languages]

    # 4. Publisher
    publishers = [
        {"name": f"Publisher{n}", "address": f"Address{n}", "is_deleted": False}
        for n in range(1, 6)
    ]
    publisher_objects = [Publisher.objects.create(**publisher) for publisher in publishers]

    # 5. Genre
    genres = [
        {"name": f"Genre{n}", "is_deleted": False}
        for n in range(1, 6)
    ]
    genre_objects = [Genre.objects.create(**genre) for genre in genres]

    # 6. Author
    authors = [
        {"first_name": f"AuthorFirstName{n}",
         "last_name": f"AuthorLastName{n}",
         "middle_name": f"AuthorMiddleName{n}",
         "is_deleted": False}
        for n in range(1, 6)
    ]
    author_objects = [Author.objects.create(**author) for author in authors]

    # 7. Book
    books = [
        {
            "name": f"Book{n}",
            "publication_year": randint(2000, 2023),
            "language": choice(language_objects),
            "cover_url": f"http://example.com/cover{n}.jpg",
            "is_deleted": False,
            "publishers": sample(publisher_objects, k=2),
            "genres": sample(genre_objects, k=2),
            "authors": sample(author_objects, k=2),
        }
        for n in range(1, 6)
    ]
    book_objects = []
    for book in books:
        publishers = book.pop("publishers")
        genres = book.pop("genres")
        authors = book.pop("authors")
        book_obj = Book.objects.create(**book)
        book_obj.publishers.set(publishers)
        book_obj.genres.set(genres)
        book_obj.authors.set(authors)
        book_objects.append(book_obj)

    # 8. Request
    requests = [
        {
            "user": choice(user_objects),
            "borrow_date": datetime.now() - timedelta(days=randint(1, 30)),
            "return_date": datetime.now() + timedelta(days=randint(1, 30)),
            "book": choice(book_objects),
            "status": choice(["RENTED", "EXPIRED", "RETURNED"])
        }
        for _ in range(5)
    ]
    request_objects = [Request.objects.create(**request) for request in requests]

    print("Тестовые данные успешно добавлены.")


# Запуск функции заполнения
populate_data()