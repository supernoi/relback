from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Client, Host, Database, BackupPolicy, RelbackUser


# Função para a página inicial
def index(request):
    return render(request, "index.html")

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
    fields = ['name', 'description']  # ajuste os campos conforme o seu modelo
    success_url = reverse_lazy('coreRelback:client-list')

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

# Funções para extras na área de relatórios
def report_read(request):
    # Implemente sua lógica para relatórios
    return render(request, "reports.html")

def report_read_log_detail(request, idPolicy, dbKey, sessionKey):
    # Exemplo: obtenha detalhes a partir dos parâmetros e passe para o template
    context = {"idPolicy": idPolicy, "dbKey": dbKey, "sessionKey": sessionKey}
    return render(request, "reportsReadLog.html", context)

def report_refresh_schedule(request):
    # Lógica para atualizar agendamentos (exemplo)
    # Depois redirecione para a página de relatórios
    return redirect('coreRelback:report-read')


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
>>>>>>> 811bf09f982df832f56f799820e3f43d02b7aae7
