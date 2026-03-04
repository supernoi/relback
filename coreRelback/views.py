from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django_tables2 import RequestConfig
from django.db.models import Q
from .models import Client, Host, Database, BackupPolicy, RelbackUser, Schedule
from .mixins import RoleRequiredMixin
from .tables import ClientTable, HostTable, DatabaseTable, BackupPolicyTable
from django import forms

# --- Clean Architecture: use-case factories ---
from coreRelback.domain.entities import BackupStatusValue
from coreRelback.gateways.repositories import (
    DjangoClientRepository,
    DjangoHostRepository,
    DjangoDatabaseRepository,
    DjangoBackupPolicyRepository,
    DjangoScheduleRepository,
    OracleRmanRepository,
    DemoRmanRepository,
)
from coreRelback.services.use_cases import (
    AuditBackupUseCase,
    GetDashboardStatsUseCase,
    GetScheduleReportUseCase,
    GenerateScheduleUseCase,
    CreateClientUseCase,
    UpdateClientUseCase,
    DeleteClientUseCase,
    CreateHostUseCase,
    UpdateHostUseCase,
    DeleteHostUseCase,
    CreateDatabaseUseCase,
    UpdateDatabaseUseCase,
    DeleteDatabaseUseCase,
    CreateBackupPolicyUseCase,
    UpdateBackupPolicyUseCase,
    DeleteBackupPolicyUseCase,
    GetBackupDetailUseCase,
)


def _get_rman_repo():
    """Return the appropriate RMAN repository based on settings.

    When ``DEMO_MODE = True``, returns ``DemoRmanRepository`` so the UI
    renders with realistic fixture data even without an Oracle connection.
    Otherwise uses ``OracleRmanRepository`` (which also gracefully returns
    empty lists when ``ORACLE_CATALOG`` is None).
    """
    from django.conf import settings
    if getattr(settings, "DEMO_MODE", False):
        return DemoRmanRepository()
    return OracleRmanRepository()


def _get_relback_user(request):
    """Resolves the RelbackUser for the current request. Returns None if not found."""
    try:
        return RelbackUser.objects.get(username=request.user.username)
    except RelbackUser.DoesNotExist:
        return None


def _make_dashboard_use_case() -> GetDashboardStatsUseCase:
    return GetDashboardStatsUseCase(
        client_repo=DjangoClientRepository(),
        host_repo=DjangoHostRepository(),
        database_repo=DjangoDatabaseRepository(),
        policy_repo=DjangoBackupPolicyRepository(),
    )


def _make_schedule_report_use_case() -> GetScheduleReportUseCase:
    return GetScheduleReportUseCase(schedule_repo=DjangoScheduleRepository())


def _make_generate_schedule_use_case() -> GenerateScheduleUseCase:
    return GenerateScheduleUseCase(
        policy_repo=DjangoBackupPolicyRepository(),
        schedule_repo=DjangoScheduleRepository(),
    )


# ---------------------------------------------------------------------------
# Infrastructure helpers (used by test_without_db.py and health checks)
# ---------------------------------------------------------------------------

def is_database_available() -> bool:
    """Returns True if the Django default DB is reachable."""
    try:
        from django.db import connection
        connection.ensure_connection()
        return True
    except Exception:
        return False


@login_required
def get_hosts_by_client(request, client_id: int) -> JsonResponse:
    """Returns hosts JSON for a given client_id (used by AJAX selects)."""
    try:
        hosts = list(Host.objects.filter(
            client_id=client_id).values('id_host', 'hostname'))
        return JsonResponse({'hosts': hosts})
    except Exception:
        return JsonResponse({'hosts': []})


@login_required
def get_databases_by_client(request, client_id: int) -> JsonResponse:
    """Returns databases JSON for a given client_id (used by AJAX selects)."""
    try:
        dbs = list(Database.objects.filter(
            client_id=client_id).values('id_database', 'db_name'))
        return JsonResponse({'databases': dbs})
    except Exception:
        return JsonResponse({'databases': []})


