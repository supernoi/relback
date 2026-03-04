"""
URL routing for the REST API (Phase 17).
"""
from django.urls import path

from . import views

app_name = "api"

urlpatterns = [
    path("backup-audit/", views.backup_audit_list, name="backup-audit-list"),
]
