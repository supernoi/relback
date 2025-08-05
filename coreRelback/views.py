from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Client, Host, Database, BackupPolicy, RelbackUser, Schedule
from coreRelback.services.schedule_generator import generate_schedules
from django import forms


# Função para a página inicial
def index(request):
    context = {
        'clients_count': Client.objects.count(),
        'hosts_count': Host.objects.count(),
        'databases_count': Database.objects.count(),
        'policies_count': BackupPolicy.objects.count(),
    }
    return render(request, "index.html", context)


# Função para a página dos criadores
def creators(request):
    return render(request, "creators.html")


# ---------------------------
# VIEWS PARA CLIENTS
# ---------------------------
class ClientListView(ListView):
    model = Client
    template_name = "clients.html"
    context_object_name = "clients"


class ClientCreateView(CreateView):

    model = Client
    template_name = "client_form.html"
    fields = ['name', 'description']
    success_url = reverse_lazy('coreRelback:client-list')

    def form_valid(self, form):
        # Busca o RelbackUser relacionado ao usuário logado
        from .models import RelbackUser
        try:
            relback_user = RelbackUser.objects.get(username=self.request.user.username)
            form.instance.created_by = relback_user
        except RelbackUser.DoesNotExist:
            form.add_error(None, "Usuário não possui perfil RelbackUser cadastrado.")
            return self.form_invalid(form)
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Client
    template_name = "client_form.html"
    fields = ['name', 'description']
    success_url = reverse_lazy('coreRelback:client-list')


class ClientDeleteView(DeleteView):
    model = Client
    template_name = "client_confirm_delete.html"
    success_url = reverse_lazy('coreRelback:client-list')


# ---------------------------
# VIEWS PARA HOSTS
# ---------------------------
class HostListView(ListView):
    model = Host
    template_name = "hosts.html"
    context_object_name = "hosts"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hosts = self.get_queryset().select_related('client')
        
        # Estatísticas para os cards (removendo filtro por status que não existe)
        context['total_hosts'] = hosts.count()
        context['active_hosts'] = hosts.count()  # Assumindo que todos hosts listados estão ativos
        context['total_clients'] = Client.objects.count()
        context['total_databases'] = Database.objects.filter(host__in=hosts).count()
        context['clients'] = Client.objects.all()  # Para o filtro
        
        return context


class HostCreateView(CreateView):
    model = Host
    template_name = "host_form.html"
    fields = ['hostname', 'description', 'ip', 'client']
    success_url = reverse_lazy('coreRelback:host-list')


class HostUpdateView(UpdateView):
    model = Host
    template_name = "host_form.html"
    fields = ['hostname', 'description', 'ip', 'client']
    success_url = reverse_lazy('coreRelback:host-list')


class HostDeleteView(DeleteView):
    model = Host
    template_name = "host_confirm_delete.html"
    success_url = reverse_lazy('coreRelback:host-list')


# ---------------------------
# VIEWS PARA DATABASES
# ---------------------------
class DatabaseListView(ListView):
    model = Database
    template_name = "databases.html"
    context_object_name = "databases"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        databases = self.get_queryset().select_related('client', 'host')
        
        # Estatísticas para os cards (removendo filtro por active que não existe)
        context['total_databases'] = databases.count()
        context['active_databases'] = databases.count()  # Assumindo que todos databases listados estão ativos
        context['total_hosts'] = Host.objects.count()
        context['total_policies'] = BackupPolicy.objects.filter(database__in=databases).count()
        
        return context


class DatabaseCreateView(CreateView):
    model = Database
    template_name = "database_form.html"
    fields = ['db_name', 'description', 'client', 'host', 'dbid']
    success_url = reverse_lazy('coreRelback:database-list')


class DatabaseUpdateView(UpdateView):
    model = Database
    template_name = "database_form.html"
    fields = ['db_name', 'description', 'client', 'host', 'dbid']
    success_url = reverse_lazy('coreRelback:database-list')


class DatabaseDeleteView(DeleteView):
    model = Database
    template_name = "database_confirm_delete.html"
    success_url = reverse_lazy('coreRelback:database-list')


# Função de exemplo: lista de hosts vinculados a um determinado database
def database_hosts_list(request, pk):
    database = get_object_or_404(Database, pk=pk)
    hosts = Host.objects.filter(client=database.client)
    context = {'database': database, 'hosts': hosts}
    return render(request, "database_hosts_list.html", context)


# ---------------------------
# VIEWS PARA BACKUP POLICIES
# ---------------------------
class BackupPolicyListView(ListView):
    model = BackupPolicy
    template_name = "policies.html"
    context_object_name = "policies"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        policies = self.get_queryset().select_related('client', 'database', 'host')
        
        # Estatísticas para os cards
        context['total_policies'] = policies.count()
        context['active_policies'] = policies.filter(status=1).count()
        context['inactive_policies'] = policies.filter(status=0).count()
        # Simulando políticas agendadas para hoje (você pode implementar a lógica real)
        context['scheduled_policies'] = policies.filter(status=1).count() // 2
        context['clients'] = Client.objects.all()  # Para o filtro
        
        return context


class BackupPolicyCreateView(CreateView):
    model = BackupPolicy
    template_name = "policy_form.html"
    fields = ['policy_name', 'client', 'database', 'host', 'backup_type', 'destination',
              'minute', 'hour', 'day', 'month', 'day_week', 'duration', 'size_backup', 'status', 'description']
    success_url = reverse_lazy('coreRelback:policy-list')


