from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import CASCADE
from django.urls import reverse

from apps.shared.models import AbstractModel


class LanguageChoice(models.TextChoices):
    UZBEK = "UZ", "O'zbekcha"
    ARABIC = "AR", "Arabic"
    ENGLISH = "EN", "English"
    FRENCH = "FR", "French"
    RUSSIAN = "RU", "Russian"


class Book(AbstractModel):
    title = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    published = models.DateField()
    isbn = models.CharField(unique=True, max_length=128)
    language = models.CharField(max_length=14, choices=LanguageChoice.choices)
    page = models.IntegerField()
    cover = models.ImageField(upload_to="books/cover/%Y/%m/%d", default="default/default_user.jpg", blank=True)
    genre = models.ManyToManyField("books.BookGenre", related_name="books")
    authors = models.ManyToManyField("books.Author", related_name="books")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("books:book_detail", kwargs={"slug": self.slug})


class Author(AbstractModel):
    first_name = models.CharField(max_length=56)
    last_name = models.CharField(max_length=56)
    birth_date = models.DateField()
    birth_place = models.CharField(max_length=56)
    website = models.URLField()
    avatar = models.ImageField(upload_to="authors/avatar/%Y/%m/%d")
    about = models.TextField()

    def __str__(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse("books:author_detail", kwargs={"pk": self.id})


class BookGenre(AbstractModel):
    name = models.CharField(max_length=28)
    description = models.TextField()

    def __str__(self):
        return self.name


class BookReview(AbstractModel):
    book = models.ForeignKey("books.Book", CASCADE, "reviews")
    user = models.ForeignKey("users.User", CASCADE, "reviews")
    body = models.TextField()
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    like_count = models.IntegerField(default=0)
