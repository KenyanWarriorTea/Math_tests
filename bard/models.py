import random

from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import uuid

from django.db import models
from django.contrib.auth.models import User


class Classroom(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Globally unique name
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    students = models.ManyToManyField(User, related_name='classrooms', blank=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    status = models.CharField(max_length=100)
    classrooms = models.ManyToManyField(Classroom, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Test(models.Model):
    title = models.CharField(max_length=200)
    # что то там


class ClassroomJoinRequest(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)  # Принят или нет запрос
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Запрос от {self.student.username} в класс {self.classroom.name}"
class UserTestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.IntegerField()
    percentage = models.DecimalField(max_digits=5, decimal_places=2)  # Поле для хранения процентов

    def calculate_percentage(self):
        total_questions = self.test.question_set.count()
        if total_questions > 0:
            correct_answers = self.score
            percentage = (correct_answers / total_questions) * 100
            return round(percentage, 2)
        else:
            return 0.00

    def save(self, *args, **kwargs):
        self.percentage = self.calculate_percentage()
        super().save(*args, **kwargs)


class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    best_score = models.IntegerField(default=0)

    def __str__(self):
        return f"Результат теста {self.test.title} для пользователя {self.user.username}: Последний балл - {self.score}, Лучший балл - {self.best_score}"






class MathTopic(models.Model):
    title = models.CharField(max_length=100)
    description = RichTextField()

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    text = models.TextField()
    math_topic = models.ForeignKey(MathTopic, on_delete=models.SET_NULL, null=True, blank=True)
    # Остальные поля...

class Language(models.Model):
    code = models.CharField(max_length=10, unique=True)  # Например, 'ru' или 'kz'

    def __str__(self):
        return self.code

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    # Остальные поля...


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

class ConfirmationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)

    @staticmethod
    def generate_code():
        return str(random.randint(100000, 999999))  # Generates a six-digit code

    def __str__(self):
        return f"Code for {self.user.username}: {self.code}"