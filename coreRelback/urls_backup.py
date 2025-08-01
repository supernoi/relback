from django.contrib import admin
from django.urls import path
from coreRelback.views import (
    index, creators,
    ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView,
    HostListView, HostCreateView, HostUpdateView, HostDeleteView,
    DatabaseListView, DatabaseCreateView, DatabaseUpdateView, DatabaseDeleteView,
    BackupPolicyListView, BackupPolicyCreateView, BackupPolicyUpdateView, BackupPolicyDeleteView, BackupPolicyDetailView,
    report_read, report_read_log_detail, report_refresh_schedule,
    database_hosts_list, user_settings
)

app_name = "coreRelback"

urlpatterns = [
    # Página inicial e administração
    path("", index, name="index"),
    path("admin/", admin.site.urls),
    path("creators/", creators, name="creators"),

<<<<<<< HEAD
    # Authentication
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),

    path("creators/", views.creators, name="creators"),

    # Clients
    path("client/", views.clients.as_view(), name="client"),
    path("client/create/", views.clientCreate.as_view(), name="clientCreate"),
    path("client/update/", views.clientUpdate.as_view(), name="clientUpdate"),
    path("client/delete/", views.clientDelete.as_view(), name="clientDelete"),
=======
    # Endpoints para Clientes
    path("clients/", ClientListView.as_view(), name="client-list"),
    path("clients/create/", ClientCreateView.as_view(), name="client-create"),
    path("clients/<int:pk>/update/", ClientUpdateView.as_view(), name="client-update"),
    path("clients/<int:pk>/delete/", ClientDeleteView.as_view(), name="client-delete"),

    # Endpoints para Hosts
    path("hosts/", HostListView.as_view(), name="host-list"),
    path("hosts/create/", HostCreateView.as_view(), name="host-create"),
    path("hosts/<int:pk>/update/", HostUpdateView.as_view(), name="host-update"),
    path("hosts/<int:pk>/delete/", HostDeleteView.as_view(), name="host-delete"),
>>>>>>> 811bf09f982df832f56f799820e3f43d02b7aae7

    # Endpoints para Bancos de Dados
    path("databases/", DatabaseListView.as_view(), name="database-list"),
    path("databases/create/", DatabaseCreateView.as_view(), name="database-create"),
    path("databases/<int:pk>/update/", DatabaseUpdateView.as_view(), name="database-update"),
    path("databases/<int:pk>/delete/", DatabaseDeleteView.as_view(), name="database-delete"),
    path("databases/<int:pk>/hosts/", database_hosts_list, name="database-hosts-list"),

    # Endpoints para Políticas de Backup
    path("policies/", BackupPolicyListView.as_view(), name="policy-list"),
    path("policies/detail/", BackupPolicyDetailView.as_view(), name="policy-detail"),
    path("policies/create/", BackupPolicyCreateView.as_view(), name="policy-create"),
    path("policies/<int:pk>/update/", BackupPolicyUpdateView.as_view(), name="policy-update"),
    path("policies/<int:pk>/delete/", BackupPolicyDeleteView.as_view(), name="policy-delete"),

    # Endpoints para Relatórios
    path("reports/", report_read, name="report-read"),
    path("reports/read-log-detail/<int:idPolicy>/<int:dbKey>/<int:sessionKey>/", report_read_log_detail, name="report-read-log-detail"),
    path("reports/refresh-schedule/", report_refresh_schedule, name="report-refresh-schedule"),
]
