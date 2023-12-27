from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    status = models.CharField(max_length=100)
    def __str__(self):
        return f"Профиль пользователя {self.user.username}: ФИО - {self.full_name}, Статус - {self.status}"


class Test(models.Model):
    title = models.CharField(max_length=200)
    # что то там


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


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    # Остальные поля...


class Women(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категории")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Известные женщины'
        verbose_name_plural = 'Известные женщины'
        ordering = ['id']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']
