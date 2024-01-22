import random

from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import (
    UserPassesTestMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.core.cache import cache
from django.forms import SplitDateTimeField
from django.forms.widgets import SplitDateTimeWidget
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
    DetailView,
)

from blog.models import Article
from users.services import manager_or_superuser
from .forms import AudienceForm
from .models import Mailing, Client, Periods, MailingLog, Audience

DATETIME_WIDGET = SplitDateTimeWidget(
    date_attrs={"type": "date", "class": "my-2"}, time_attrs={"type": "time"}
)


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "mailings/index.html"
    extra_context = {
        "nbar": "home",
    }

    def get_context_data(self, **kwargs):
        user = self.request.user
        context_data = super().get_context_data(**kwargs)

        if manager_or_superuser(user):
            all_mailings = Mailing.objects
            user_clients = Client.objects
        else:
            all_mailings = user.mailing_set
            user_clients = user.client_set

        if settings.CACHE_ENABLED:
            key_random_articles = "index_page_random_articles"
            random_articles = cache.get(key_random_articles)

            if random_articles is None:
                total_articles = Article.objects.filter(is_published=True).count()
                random_articles_limit = total_articles if total_articles <= 3 else 3
                random_articles = random.sample(
                    list(Article.objects.filter(is_published=True)),
                    random_articles_limit,
                )
                cache.set(key_random_articles, random_articles)
        else:
            total_articles = Article.objects.filter(is_published=True).count()
            random_articles_limit = total_articles if total_articles <= 3 else 3
            random_articles = random.sample(
                list(Article.objects.filter(is_published=True)), random_articles_limit
            )

        total_mailings = all_mailings.count()
        started_mailings = all_mailings.filter(status="started").count()
        waiting_for_start = all_mailings.filter(status="created").count()
        total_clients = user_clients.count()

        context_data["total_mailings"] = total_mailings
        context_data["started_mailings"] = started_mailings
        context_data["waiting_for_start"] = waiting_for_start
        context_data["total_clients"] = total_clients
        context_data["random_articles"] = random_articles

        return context_data


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing

    extra_context = {
        "title": "Рассылки",
        "nbar": "mailings",
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        user = self.request.user

        if not manager_or_superuser(user):
            queryset = queryset.filter(creator=user)

        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        all_mailings = self.get_queryset()

        started_mailings = all_mailings.filter(status="started")
        created_mailings = all_mailings.filter(status="created")
        finished_mailings = all_mailings.filter(status="finished")

        context_data["created_mailings"] = created_mailings
        context_data["started_mailings"] = started_mailings
        context_data["finished_mailings"] = finished_mailings
        return context_data


class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Mailing
    permission_required = "mailings.delete_mailing"
    success_url = reverse_lazy("mailings:mailings_list")


class MailingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Mailing
    permission_required = "mailings.add_mailing"
    fields = (
        "name",
        "period",
        "audience",
        "start_time",
        "end_time",
        "message_title",
        "message_body",
    )
    success_url = reverse_lazy("mailings:mailings_list")
    extra_context = {
        "title": "Создать рассылку",
        "nbar": "mailings",
    }

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["start_time"] = SplitDateTimeField(
            widget=DATETIME_WIDGET, label="Время начала"
        )
        form.fields["end_time"] = SplitDateTimeField(
            widget=DATETIME_WIDGET, label="Время завершения"
        )
        form.fields["audience"].queryset = Audience.objects.filter(
            creator=self.request.user
        )
        return form

    def form_valid(self, form):
        mailing = form.save(commit=False)
        user = self.request.user
        mailing.creator = user
        mailing.save()

        return super().form_valid(form)


class MailingUpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView
):
    model = Mailing
    permission_required = "mailings.change_mailing"
    fields = (
        "name",
        "period",
        "audience",
        "start_time",
        "end_time",
        "message_title",
        "message_body",
    )
    success_url = reverse_lazy("mailings:mailings_list")

    extra_context = {
        "title": "Редактировать рассылку",
        "nbar": "mailings",
    }

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["start_time"] = SplitDateTimeField(
            widget=DATETIME_WIDGET, label="Время начала"
        )
        form.fields["end_time"] = SplitDateTimeField(
            widget=DATETIME_WIDGET, label="Время начала"
        )
        form.fields["audience"].queryset = Audience.objects.filter(
            creator=self.request.user
        )
        return form

    def test_func(self):
        mailing = self.get_object()
        return mailing.creator == self.request.user or self.request.user.is_superuser


