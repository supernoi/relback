"""
django-tables2 Table classes for server-side pagination and sorting.

Used with RequestConfig in views to enable ?page= and ?sort= query params.
"""
import django_tables2 as tables

from .models import Client, Host, Database, BackupPolicy


class ClientTable(tables.Table):
    """Clients list with pagination."""

    name = tables.Column(verbose_name="Client Name", order_by="name")
    description = tables.Column(verbose_name="Description")
    created_at = tables.DateTimeColumn(format="M d, Y", verbose_name="Created")
    actions = tables.TemplateColumn(
        verbose_name="Actions",
        template_name="coreRelback/table_actions_client.html",
        orderable=False,
    )

    class Meta:
        model = Client
        attrs = {"class": "table table-xs table-zebra w-full"}
        fields = ("name", "description", "created_at", "actions")
        per_page = 25


class HostTable(tables.Table):
    """Hosts list with pagination."""

    hostname = tables.Column(verbose_name="Hostname", order_by="hostname")
    ip = tables.Column(verbose_name="IP")
    client = tables.Column(verbose_name="Client", accessor="client.name")
    created_at = tables.DateTimeColumn(format="M d, Y", verbose_name="Created")
    actions = tables.TemplateColumn(
        verbose_name="Actions",
        template_name="coreRelback/table_actions_host.html",
        orderable=False,
    )

    class Meta:
        model = Host
        attrs = {"class": "table table-xs table-zebra w-full"}
        fields = ("hostname", "ip", "client", "created_at", "actions")
        per_page = 25


class DatabaseTable(tables.Table):
    """Databases list with pagination."""

    db_name = tables.Column(verbose_name="Database", order_by="db_name")
    dbid = tables.Column(verbose_name="DBID")
    host = tables.Column(verbose_name="Host", accessor="host.hostname")
    client = tables.Column(verbose_name="Client", accessor="client.name")
    created_at = tables.DateTimeColumn(format="M d, Y", verbose_name="Created")
    actions = tables.TemplateColumn(
        verbose_name="Actions",
        template_name="coreRelback/table_actions_database.html",
        orderable=False,
    )

    class Meta:
        model = Database
        attrs = {"class": "table table-xs table-zebra w-full"}
        fields = ("db_name", "dbid", "host", "client", "created_at", "actions")
        per_page = 25


class BackupPolicyTable(tables.Table):
    """Backup policies list with pagination."""

    policy_name = tables.Column(verbose_name="Policy", order_by="policy_name")
    backup_type = tables.Column(verbose_name="Type")
    database = tables.Column(verbose_name="Database", accessor="database.db_name")
    host = tables.Column(verbose_name="Host", accessor="host.hostname")
    created_at = tables.DateTimeColumn(format="M d, Y", verbose_name="Created")
    actions = tables.TemplateColumn(
        verbose_name="Actions",
        template_name="coreRelback/table_actions_policy.html",
        orderable=False,
    )

    class Meta:
        model = BackupPolicy
        attrs = {"class": "table table-xs table-zebra w-full"}
        fields = ("policy_name", "backup_type", "database", "host", "created_at", "actions")
        per_page = 25


class ReportJobTable(tables.Table):
    """Reports page: backup jobs (list of dicts). No model; data from view."""

    policy_name = tables.Column(verbose_name="Policy")
    hostname = tables.Column(verbose_name="Host")
    db_name = tables.Column(verbose_name="Database")
    backup_type = tables.Column(verbose_name="Type")
    start_time = tables.DateTimeColumn(format="M d, Y H:i", verbose_name="Start")
    end_time = tables.DateTimeColumn(format="M d, Y H:i", verbose_name="End")
    status = tables.Column(verbose_name="Status")
    time_taken_display = tables.Column(verbose_name="Duration")
    output_bytes_display = tables.Column(verbose_name="Size")

    class Meta:
        attrs = {"class": "table table-xs table-zebra w-full"}
        per_page = 25
