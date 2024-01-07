from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView
from .mixin import UnauthenticatedUserMixin
from .forms import *
from .utils import *
from django.shortcuts import get_object_or_404
from .models import TestResult, Test
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView
import random
from .models import MathTopic
from .forms import RegisterUserForm
from django.db import IntegrityError
from .forms import ClassroomForm
from .models import Classroom
from django.shortcuts import render
from .models import UserProfile
from django.contrib.auth.decorators import login_required


def math_topic_details(request, topic_id):
    topic = MathTopic.objects.get(pk=topic_id)
    test_id = ...
    context = {
        'topic': topic,
        'your_test_id': test_id
    }
    return render(request, 'topic_details.html', {'topic': topic})


def test_results(request, test_id):
    test = Test.objects.get(id=test_id)
    user = request.user
    user_test_result = TestResult.objects.filter(user=user, test=test).first()

    context = {
        'test': test,
        'user_test_result': user_test_result,
    }
    return render(request, 'test_results.html', context)


@login_required
def create_classroom(request):
    if request.method == 'POST':
        form = ClassroomForm(request.POST)
        if form.is_valid():
            try:
                classroom = form.save(commit=False)
                classroom.teacher = request.user
                classroom.save()

                # Add classroom to user's profile
                user_profile, created = UserProfile.objects.get_or_create(user=request.user)
                user_profile.classrooms.add(classroom)

                return redirect('profile')
            except IntegrityError:
                # Handle the unique constraint error
                messages.error(request, "A classroom with this name already exists.")
    else:
        form = ClassroomForm()

    return render(request, 'create_classroom.html', {'form': form})


def test_view(request, test_id):
    test = get_object_or_404(Test, pk=test_id)

    if 'questions_order' not in request.session:
        questions = list(Question.objects.filter(test=test))
        random.shuffle(questions)
        questions = questions[:30]
        request.session['questions_order'] = [q.id for q in questions]
    else:
        questions_ids = request.session['questions_order']
        questions = [Question.objects.get(id=qid) for qid in questions_ids]

    # Загрузка сохраненных ответов
    saved_answers = {key.split('_')[1]: request.session[key] for key in request.session.keys() if key.startswith('answer_')}

    context = {'test': test, 'questions': questions, 'saved_answers': saved_answers}
    return render(request, 'test.html', context)

