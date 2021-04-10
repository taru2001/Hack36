from django.contrib import admin

# Register your models here.

from .models import Course,Video,subscription

admin.site.register(Course)
admin.site.register(Video)
admin.site.register(subscription)
