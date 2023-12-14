from django.contrib import admin
from django.contrib import admin
from .models import MathTopic


# Register your models here.
@admin.register(MathTopic)
class MathTopicAdmin(admin.ModelAdmin):
    pass
