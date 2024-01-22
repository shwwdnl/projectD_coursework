from django.urls import path

from . import views
from .apps import MailingsConfig

app_name = MailingsConfig.name

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('mailings/', views.MailingListView.as_view(), name='mailings_list'),

    path('mailings/create/', views.MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/edit/<int:pk>/', views.MailingUpdateView.as_view(), name='mailing_edit'),
    path('mailings/stop/<int:pk>/', views.stop_mailing, name='mailing_stop'),
    path('mailings/start/<int:pk>/', views.start_mailing, name='mailing_start'),
    path('mailings/delete/<int:pk>/', views.MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailings/<int:pk>/', views.MailingDetailView.as_view(), name='mailing_detail'),

    path('clients/create/', views.ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/edit/', views.ClientUpdateView.as_view(), name='client_edit'),
    path('clients/<int:pk>/delete/', views.ClientDeleteView.as_view(), name='client_delete'),
    path('clients/', views.ClientListView.as_view(), name='client_list'),

    path('audiences/', views.AudienceListView.as_view(), name='audiences_list'),
    path('audiences/create/', views.AudienceCreateView.as_view(), name='audiences_create'),

    path('mailings/periods/create/', views.PeriodsCreateView.as_view(), name='periods_create'),
    path('mailings/periods/', views.PeriodsListView.as_view(), name='periods_list'),

    path('mailing_logs/', views.MailingLogListView.as_view(), name='mailing_log_list'),
]
