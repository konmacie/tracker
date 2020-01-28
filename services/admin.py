from django.contrib import admin
from services.models import Service, Post, ScraperRunLog


admin.site.register(Service)
admin.site.register(Post)
admin.site.register(ScraperRunLog)