# Função para a página inicial
@login_required
def index(request):
    stats = _make_dashboard_use_case().execute()
    context = {
        'clients_count': stats.clients_count,
        'hosts_count': stats.hosts_count,
        'databases_count': stats.databases_count,
        'policies_count': stats.policies_count,
    }
    return render(request, "index.html", context)


# Função para a página dos criadores
def creators(request):
    return render(request, "creators.html")


# ---------------------------
# VIEWS PARA CLIENTS
# ---------------------------
class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "clients.html"
    context_object_name = "clients"

    def get_queryset(self):
        qs = super().get_queryset()
        search = (self.request.GET.get("search") or "").strip()
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(description__icontains=search))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table = ClientTable(self.get_queryset())
        RequestConfig(self.request, paginate={"per_page": 25}).configure(table)
        context["table"] = table
        context["clients_count"] = self.get_queryset().count()
        return context


class ClientCreateView(RoleRequiredMixin, LoginRequiredMixin, CreateView):
    required_roles = [RelbackUser.ROLE_ADMIN, RelbackUser.ROLE_OPERATOR]
    model = Client
    template_name = "client_form.html"
    fields = ['name', 'description']
    success_url = reverse_lazy('coreRelback:client-list')

    def form_valid(self, form):
        relback_user = _get_relback_user(self.request)
        if relback_user is None:
            form.add_error(
                None, "Usuário não possui perfil RelbackUser cadastrado.")
            return self.form_invalid(form)
        CreateClientUseCase(DjangoClientRepository()).execute(
            name=form.cleaned_data['name'],
            description=form.cleaned_data.get('description'),
            created_by_id=relback_user.pk,
        )
        return redirect(self.success_url)


class ClientUpdateView(RoleRequiredMixin, LoginRequiredMixin, UpdateView):
    required_roles = [RelbackUser.ROLE_ADMIN, RelbackUser.ROLE_OPERATOR]
    model = Client
    template_name = "client_form.html"
    fields = ['name', 'description']
    success_url = reverse_lazy('coreRelback:client-list')

    def form_valid(self, form):
        relback_user = _get_relback_user(self.request)
        if relback_user is None:
            form.add_error(
                None, "Usuário não possui perfil RelbackUser cadastrado.")
            return self.form_invalid(form)
        UpdateClientUseCase(DjangoClientRepository()).execute(
            client_id=self.object.pk,
            name=form.cleaned_data['name'],
            description=form.cleaned_data.get('description'),
            updated_by_id=relback_user.pk,
        )
        return redirect(self.success_url)


class ClientDeleteView(RoleRequiredMixin, LoginRequiredMixin, DeleteView):
    required_roles = [RelbackUser.ROLE_ADMIN]
    model = Client
    template_name = "client_confirm_delete.html"
    success_url = reverse_lazy('coreRelback:client-list')

    def delete(self, request, *args, **kwargs):
        DeleteClientUseCase(DjangoClientRepository()
                            ).execute(self.get_object().pk)
        return redirect(self.success_url)


# ---------------------------
# VIEWS PARA HOSTS
# ---------------------------
class HostListView(LoginRequiredMixin, ListView):
    model = Host
    template_name = "hosts.html"
    context_object_name = "hosts"

    def get_queryset(self):
        qs = super().get_queryset().select_related("client")
        search = (self.request.GET.get("search") or "").strip()
        if search:
            qs = qs.filter(hostname__icontains=search) | qs.filter(ip__icontains=search)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hosts = self.get_queryset()
        table = HostTable(hosts)
        RequestConfig(self.request, paginate={"per_page": 25}).configure(table)
        context["table"] = table
        context["total_hosts"] = hosts.count()
        context["active_hosts"] = hosts.count()
        context["total_clients"] = Client.objects.count()
        context["total_databases"] = Database.objects.filter(host__in=hosts).count()
        context["clients"] = Client.objects.all()
        return context


