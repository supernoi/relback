from django.contrib import admin
from django.urls import path
from coreRelback import views

app_name = "coreRelback"

urlpatterns = [
    # Página inicial e administração
    path("", views.index, name="index"),
    path("admin/", admin.site.urls),
    path("creators/", views.creators, name="creators"),

    # Endpoints para Clientes
    path("clients/", views.clientRead.as_view(), name="client-list"),
    path("clients/create/", views.clientCreate.as_view(), name="client-create"),
    path("clients/<int:pk>/update/", views.clientUpdate.as_view(), name="client-update"),
    path("clients/<int:pk>/delete/", views.clientDelete.as_view(), name="client-delete"),

    # Endpoints para Hosts
    path("hosts/", views.hostRead.as_view(), name="host-list"),
    path("hosts/create/", views.hostCreate.as_view(), name="host-create"),
    path("hosts/<int:pk>/update/", views.hostUpdate.as_view(), name="host-update"),
    path("hosts/<int:pk>/delete/", views.hostDelete.as_view(), name="host-delete"),

    # Endpoints para Bancos de Dados
    path("databases/", views.databaseRead.as_view(), name="database-list"),
    path("databases/create/", views.databaseCreate.as_view(), name="database-create"),
    path("databases/<int:pk>/update/", views.databaseUpdate.as_view(), name="database-update"),
    path("databases/<int:pk>/delete/", views.databaseDelete.as_view(), name="database-delete"),
    path("databases/<int:pk>/hosts/", views.hostsList, name="database-hosts-list"),

    # Endpoints para Políticas de Backup
    path("policies/", views.policyRead.as_view(), name="policy-list"),
    path("policies/detail/", views.policyRead.policyDetail, name="policy-detail"),
    path("policies/create/", views.policyCreate.as_view(), name="policy-create"),
    path("policies/<int:pk>/update/", views.policyUpdate.as_view(), name="policy-update"),
    path("policies/<int:pk>/delete/", views.policyDelete.as_view(), name="policy-delete"),
    path("policies/hosts/", views.hostsList, name="policy-hosts-list"),
    path("policies/databases/", views.databasesList, name="policy-databases-list"),

    # Endpoints para Relatórios
    path("reports/", views.reportRead, name="report-read"),
    path(
        "reports/read-log-detail/<int:idPolicy>/<int:dbKey>/<int:sessionKey>/",
        views.reportReadLogDetail,
        name="report-read-log-detail"
    ),
    path("reports/refresh-schedule/", views.reportRefreshSchedule, name="report-refresh-schedule"),
]
