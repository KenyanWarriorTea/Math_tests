from django.urls import path, re_path
from django.contrib.auth import views as auth_views


from . import views
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('accept-invitation/<int:join_request_id>/', views.accept_classroom_invitation, name='accept_invitation'),
    path('email-confirmation/', EmailConfirmationView.as_view(), name='email_confirmation'),
    path('classroom/<int:classroom_id>/', views.classroom_detail, name='classroom_detail'),
    path('topics/<int:topic_id>/', math_topic_details, name='topic_details'),
    path('test-history/<int:test_id>/', views.test_history, name='test_history'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('test/<int:test_id>/', views.test_view, name='test_view'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('profile/', profile, name='profile'),
    path('kz/', Home2.as_view(), name="home2"),
    path('process_test/<int:test_id>/', process_test, name='process_test'),
    path('create_class/', views.create_classroom, name='create_class'),
    path('test-results/<int:test_id>/', test_results, name='test_results'),
    path('profile/student/<int:user_id>/', views.student_profile, name='profile_student'),
    path('classroom/delete/<int:classroom_id>/', views.delete_classroom, name='delete_classroom'),
    path('manage-join-requests/', views.manage_join_requests, name='manage_join_requests'),
    path('accept-join-request/<int:join_request_id>/', views.accept_join_request, name='accept_join_request'),
    path('set-language/russian/', views.set_language_to_russian, name='set_language_russian'),
    path('set-language/kazakh/', views.set_language_to_kazakh, name='set_language_kazakh'),
    path('classroom/<int:classroom_id>/remove_student/<int:student_id>/', views.remove_student_from_classroom, name='remove_student_from_classroom'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),

]