class HostCreateView(RoleRequiredMixin, LoginRequiredMixin, CreateView):
    required_roles = [RelbackUser.ROLE_ADMIN, RelbackUser.ROLE_OPERATOR]
    model = Host
    template_name = "host_form.html"
    fields = ['hostname', 'description', 'ip', 'client']
    success_url = reverse_lazy('coreRelback:host-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["clients"] = Client.objects.all().order_by("name")
        return context

    def form_valid(self, form):
        relback_user = _get_relback_user(self.request)
        if relback_user is None:
            form.add_error(
                None, "Usuário não possui perfil RelbackUser cadastrado.")
            return self.form_invalid(form)
        CreateHostUseCase(DjangoHostRepository()).execute(
            hostname=form.cleaned_data['hostname'],
            description=form.cleaned_data.get('description', ''),
            ip=form.cleaned_data.get('ip', ''),
            client_id=form.cleaned_data['client'].pk,
            created_by_id=relback_user.pk,
        )
        return redirect(self.success_url)


class HostUpdateView(RoleRequiredMixin, LoginRequiredMixin, UpdateView):
    required_roles = [RelbackUser.ROLE_ADMIN, RelbackUser.ROLE_OPERATOR]
    model = Host
    template_name = "host_form.html"
    fields = ['hostname', 'description', 'ip', 'client']
    success_url = reverse_lazy('coreRelback:host-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["clients"] = Client.objects.all().order_by("name")
        return context

    def form_valid(self, form):
        relback_user = _get_relback_user(self.request)
        if relback_user is None:
            form.add_error(
                None, "Usuário não possui perfil RelbackUser cadastrado.")
            return self.form_invalid(form)
        UpdateHostUseCase(DjangoHostRepository()).execute(
            host_id=self.object.pk,
            hostname=form.cleaned_data['hostname'],
            description=form.cleaned_data.get('description', ''),
            ip=form.cleaned_data.get('ip', ''),
            client_id=form.cleaned_data['client'].pk,
            updated_by_id=relback_user.pk,
        )
        return redirect(self.success_url)


class HostDeleteView(RoleRequiredMixin, LoginRequiredMixin, DeleteView):
    required_roles = [RelbackUser.ROLE_ADMIN]
    model = Host
    template_name = "host_confirm_delete.html"
    success_url = reverse_lazy('coreRelback:host-list')

    def delete(self, request, *args, **kwargs):
        DeleteHostUseCase(DjangoHostRepository()).execute(self.get_object().pk)
        return redirect(self.success_url)


# ---------------------------
# VIEWS PARA DATABASES
# ---------------------------
class DatabaseListView(LoginRequiredMixin, ListView):
    model = Database
    template_name = "databases.html"
    context_object_name = "databases"

    def get_queryset(self):
        qs = super().get_queryset().select_related("client", "host")
        search = (self.request.GET.get("search") or "").strip()
        if search:
            qs = qs.filter(Q(db_name__icontains=search) | Q(description__icontains=search))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        databases = self.get_queryset()
        table = DatabaseTable(databases)
        RequestConfig(self.request, paginate={"per_page": 25}).configure(table)
        context["table"] = table
        context["total_databases"] = databases.count()
        context["active_databases"] = databases.count()
        context["total_hosts"] = Host.objects.count()
        context["total_policies"] = BackupPolicy.objects.filter(database__in=databases).count()
        context["hosts"] = Host.objects.all().select_related("client").order_by("hostname")
        context["clients"] = Client.objects.all().order_by("name")
        return context


class DatabaseCreateView(RoleRequiredMixin, LoginRequiredMixin, CreateView):
    required_roles = [RelbackUser.ROLE_ADMIN, RelbackUser.ROLE_OPERATOR]
    model = Database
    template_name = "database_form.html"
    fields = ['db_name', 'description', 'client', 'host', 'dbid']
    success_url = reverse_lazy('coreRelback:database-list')

    def form_valid(self, form):
        relback_user = _get_relback_user(self.request)
        if relback_user is None:
            form.add_error(
                None, "Usuário não possui perfil RelbackUser cadastrado.")
            return self.form_invalid(form)
        CreateDatabaseUseCase(DjangoDatabaseRepository()).execute(
            db_name=form.cleaned_data['db_name'],
            description=form.cleaned_data.get('description', ''),
            client_id=form.cleaned_data['client'].pk,
            host_id=form.cleaned_data['host'].pk,
            dbid=form.cleaned_data.get('dbid') or 0,
            created_by_id=relback_user.pk,
        )
        return redirect(self.success_url)


class DatabaseUpdateView(RoleRequiredMixin, LoginRequiredMixin, UpdateView):
    required_roles = [RelbackUser.ROLE_ADMIN, RelbackUser.ROLE_OPERATOR]
    model = Database
    template_name = "database_form.html"
    fields = ['db_name', 'description', 'client', 'host', 'dbid']
    success_url = reverse_lazy('coreRelback:database-list')

    def form_valid(self, form):
        relback_user = _get_relback_user(self.request)
        if relback_user is None:
            form.add_error(
                None, "Usuário não possui perfil RelbackUser cadastrado.")
            return self.form_invalid(form)
        UpdateDatabaseUseCase(DjangoDatabaseRepository()).execute(
            database_id=self.object.pk,
            db_name=form.cleaned_data['db_name'],
            description=form.cleaned_data.get('description', ''),
            client_id=form.cleaned_data['client'].pk,
            host_id=form.cleaned_data['host'].pk,
            dbid=form.cleaned_data.get('dbid') or 0,
            updated_by_id=relback_user.pk,
        )
        return redirect(self.success_url)


class DatabaseDeleteView(RoleRequiredMixin, LoginRequiredMixin, DeleteView):
    required_roles = [RelbackUser.ROLE_ADMIN]
    model = Database
    template_name = "database_confirm_delete.html"
    success_url = reverse_lazy('coreRelback:database-list')

    def delete(self, request, *args, **kwargs):
        DeleteDatabaseUseCase(DjangoDatabaseRepository()
                              ).execute(self.get_object().pk)
        return redirect(self.success_url)


# Função de exemplo: lista de hosts vinculados a um determinado database
@login_required
def database_hosts_list(request, pk):
    database = get_object_or_404(Database, pk=pk)
    hosts = Host.objects.filter(client=database.client)
    context = {'database': database, 'hosts': hosts}
    return render(request, "database_hosts_list.html", context)


# ---------------------------
# VIEWS PARA BACKUP POLICIES
# ---------------------------
class BackupPolicyListView(LoginRequiredMixin, ListView):
    model = BackupPolicy
    template_name = "policies.html"
    context_object_name = "policies"

    def get_queryset(self):
        qs = super().get_queryset().select_related("client", "database", "host")
        search = (self.request.GET.get("search") or "").strip()
        if search:
            qs = qs.filter(Q(policy_name__icontains=search) | Q(backup_type__icontains=search))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        policies = self.get_queryset()
        table = BackupPolicyTable(policies)
        RequestConfig(self.request, paginate={"per_page": 25}).configure(table)
        context["table"] = table
        context["total_policies"] = policies.count()
        context["active_policies"] = policies.filter(status__iexact="ACTIVE").count()
        context["inactive_policies"] = policies.filter(status__iexact="INACTIVE").count()
        context["scheduled_policies"] = policies.filter(status__iexact="ACTIVE").count() // 2
        context["clients"] = Client.objects.all().order_by("name")
        context["hosts"] = Host.objects.all().select_related("client").order_by("hostname")
        context["databases"] = Database.objects.all().select_related("client", "host").order_by("db_name")
        return context


class BackupPolicyCreateView(RoleRequiredMixin, LoginRequiredMixin, CreateView):
    required_roles = [RelbackUser.ROLE_ADMIN, RelbackUser.ROLE_OPERATOR]
    model = BackupPolicy
    template_name = "policy_form.html"
    fields = ['policy_name', 'client', 'database', 'host', 'backup_type', 'destination',
              'minute', 'hour', 'day', 'month', 'day_week', 'duration', 'size_backup', 'status', 'description']
    success_url = reverse_lazy('coreRelback:policy-list')

    def form_valid(self, form):
        relback_user = _get_relback_user(self.request)
        if relback_user is None:
            form.add_error(
                None, "Usuário não possui perfil RelbackUser cadastrado.")
            return self.form_invalid(form)
        cd = form.cleaned_data
        CreateBackupPolicyUseCase(DjangoBackupPolicyRepository()).execute(
            policy_name=cd['policy_name'],
            client_id=cd['client'].pk,
            database_id=cd['database'].pk,
            host_id=cd['host'].pk,
            backup_type=cd['backup_type'],
            destination=cd['destination'],
            minute=cd['minute'],
            hour=cd['hour'],
            day=cd['day'],
            month=cd['month'],
            day_week=cd['day_week'],
            duration=int(cd['duration']),
            size_backup=cd['size_backup'],
            status=cd['status'],
            description=cd.get('description'),
            created_by_id=relback_user.pk,
        )
        return redirect(self.success_url)


class BackupPolicyUpdateView(RoleRequiredMixin, LoginRequiredMixin, UpdateView):
    required_roles = [RelbackUser.ROLE_ADMIN, RelbackUser.ROLE_OPERATOR]
    model = BackupPolicy
    template_name = "policy_form.html"
    fields = ['policy_name', 'client', 'database', 'host', 'backup_type', 'destination',
              'minute', 'hour', 'day', 'month', 'day_week', 'duration', 'size_backup', 'status', 'description']
    success_url = reverse_lazy('coreRelback:policy-list')

    def form_valid(self, form):
        relback_user = _get_relback_user(self.request)
        if relback_user is None:
            form.add_error(
                None, "Usuário não possui perfil RelbackUser cadastrado.")
            return self.form_invalid(form)
        cd = form.cleaned_data
        UpdateBackupPolicyUseCase(DjangoBackupPolicyRepository()).execute(
            policy_id=self.object.pk,
            policy_name=cd['policy_name'],
            client_id=cd['client'].pk,
            database_id=cd['database'].pk,
            host_id=cd['host'].pk,
            backup_type=cd['backup_type'],
            destination=cd['destination'],
            minute=cd['minute'],
            hour=cd['hour'],
            day=cd['day'],
            month=cd['month'],
            day_week=cd['day_week'],
            duration=int(cd['duration']),
            size_backup=cd['size_backup'],
            status=cd['status'],
            description=cd.get('description'),
            updated_by_id=relback_user.pk,
        )
        return redirect(self.success_url)


class BackupPolicyDeleteView(RoleRequiredMixin, LoginRequiredMixin, DeleteView):
    required_roles = [RelbackUser.ROLE_ADMIN]
    model = BackupPolicy
    template_name = "policy_confirm_delete.html"
    success_url = reverse_lazy('coreRelback:policy-list')

    def delete(self, request, *args, **kwargs):
        DeleteBackupPolicyUseCase(
            DjangoBackupPolicyRepository()).execute(self.get_object().pk)
        return redirect(self.success_url)


# Se a detail for necessária (por exemplo, para visualização detalhada de uma política)
class BackupPolicyDetailView(LoginRequiredMixin, DetailView):
    model = BackupPolicy
    template_name = "policy_detail.html"


# ---------------------------
# VIEWS PARA CONFIGURAÇÕES DO USUÁRIO
# ---------------------------
@login_required
def user_settings(request):
    """View para configurações do usuário"""
    try:
        relback_user = RelbackUser.objects.get(username=request.user.username)
    except RelbackUser.DoesNotExist:
        messages.error(request, 'User profile not found.')
        return redirect('coreRelback:index')

    if request.method == 'POST':
        # Update user settings
        relback_user.name = request.POST.get('name', relback_user.name)
        relback_user.email = request.POST.get('email', relback_user.email)
        relback_user.theme_preference = request.POST.get(
            'theme_preference', relback_user.theme_preference)
        relback_user.language_preference = request.POST.get(
            'language_preference', relback_user.language_preference)
        relback_user.notifications_enabled = 'notifications_enabled' in request.POST

        # Change password if provided
        new_password = request.POST.get('new_password')
        if new_password:
            relback_user.set_password(new_password)

        relback_user.save()
        messages.success(request, 'Settings updated successfully!')
        return redirect('coreRelback:user-settings')

    context = {
        'relback_user': relback_user,
        'theme_choices': [('light', 'Light'), ('dark', 'Dark'), ('auto', 'Auto')],
        'language_choices': [('en', 'English'), ('pt', 'Portuguese')]
    }
    return render(request, 'user_settings.html', context)


# Funções para extras na área de relatórios
class ScheduleFilterForm(forms.Form):
    policy_name = forms.CharField(label='Policy', required=False)
    hostname = forms.CharField(label='Host', required=False)
    db_name = forms.CharField(label='Database', required=False)
    backup_type = forms.CharField(label='Type', required=False)
    days = forms.IntegerField(
        label='Days', min_value=1, max_value=30, required=False, initial=2)
    start_date = forms.DateField(label='Start Date', required=False)
    end_date = forms.DateField(label='End Date', required=False)


@login_required
def report_refresh_schedule(request):
    import datetime
    days = int(request.GET.get('days', 2))
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    use_case = _make_generate_schedule_use_case()

    if start_date_str and end_date_str:
        start = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
        use_case.execute_range(start, end)
    else:
        today = datetime.date.today()
        use_case.execute_range(
            today, today + datetime.timedelta(days=days - 1))

    return redirect('coreRelback:report-read')


@login_required
def report_read(request):
    import datetime
    form = ScheduleFilterForm(request.GET or None)
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    days = int(request.GET.get('days', 2))
    status_filter = request.GET.get('status_filter', '')

    from_date = None
    to_date = None
    if start_date_str and end_date_str:
        from_date = datetime.datetime.strptime(
            start_date_str, '%Y-%m-%d').date()
        to_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()

    # ── Oracle RMAN Catalog: attempt real backup job results ──────────────
    from_dt = (datetime.datetime.combine(from_date, datetime.time.min)
               if from_date else None)
    to_dt = (datetime.datetime.combine(to_date, datetime.time.max)
             if to_date else None)
    relback_user = _get_relback_user(request)
    request_client_id = getattr(relback_user, 'default_client_id', None) if relback_user else None

    backup_jobs = AuditBackupUseCase(_get_rman_repo()).execute(
        from_date=from_dt, to_date=to_dt, client_id=request_client_id,
    )
    oracle_available = bool(backup_jobs)

    if backup_jobs:
        # Map BackupJobResult entities → template context dict.
        today = datetime.date.today()
        jobs_data = []
        for j in backup_jobs:
            status_str = (j.status.value if hasattr(j.status, 'value')
                          else str(j.status))
            if status_filter and status_filter.upper() not in status_str.upper():
                continue
            jobs_data.append({
                'policy_name':          j.input_type or '-',
                'hostname':             j.db_name,
                'db_name':              j.db_name,
                'backup_type':          j.backup_type or j.input_type or '-',
                'start_time':           j.start_time,
                'end_time':             j.end_time,
                'status':               status_str,
                'elapsed_seconds':      None,
                'time_taken_display':   j.time_taken_display,
                'output_bytes_display': j.output_bytes_display,
                'input_bytes':          None,
                'session_key':          j.session_key or 0,
            })
        successful_jobs = sum(
            1 for j in backup_jobs
            if j.status == BackupStatusValue.COMPLETED)
        failed_jobs = sum(
            1 for j in backup_jobs
            if j.status in (BackupStatusValue.FAILED,
                            BackupStatusValue.INTERRUPTED))
        today_jobs = sum(
            1 for j in backup_jobs
            if j.start_time and j.start_time.date() == today)
        running_jobs = sum(
            1 for j in backup_jobs
            if j.status == BackupStatusValue.RUNNING)
    else:
        # ── Fallback: schedule entries when RMAN Catalog unavailable ──────
        entries = _make_schedule_report_use_case().execute(
            from_date=from_date, to_date=to_date, days=days,
        )
        if form.is_valid():
            cd = form.cleaned_data
            if cd.get('policy_name'):
                entries = [e for e in entries if cd['policy_name'].lower() in (
                    e.policy_name or '').lower()]
            if cd.get('hostname'):
                entries = [e for e in entries if cd['hostname'].lower()
                           in (e.hostname or '').lower()]
            if cd.get('db_name'):
                entries = [e for e in entries if cd['db_name'].lower()
                           in (e.db_name or '').lower()]
            if cd.get('backup_type'):
                entries = [e for e in entries if cd['backup_type'].lower() in (
                    e.backup_type or '').lower()]
        if status_filter:
            entries = [
                e for e in entries
                if status_filter.upper() == 'SCHEDULED'
            ]
        jobs_data = [
            {
                'policy_name':          e.policy_name or '-',
                'hostname':             e.hostname or '-',
                'db_name':              e.db_name or '-',
                'backup_type':          e.backup_type or '-',
                'start_time':           e.schedule_start,
                'end_time':             None,
                'status':               'SCHEDULED',
                'elapsed_seconds':      None,
                'time_taken_display':   None,
                'output_bytes_display': None,
                'input_bytes':          None,
                'session_key':          e.id_schedule,
            }
            for e in entries
        ]
        today = datetime.date.today()
        successful_jobs = 0
        failed_jobs = 0
        running_jobs = 0
        today_jobs = sum(
            1 for e in entries
            if e.schedule_start.date() == today)

    all_policies = BackupPolicy.objects.values_list(
        'policy_name', flat=True).distinct().order_by('policy_name')
    all_hosts = Host.objects.values_list(
        'hostname', flat=True).distinct().order_by('hostname')
    all_databases = Database.objects.values_list(
        'db_name', flat=True).distinct().order_by('db_name')
    all_backup_types = BackupPolicy.objects.values_list(
        'backup_type', flat=True).distinct().order_by('backup_type')

    context = {
        'jobs':             jobs_data,
        'form':             form,
        'oracle_available': oracle_available,
        'successful_jobs':  successful_jobs,
        'failed_jobs':      failed_jobs,
        'today_jobs':       today_jobs,
        'running_jobs':     running_jobs,
        'all_policies':     all_policies,
        'all_hosts':        all_hosts,
        'all_databases':    all_databases,
        'all_backup_types': all_backup_types,
    }
    return render(request, "reports.html", context)


@login_required
def report_read_log_detail(request, idPolicy, dbKey, sessionKey):
    """Backup session log detail view.

    Fetches:
    - ``policyDetail`` — BackupPolicy ORM instance for metadata
    - ``execDetail``   — BackupJobResult entity (RC_BACKUP_JOB_DETAILS)
    - ``reportLog``    — list of BackupLogEntry entities (RC_RMAN_OUTPUT)

    Renders gracefully when Oracle catalog is unavailable.
    """
    from coreRelback.models import BackupPolicy

    try:
        policy = BackupPolicy.objects.select_related(
            'client', 'host', 'database'
        ).get(pk=idPolicy)
    except BackupPolicy.DoesNotExist:
        policy = None

    log_client_id = policy.client_id if policy else None
    detail_result = GetBackupDetailUseCase(_get_rman_repo()).execute(
        db_key=dbKey, session_key=sessionKey, client_id=log_client_id
    )

    context = {
        "idPolicy": idPolicy,
        "dbKey": dbKey,
        "sessionKey": sessionKey,
        "policyDetail": policy,
        "execDetail": detail_result["exec_detail"],
        "reportLog": detail_result["report_log"],
        "oracle_available": detail_result["oracle_available"],
    }
    return render(request, "reportsReadLog.html", context)


# ---------------------------
# AUTH VIEWS
# ---------------------------

def register_view(request):
    """Public view to create a new RelbackUser account.

    Uses RelbackUserCreationForm (forms.py) which handles password hashing
    and sets status=1 (active) by default.
    After successful registration the user is redirected to the login page.
    """
    from coreRelback.forms import RelbackUserCreationForm

    if request.method == 'POST':
        form = RelbackUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Account created successfully. Please sign in.")
            return redirect('coreRelback:login')
    else:
        form = RelbackUserCreationForm()
    return render(request, 'auth/register.html', {'form': form})