class BackupPolicyUpdateView(UpdateView):
    model = BackupPolicy
    template_name = "policy_form.html"
    fields = ['policy_name', 'client', 'database', 'host', 'backup_type', 'destination',
              'minute', 'hour', 'day', 'month', 'day_week', 'duration', 'size_backup', 'status', 'description']
    success_url = reverse_lazy('coreRelback:policy-list')


class BackupPolicyDeleteView(DeleteView):
    model = BackupPolicy
    template_name = "policy_confirm_delete.html"
    success_url = reverse_lazy('coreRelback:policy-list')


# Se a detail for necessária (por exemplo, para visualização detalhada de uma política)
class BackupPolicyDetailView(DetailView):
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
        relback_user.theme_preference = request.POST.get('theme_preference', relback_user.theme_preference)
        relback_user.language_preference = request.POST.get('language_preference', relback_user.language_preference)
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
    days = forms.IntegerField(label='Days', min_value=1, max_value=30, required=False, initial=2)
    start_date = forms.DateField(label='Start Date', required=False)
    end_date = forms.DateField(label='End Date', required=False)


def report_refresh_schedule(request):
    days = int(request.GET.get('days', 2))
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    from coreRelback.services.schedule_generator import generate_schedules
    import datetime
    
    if start_date and end_date:
        # Gerar para faixa específica
        start = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        current = start
        while current <= end:
            generate_schedules(current)
            current += datetime.timedelta(days=1)
    else:
        # Gerar para próximos dias (padrão: hoje + amanhã)
        reference_date = datetime.date.today()
        for i in range(days):
            generate_schedules(reference_date + datetime.timedelta(days=i))
    
    return redirect('coreRelback:report-read')


def report_read(request):
    form = ScheduleFilterForm(request.GET or None)
    jobs = Schedule.objects.select_related('backup_policy', 'backup_policy__database', 'backup_policy__host').order_by('schedule_start')
    
    # Filtros básicos
    if form.is_valid():
        if form.cleaned_data['policy_name']:
            jobs = jobs.filter(backup_policy__policy_name__icontains=form.cleaned_data['policy_name'])
        if form.cleaned_data['hostname']:
            jobs = jobs.filter(backup_policy__host__hostname__icontains=form.cleaned_data['hostname'])
        if form.cleaned_data['db_name']:
            jobs = jobs.filter(backup_policy__database__db_name__icontains=form.cleaned_data['db_name'])
        if form.cleaned_data['backup_type']:
            jobs = jobs.filter(backup_policy__backup_type__icontains=form.cleaned_data['backup_type'])
    
    # Filtro por parâmetros GET diretos (para campos de data)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date and end_date:
        # Filtrar por faixa de datas específica
        import datetime
        start = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        jobs = jobs.filter(schedule_start__date__gte=start, schedule_start__date__lte=end)
    elif not start_date and not end_date:
        # Padrão: mostrar próximos dias conforme seleção
        days = int(request.GET.get('days', 2))
        import datetime
        today = datetime.date.today()
        end_date_calc = today + datetime.timedelta(days=days-1)
        jobs = jobs.filter(schedule_start__date__gte=today, schedule_start__date__lte=end_date_calc)
    
    jobs_data = []
    for job in jobs:
        jobs_data.append({
            'policy_name': job.backup_policy.policy_name if job.backup_policy else '-',
            'hostname': job.backup_policy.host.hostname if job.backup_policy and job.backup_policy.host else '-',
            'db_name': job.backup_policy.database.db_name if job.backup_policy and job.backup_policy.database else '-',
            'backup_type': job.backup_policy.backup_type if job.backup_policy else '-',
            'start_time': job.schedule_start,
            'end_time': '-',
            'status': getattr(job.backup_policy, 'status', '-') if job.backup_policy else '-',
            'elapsed_seconds': '',
            'input_bytes': '',
            'session_key': job.id_schedule
        })
    # Prepare data for dropdown selects
    all_policies = BackupPolicy.objects.values_list('policy_name', flat=True).distinct().order_by('policy_name')
    all_hosts = Host.objects.values_list('hostname', flat=True).distinct().order_by('hostname')
    all_databases = Database.objects.values_list('db_name', flat=True).distinct().order_by('db_name')
    all_backup_types = BackupPolicy.objects.values_list('backup_type', flat=True).distinct().order_by('backup_type')
    
    context = {
        'jobs': jobs_data,
        'form': form,
        'successful_jobs': [],
        'failed_jobs': [],
        'running_jobs': [],
        'all_policies': all_policies,
        'all_hosts': all_hosts,
        'all_databases': all_databases,
        'all_backup_types': all_backup_types,
    }
    return render(request, "reports.html", context)


def report_read_log_detail(request, idPolicy, dbKey, sessionKey):
    # Exemplo: obtenha detalhes a partir dos parâmetros e passe para o template
    context = {"idPolicy": idPolicy, "dbKey": dbKey, "sessionKey": sessionKey}
    return render(request, "reportsReadLog.html", context)


def report_refresh_schedule(request):
    days = int(request.GET.get('days', 1))
    from coreRelback.services.schedule_generator import generate_schedules
    import datetime
    reference_date = datetime.date.today()
    for i in range(days):
        generate_schedules(reference_date + datetime.timedelta(days=i))
    return redirect('coreRelback:report-read')
