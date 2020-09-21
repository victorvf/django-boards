from django.urls import path
from django.contrib.auth import views as auth_views

from .views import sign_up, UserUpdateView

urlpatterns = [
    path('signup/', sign_up, name='sign_up'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='login.html'),
        name='login'
    ),

    path(
        'reset/',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'
        ),
        name='password_reset'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    path(
        'settings/password/',
        auth_views.PasswordChangeView.as_view(
            template_name='password_change.html'
        ),
        name='password_change'
    ),
    path(
        'settings/password/done',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='password_change_done.html'
        ),
        name='password_change_done'
    ),

    path('settings/account/', UserUpdateView.as_view(), name='my_account')
]
