from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CASCADE

from apps.shared.models import AbstractModel


class User(AbstractUser):
    avatar = models.ImageField(upload_to="users/avatar/%Y/%m/%d", default="default/default_user.jpg")
    middle_name = models.CharField(max_length=56)


class Bookshelf(AbstractModel):
    name = models.CharField(max_length=128)
    user = models.ForeignKey("users.User", CASCADE)
    books = models.ManyToManyField("books.Book",related_name='bookshelves')
