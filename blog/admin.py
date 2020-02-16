from django.contrib import admin

from .models import Post
from .models import employees

admin.site.register(Post)
admin.site.register(employees)