@login_required
def profile(request):
    user = request.user
    tests = Test.objects.all()

    try:
        user_profile = UserProfile.objects.get(user=user)
        full_name = user_profile.full_name
        status = user_profile.status

        # If the user is a student, fetch the classrooms they are part of with teacher's full name
        if status == "student":
            classrooms = Classroom.objects.filter(students=user).select_related('teacher')
            classrooms = [
                {
                    'name': classroom.name,
                    'teacher_full_name': UserProfile.objects.get(user=classroom.teacher).full_name
                } for classroom in classrooms
            ]
        else:
            classrooms = user_profile.classrooms.all()  # For teachers

    except UserProfile.DoesNotExist:
        full_name = ""
        status = ""
        classrooms = []

    test_results = {test: TestResult.objects.filter(user=user, test=test).first() for test in tests}

    context = {
        'user': user,
        'tests': tests,
        'test_results': test_results,
        'full_name': full_name,
        'status': status,
        'classrooms': classrooms,
    }

    return render(request, 'profile.html', context)

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
class Home(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # You can add more context variables if needed
        return context

class Home2(TemplateView):
    template_name = 'base2.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # You can add more context variables if needed
        return context


class RegisterUserView(UnauthenticatedUserMixin, View):
    def get(self, request, *args, **kwargs):
        form = RegisterUserForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            # Сохранение данных формы в сессии
            request.session['registration_data'] = form.cleaned_data

            # Генерация кода подтверждения
            confirmation_code = random.randint(100000, 999999)
            request.session['confirmation_code'] = confirmation_code

            # Отправка кода на почту пользователя
            send_mail(
                'Код подтверждения',
                f'Ваш код подтверждения: {confirmation_code}',
                'asllsackl@gmail.com',
                [form.cleaned_data['email']],
                fail_silently=False,
            )
            return redirect('email_confirmation')
        return render(request, 'register.html', {'form': form})

class EmailConfirmationView(UnauthenticatedUserMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'email_confirmation.html')

    def post(self, request, *args, **kwargs):
        user_code = request.POST.get('code')
        if user_code == str(request.session.get('confirmation_code')):
            # Создание пользователя
            registration_data = request.session.get('registration_data')
            user = User.objects.create_user(
                username=registration_data['username'],
                email=registration_data['email'],
                password=registration_data['password1'],
                # Добавьте другие поля, если необходимо
            )
            UserProfile.objects.create(user=user, full_name=registration_data['full_name'], status=registration_data['status'])
            # Очистка сессии
            del request.session['registration_data']
            del request.session['confirmation_code']
            login(self.request, user)
            return redirect('home')
        else:
            # Обработка ошибки ввода кода
            return render(request, 'email_confirmation.html', {'error': 'Неверный код подтверждения'})
class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация / Авторландыру")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')




@login_required
def classroom_detail(request, classroom_id):
    classroom = get_object_or_404(Classroom, id=classroom_id)

    if request.user != classroom.teacher:
        return redirect('home')  # Redirect if not the teacher of the classroom

    students = classroom.students.all()
    form = AddStudentForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            student_identifier = form.cleaned_data['username_or_email']

            # Determine if the identifier is an email or username
            try:
                if '@' in student_identifier:
                    student = User.objects.get(email=student_identifier)
                else:
                    student = User.objects.get(username=student_identifier)

                # Rest of your logic
                if student == classroom.teacher:
                    messages.error(request, 'Вы не можете добавить учителя в класс.')
                elif student in students:
                    messages.error(request, 'Этот студент уже добавлен.')
                else:
                    ClassroomJoinRequest.objects.create(classroom=classroom, student=student)
                    messages.success(request, 'Запрос отправлен студенту.')

            except User.DoesNotExist:
                messages.error(request, 'Пользователь с таким идентификатором не найден.')
        else:
            messages.error(request, 'Ошибка в форме.')

    context = {
        'classroom': classroom,
        'students': students,
        'form': form
    }

    return render(request, 'classroom_detail.html', context)

@login_required
def manage_join_requests(request):
    join_requests = ClassroomJoinRequest.objects.filter(student=request.user, is_accepted=False)
    return render(request, 'manage_join_requests.html', {'join_requests': join_requests})


def set_language_to_russian(request):
    request.session['language'] = 'russian'
    return redirect('home')


def set_language_to_kazakh(request):
    request.session['language'] = 'kazakh'
    return redirect('home2')

@login_required
def accept_join_request(request, join_request_id):
    join_request = get_object_or_404(ClassroomJoinRequest, id=join_request_id, student=request.user)

    if request.method == 'POST':
        if 'accept' in request.POST:
            join_request.is_accepted = True
            join_request.save()
            join_request.classroom.students.add(request.user)
            return redirect('profile')
            # Перенаправление на страницу с подтверждением или другую страницу
        elif 'decline' in request.POST:
            join_request.delete()
            return redirect('profile')
            # Удалить запрос при отклонении
            # Перенаправление на страницу с подтверждением отклонения или другую страницу

    return render(request, 'accept_join_request.html', {'join_request': join_request})
@login_required
def delete_classroom(request, classroom_id):
    classroom = get_object_or_404(Classroom, id=classroom_id, teacher=request.user)
    if request.method == 'POST':
        classroom.delete()
        return redirect('profile')  # Перенаправление на другую страницу после удаления
    return render(request, 'delete_classroom.html', {'classroom': classroom})
@login_required
def remove_student_from_classroom(request, classroom_id, student_id):
    classroom = get_object_or_404(Classroom, id=classroom_id, teacher=request.user)
    student = get_object_or_404(User, id=student_id)
    if request.method == 'POST':
        classroom.students.remove(student)
        return redirect('classroom_detail', classroom_id=classroom_id)
    return render(request, 'classroom_detail.html', {'classroom': classroom, 'student': student})
@login_required
def student_profile(request, user_id):
    student = get_object_or_404(User, pk=user_id)
    user_profile = UserProfile.objects.filter(user=student).first()

    test_results = TestResult.objects.filter(user=student)

    context = {
        'student': student,
        'user_profile': user_profile,
        'test_results': test_results
    }

    return render(request, 'student_profile.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def process_test(request, test_id):

    if request.method == 'POST':
        # Очистка данных сессии после отправки ответов
        keys_to_clear = [key for key in request.session.keys() if key.startswith('answer_') or key == 'questions_order']
        for key in keys_to_clear:
            del request.session[key]
    if request.method == 'POST':
        try:
            test = Test.objects.get(id=test_id)
            user = request.user
            score = 0

            for question in test.question_set.all():
                user_answer = request.POST.get(str(question.id))
                correct_answer = question.answer_set.filter(is_correct=True).first()

                # Check if correct answer exists and user answer matches it
                if correct_answer and user_answer == correct_answer.text:
                    score += 1
# You can add additional logic here if needed, for example, handling specific types of questions differently

            # Find or create a TestResult entry for this user and test
            user_test_result, created = TestResult.objects.get_or_create(user=user, test=test)

            # Update the latest result
            user_test_result.score = score

            # Update the best result if it's better than the previous one
            if score > user_test_result.best_score:
                user_test_result.best_score = score

            user_test_result.save()
            total_questions = test.question_set.count()
            return redirect('test_results', test_id=test_id)

        except Test.DoesNotExist:
            return redirect('profile')
