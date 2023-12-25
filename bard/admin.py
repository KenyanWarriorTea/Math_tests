from django.contrib import admin
from .models import MathTopic
from django.contrib import admin
from .models import Test, Question, Answer
from nested_admin import NestedStackedInline, NestedModelAdmin
# Register your models here.


class AnswerInline(NestedStackedInline):
    model = Answer
    extra = 1  # Количество форм для новых ответов

class QuestionInline(NestedStackedInline):
    model = Question
    extra = 1  # Количество форм для новых вопросов
    inlines = [AnswerInline]

@admin.register(Test)
class TestAdmin(NestedModelAdmin):
    list_display = ['title']
    inlines = [QuestionInline]
    # Другие настройки админ-панели для Test


@admin.register(MathTopic)
class MathTopicAdmin(admin.ModelAdmin):
    pass

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'test', 'math_topic']
    inlines = [AnswerInline]

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['text', 'question', 'is_correct']
    # Другие настройки админ-панели для Answer