from django.contrib import admin
from apps.books.models import Book, Author, BookGenre, BookReview

admin.site.register([Author, BookReview, BookGenre])


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ["title"]
    }
