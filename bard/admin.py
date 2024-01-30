from django.contrib import admin
from django.contrib.auth.models import User

from .models import MathTopic
from django.contrib import admin
from .models import Test, Question, Answer
from nested_admin import NestedStackedInline, NestedModelAdmin
# Register your models here.
from django import forms

from django.contrib import admin
from .models import Classroom
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile

# Unregister the original User admin
admin.site.unregister(User)

class CustomUserAdmin(UserAdmin):
    # Add an additional list_display field
    list_display = UserAdmin.list_display + ('user_status',)

    def user_status(self, obj):
        # Get the user's status from UserProfile
        profile = UserProfile.objects.filter(user=obj).first()
        return profile.status if profile else 'Unknown'
    user_status.short_description = 'Status'

# Register the custom admin class with the User model
admin.site.register(User, CustomUserAdmin)
# Optional: If you want to customize the admin interface for Classroom
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher')  # Fields to display in the admin list view
    search_fields = ('name',)  # Fields to be searched in the admin
    list_filter = ('teacher',)  # Filters to be applied in the admin

    # This function is useful if you want to customize how the many-to-many field is displayed
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "students":
            kwargs["queryset"] = User.objects.filter(is_staff=False)  # Example: Filter to non-staff users
        return super().formfield_for_manytomany(db_field, request, **kwargs)

# Register your models here.
admin.site.register(Classroom, ClassroomAdmin)
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
    list_display = ['title']



class QuestionAdminForm(forms.ModelForm):
    test = forms.ModelChoiceField(queryset=Test.objects.all(), label="Test", required=False,
                                  widget=forms.Select(), empty_label="Select Test")
    math_topic = forms.ModelChoiceField(queryset=MathTopic.objects.all(), label="Math Topic", required=False,
                                        widget=forms.Select(), empty_label="Select Math Topic")

    class Meta:
        model = Question
        fields = '__all__'

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm
    list_display = ('text', 'get_test_title')
    inlines = [AnswerInline]
    fields = ('test', 'text')
    def get_test_title(self, obj):
        return obj.test.title if obj.test else 'No test'

    def get_math_topic_title(self, obj):
        return obj.math_topic.title if obj.math_topic else 'No math topic'
    get_test_title.short_description = 'Test Title'
    get_math_topic_title.short_description = 'Math Topic Title'



@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['text', 'question', 'is_correct']
    # Другие настройки админ-панели для Answer

