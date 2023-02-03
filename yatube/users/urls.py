from django.contrib.auth import views as v
from django.urls import include, path, reverse_lazy

from users.apps import UsersConfig
from users.views import SignUp

app_name = UsersConfig.name
passwords = [
    path(
        'change/form/',
        v.PasswordChangeView.as_view(
            success_url=reverse_lazy('users:password_change_done'),
            template_name='users/password_change.html',
        ),
        name='password_change_form',
    ),
    path(
        'change/done/',
        v.PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html',
        ),
        name='password_change_done',
    ),
    path(
        'reset/form/',
        v.PasswordResetView.as_view(
            success_url=reverse_lazy('users:password_reset_done'),
            template_name='users/password_reset_form.html',
        ),
        name='password_reset_form',
    ),
    path(
        'reset/complete/',
        v.PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),
    path(
        'reset/done/',
        v.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html',
        ),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        v.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('users:password_reset_complete'),
            template_name='users/password_reset_confirm.html',
        ),
        name='password_reset_confirm',
    ),
]

urlpatterns = [
    path(
        'logout/',
        v.LogoutView.as_view(template_name='users/logged_out.html'),
        name='logout',
    ),
    path(
        'signup/',
        SignUp.as_view(),
        name='signup',
    ),
    path(
        'login/',
        v.LoginView.as_view(template_name='users/login.html'),
        name='login',
    ),
    path('password/', include(passwords)),
]
