from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from LibHub import views as v
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

# Router definitions
routerUser = routers.DefaultRouter()
routerUser.register('users', v.UserViewSet, basename='user')

routerBook = routers.DefaultRouter()
routerBook.register('books', v.BookViewSet, basename='book')

routerRequest = routers.DefaultRouter()
routerRequest.register('requests', v.RequestViewSet, basename='request')

routerGenre = routers.DefaultRouter()
routerGenre.register('genres', v.GenreViewSet, basename='genre')

routerAuthor = routers.DefaultRouter()
routerAuthor.register('authors', v.AuthorViewSet, basename='author')

routerLanguage = routers.DefaultRouter()
routerLanguage.register('languages', v.LanguageViewSet, basename='language')

routerPublisher = routers.DefaultRouter()
routerPublisher.register('publishers', v.PublisherViewSet, basename='publisher')

api_patterns = [
    path('', include(routerUser.urls)),
    path('', include(routerBook.urls)),
    path('', include(routerAuthor.urls)),
    path('', include(routerLanguage.urls)),
    path('', include(routerGenre.urls)),
    path('', include(routerRequest.urls)),
    path('', include(routerPublisher.urls)),
    # path('', include(routerComment.urls)),
    # path('', include(routerEvaluation.urls)),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]


language_patterns = [
    path('create/', v.LanguageCreateView.as_view(), name='language_create'),
    path('<int:pk>/update/', v.LanguageUpdateView.as_view(), name='language_update'),
    path('<int:pk>/delete/', v.LanguageDeleteView.as_view(), name='language_delete'),
    path('', v.LanguagesList.as_view(), name='languages'),
]

publisher_patterns = [
    path('create/', v.PublisherCreateView.as_view(), name='publisher_create'),
    path('<int:pk>/update/', v.PublisherUpdateView.as_view(), name='publisher_update'),
    path('<int:pk>/delete/', v.PublisherDeleteView.as_view(), name='publisher_delete'),
    path('', v.PublishersList.as_view(), name='publishers'),
]

request_patterns = [
    path('create/', v.RequestCreateView.as_view(), name='request_create'),
    path('<int:pk>/update/', v.RequestUpdateView.as_view(), name='request_update'),
    path('<int:pk>/delete/', v.RequestDeleteView.as_view(), name='request_delete'),
    path('', v.RequestsList.as_view(), name='requests'),
]

author_patterns = [
    path('create/', v.AuthorCreateView.as_view(), name='author_create'),
    path('<int:pk>/update/', v.AuthorUpdateView.as_view(), name='author_update'),
    path('<int:pk>/delete/', v.AuthorDeleteView.as_view(), name='author_delete'),
    path('', v.AuthorsList.as_view(), name='authors'),
]

genre_patterns = [
    path('create/', v.GenreCreateView.as_view(), name='genre_create'),
    path('<int:pk>/update/', v.GenreUpdateView.as_view(), name='genre_update'),
    path('<int:pk>/delete/', v.GenreDeleteView.as_view(), name='genre_delete'),
    path('', v.GenresList.as_view(), name='genres'),
]

books_patterns = [
    path('addBook/', v.BookCreateView.as_view(), name='add_book'),
    path('<int:pk>/update/', v.BookUpdateView.as_view(), name='book_update'),
    path('<int:pk>/delete/', v.BookDeleteView.as_view(), name='book_delete'),
    path('export-books/', v.export_books_to_excel, name='export_books'),
    path('rent/<int:book_id>/', v.rent_book, name='rent_book'),
    path('return/<int:book_id>/', v.return_book, name='return_book'),
    path('', v.book_list, name='book_list'),
]

account_patterns = [
    path('', v.profile, name="profile"),
    path('logout/', v.logout_view, name='logout'),
]
urlpatterns = [
    path('genres/', include(genre_patterns)),
    path('authors/', include(author_patterns)),
    path('admin/', admin.site.urls),
    path('home/', v.home_view, name='home'),
    path('books/', include(books_patterns)),
    path('profile/', include(account_patterns)),
    path('languages/', include(language_patterns)),
    path('publisher/', include(publisher_patterns)),
    path('requests/', include(request_patterns)),
    path('api/', include(api_patterns)),
    path('login/', v.CustomLoginView.as_view(), name='login'),
    path('register/', v.RegisterView.as_view(), name='registration'),

    path('db/backup/', v.backup_database, name='backup_database'),

    path('restore/', v.restore_database, name='restore_database'),
    path('db/upload/', v.upload_file_view, name='upload_file'),
    path('db/getBooksInfo', v.rented_books_statistics, name="rented_books_statistics")
]