class MailingDetailView(
    LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, DetailView
):
    model = Mailing
    permission_required = "mailings.view_mailing"

    extra_context = {
        "nbar": "mailings",
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["title"] = f"Рассылка {self.object.name}"
        return context_data

    def test_func(self):
        mailing = self.get_object()
        user = self.request.user
        return mailing.creator == user or manager_or_superuser(user)


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Client
    permission_required = "mailings.add_client"
    fields = ("first_name", "last_name", "email", "note")
    success_url = reverse_lazy("mailings:client_list")

    extra_context = {"title": "Добавить получателя", "nbar": "clients"}

    def form_valid(self, form):
        user = self.request.user
        client = form.save(commit=False)
        client.creator = user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView
):
    model = Client
    permission_required = "mailings.change_client"
    fields = ("first_name", "last_name", "email", "note")
    success_url = reverse_lazy("mailings:client_list")
    extra_context = {"title": "Изменить данные получателя", "nbar": "clients"}

    def test_func(self):
        client = self.get_object()
        return client.creator == self.request.user or self.request.user.is_superuser


class ClientDeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, DeleteView
):
    model = Client
    permission_required = "mailings.delete_client"
    success_url = reverse_lazy("mailings:client_list")
    extra_context = {
        "title": "Удаление клиента",
        "nbar": "clients",
    }

    def test_func(self):
        client = self.get_object()
        return client.creator == self.request.user or self.request.user.is_superuser


class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Client
    permission_required = "mailings.view_client"

    extra_context = {"title": "Клиенты", "nbar": "clients"}

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        user = self.request.user

        if not manager_or_superuser(user):
            queryset = queryset.filter(creator=user)

        return queryset


class PeriodsCreateView(LoginRequiredMixin, CreateView):
    model = Periods
    fields = ("name", "duration")
    success_url = reverse_lazy("mailings:periods_list")

    extra_context = {
        "title": "Добавить период",
        "nbar": "periods",
    }


class PeriodsListView(LoginRequiredMixin, ListView):
    model = Periods

    extra_context = {
        "title": "Периоды",
        "nbar": "periods",
    }


class MailingLogListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = MailingLog
    permission_required = "mailings.view_mailinglog"

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)

        user = self.request.user
        if manager_or_superuser(user):
            context_data["mailings"] = Mailing.objects.all()
        else:
            context_data["mailings"] = Mailing.objects.filter(creator=user)

        context_data["title"] = "Логи"
        context_data["nbar"] = "logs"
        context_data["selected_mailing_pk"] = int(self.request.POST.get("mailing", 0))

        return context_data

    def get_queryset(self):
        mailing_pk = self.request.POST.get("mailing", 0)

        user = self.request.user

        if manager_or_superuser(user):
            all_objects = self.model.objects.all()
            mailing_pk_list = list(Mailing.objects.values_list("pk", flat=True))
        else:
            all_objects = self.model.objects.filter(mailing__creator=user)
            mailing_pk_list = list(user.mailing_set.values_list("pk", flat=True))
        if int(mailing_pk) in mailing_pk_list:
            return all_objects.filter(mailing_id=mailing_pk)
        return all_objects

    def post(self, request):
        return self.get(request)


class AudienceListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Audience
    permission_required = "mailings.view_audience"
    extra_context = {
        "title": "Аудитории",
        "nbar": "audiences",
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        user = self.request.user

        if not (user.has_perm("mailings.view_all_mailings") or user.is_superuser):
            queryset = queryset.filter(creator=user)

        return queryset


class AudienceCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Audience
    permission_required = "mailings.add_audience"
    form_class = AudienceForm
    success_url = reverse_lazy("mailings:audiences_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        audience = form.save(commit=False)
        audience.creator = user
        audience.save()
        return super().form_valid(form)


@login_required
@permission_required("mailing.stop_mailing")
def stop_mailing(request, pk):
    mailing = Mailing.objects.get(pk=pk)
    mailing.status = Mailing.STATUS_FINISHED
    mailing.save()
    return redirect(reverse_lazy("mailings:mailings_list"))


@login_required
@permission_required("mailings.start_mailing")
def start_mailing(request, pk):
    mailing = Mailing.objects.get(pk=pk)
    mailing.status = Mailing.STATUS_CREATED
    mailing.save()
    return redirect(reverse_lazy("mailings:mailings_list"))
