from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import AbstractUser, Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.http import HttpResponse, HttpResponseServerError
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from users.forms import UserRegisterForm
from users.services import send_verify_mail


class LoginView(BaseLoginView):
    extra_context = {"title": "Сервис рассылок - Вход"}


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = get_user_model()
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")
    template_name = "users/register.html"

    def form_valid(self, form):
        try:
            service_users_group = Group.objects.get(name="Service users")
        except Group.DoesNotExist:
            # Верните ошибку 500, если группа не найдена
            return HttpResponseServerError(
                "Internal Server Error: 'Service users' group not found."
            )

        user = form.save(commit=False)
        user.is_active = False
        user.save()

        user.groups.add(service_users_group)
        user.save()

        send_verify_mail(user, self.request)

        return HttpResponse("Ссылка для подтверждения отправлена на ваш email.")


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = get_user_model()

    permission_required = "users.view_user"

    extra_context = {
        "title": "Пользователи",
        "nbar": "users",
    }


def activate_user(request, uid, token):
    UserModel: AbstractUser = get_user_model()
    try:
        user = UserModel.objects.get(uid=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse(
            "Спасибо за регистрацию! Теперь вы можете войти в свой аккаунт"
        )

    return HttpResponse("Неверная ссылка активации!")


@permission_required("users.block_user", raise_exception=True)
def deactivate_user(request, uid):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(uid=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None:

        if user.is_superuser:
            return HttpResponse(f"Нельзя заблокировать суперпользователя")

        user.is_active = False
        user.save()
        return HttpResponse(f"Пользователь с почтой {user.email} заблокирован.")

    return HttpResponse("Пользователь не найден")


@permission_required("users.activate_user", raise_exception=True)
def manager_activate_user(request, pk):
    UserModel: AbstractUser = get_user_model()
    try:
        user = UserModel.objects.get(pk=pk)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None:
        user.is_active = True
        user.save()
        return HttpResponse(
            f"Пользователь {user.email} активирован!"
        )

    return HttpResponse("Пользователь не найден")
