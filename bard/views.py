from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .forms import *
from .utils import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from .models import TestResult, Test
import random
from .models import UserProfile
from .models import MathTopic
from .forms import RegisterUserForm

from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import UserProfile
from django.contrib.auth.decorators import login_required


def math_topic_details(request, topic_id):
    topic = MathTopic.objects.get(pk=topic_id)
    test_id = ...
    context = {
        'topic': topic,
        'your_test_id': test_id  # убедитесь, что здесь правильный test_id
    }
    return render(request, 'topic_details.html', {'topic': topic})


def test_results(request, test_id):
    test = Test.objects.get(id=test_id)
    user = request.user

    # Получаем результаты теста для пользователя
    user_test_result = TestResult.objects.filter(user=user, test=test).first()

    context = {
        'test': test,
        'user_test_result': user_test_result,
    }
    return render(request, 'test_results.html', context)





def test_view(request, test_id):
    test = get_object_or_404(Test, pk=test_id)


    # Проверка, были ли вопросы уже перемешаны и сохранены в сессии
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
    return render(request, 'test.html', context,)


@login_required
def profile(request):
    user = request.user
    tests = Test.objects.all()
    test_results = {}
    for test in tests:
        user_test_result = TestResult.objects.filter(user=user, test=test).first()
        test_results[test] = user_test_result

    # Получите профиль пользователя, если он существует
    try:
        user_profile = UserProfile.objects.get(user=user)
        full_name = user_profile.full_name
        status = user_profile.status
    except UserProfile.DoesNotExist:
        full_name = ""
        status = ""

    context = {
        'user': user,
        'tests': tests,
        'test_results': test_results,
        'full_name': full_name,  # Добавьте ФИО в контекст
        'status': status,        # Добавьте статус в контекст
    }

    return render(request, 'profile.html', context)


class Home(DataMixin, ListView):
    model = Women
    template_name = 'index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')



class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация / Тіркелу")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        # Создайте пользователя
        user = form.save()

        # Создайте профиль пользователя и свяжите его с пользователем
        full_name = form.cleaned_data.get('full_name')
        status = form.cleaned_data.get('status')
        UserProfile.objects.create(user=user, full_name=full_name, status=status)

        # Авторизуйте пользователя
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация / Авторландыру")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


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

class Home2(DataMixin, ListView):
    model = Women
    template_name = 'base2.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Басты бет")
        return dict(list(context.items()) + list(c_def.items()))


