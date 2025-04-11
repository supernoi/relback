from django.contrib import admin
from django.urls import path
from coreRelback import views

app_name = "coreRelback"

urlpatterns = [
    path("", views.index, name="index"),
    path("admin/", admin.site.urls),

    path("creators/", views.creators, name="creators"),

    # Clients
    path("client/", views.clientRead.as_view(), name="client"),
    path("client/create/", views.clientCreate.as_view(), name="clientCreate"),
    path("client/update/", views.clientUpdate.as_view(), name="clientUpdate"),
    path("client/delete/", views.clientDelete.as_view(), name="clientDelete"),

    # Hosts
    path("host/", views.hostRead.as_view(), name="host"),
    path("host/create/", views.hostCreate.as_view(), name="hostCreate"),
    path("host/update/", views.hostUpdate.as_view(), name="hostUpdate"),
    path("host/delete/", views.hostDelete.as_view(), name="hostDelete"),

    # Databases
    path("database/", views.databaseRead.as_view(), name="database"),
    path("database/create/", views.databaseCreate.as_view(), name="databaseCreate"),
    path("database/update/", views.databaseUpdate.as_view(), name="databaseUpdate"),
    path("database/delete/", views.databaseDelete.as_view(), name="databaseDelete"),
    path("database/hostsList/", views.hostsList, name="databaseHostsList"),

    # Policies
    path("policy/", views.policyRead.as_view(), name="policy"),
    path("policy/detail/", views.policyRead.policyDetail, name="policyDetail"),
    path("policy/create/", views.policyCreate.as_view(), name="policyCreate"),
    path("policy/update/", views.policyUpdate.as_view(), name="policyUpdate"),
    path("policy/delete/", views.policyDelete.as_view(), name="policyDelete"),
    path("policy/hostsList/", views.hostsList, name="policyHostsList"),
    path("policy/databasesList/", views.databasesList, name="policyDatabasesList"),

    # Reports
    path("reports/", views.reportRead, name="reportRead"),
    path(
        "reports/readLogDetail/<int:idPolicy>/<int:dbKey>/<int:sessionKey>/",
        views.reportReadLogDetail,
        name="reportReadLogDetail"
    ),
    path("reports/refreshSchedule/", views.reportRefreshSchedule, name="refreshSchedule"),
]
