from django.contrib import admin
from apps.users.models import User, Bookshelf

admin.site.register([User, Bookshelf])
