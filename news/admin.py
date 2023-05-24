from django.contrib import admin
from .models import *

admin.sites.register(Post)
admin.sites.register(Author)
admin.sites.register(Category)
admin.sites.register(Post)
admin.sites.register(Comment)