from django.urls import path

from .apps import UsersConfig
from .views import (
    LoginView,
    LogoutView, RegisterView, activate_user, UserListView, deactivate_user, manager_activate_user
)

app_name = UsersConfig.name

urlpatterns = [
    path("", UserListView.as_view(), name="users_list"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/<uuid:uid>/<token>/", activate_user, name="activate_user"),
    path("profile/<int:pk>/activate/", manager_activate_user, name="manager_activate_user"),
    path("<uuid:uid>/deactivate/", deactivate_user, name="deactivate_user"),

    # path("profile/", UserUpdateView.as_view(), name="profile"),
    # # path("profile/generatepassword/", generate_new_password, name="generate_new_password"),
    # path("activation_successful/", ActivationSuccessfulView.as_view(), name="activation_successful"),
    # path("profile/password-reset/", PasswordResetView.as_view(), name="password_reset"),
    # # path('reset-password/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path("profile/password-reset-done/", PasswordResetDoneView.as_view(), name="password_reset_done"),
]
