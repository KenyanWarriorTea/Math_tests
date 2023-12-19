from django.contrib import admin
from django.contrib import admin
from .models import MathTopic
from django.contrib import admin
from .models import Test, Question, Answer

# Register your models here.


@admin.register(MathTopic)
class MathTopicAdmin(admin.ModelAdmin):
    pass


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['title']
    # Другие настройки админ-панели для Test


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'test']
    # Другие настройки админ-панели для Question


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['text', 'question', 'is_correct']
    # Другие настройки админ-панели для Answer