from django.urls import path
from apps.books.views import BookListView, BookDetailView, AuthorListView, AuthorDetailView, GenreListView, \
    GenreDetailView, AddReviewView, AuthorCreateView, AuthorUpdateView, BookCreateView, BookUpdateView

app_name = 'books'
urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('create', BookCreateView.as_view(), name='book_create'),
    path('authors/', AuthorListView.as_view(), name='author_list'),
    path('genres/', GenreListView.as_view(), name='genre_list'),
    path('authors/create', AuthorCreateView.as_view(), name="author_create"),

    path('<slug:slug>/', BookDetailView.as_view(), name='book_detail'),
    path('<slug:slug>/update/', BookUpdateView.as_view(), name='book_update'),
    path('authors/<int:pk>', AuthorDetailView.as_view(), name='author_detail'),
    path('authors/<int:pk>/update', AuthorUpdateView.as_view(), name='author_update'),
    path('genres/<str:name>/', GenreDetailView.as_view(), name='genre_detail'),
    path('<int:pk>', AddReviewView.as_view(), name="add_review")
]
