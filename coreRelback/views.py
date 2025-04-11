from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Client, Host, Database, BackupPolicy
# Outras importações se forem necessárias, como Schedule ou modelos de relatório

# Função para a página inicial
def index(request):
    return render(request, "coreRelback/index.html")

# Função para a página dos criadores
def creators(request):
    return render(request, "coreRelback/creators.html")

# ---------------------------
# VIEWS PARA CLIENTS
# ---------------------------
class ClientListView(ListView):
    model = Client
    template_name = "coreRelback/clients.html"
    context_object_name = "clients"

class ClientCreateView(CreateView):
    model = Client
    template_name = "coreRelback/client_form.html"
    fields = ['name', 'description']  # ajuste os campos conforme o seu modelo
    success_url = reverse_lazy('coreRelback:client-list')

class ClientUpdateView(UpdateView):
    model = Client
    template_name = "coreRelback/client_form.html"
    fields = ['name', 'description']
    success_url = reverse_lazy('coreRelback:client-list')

class ClientDeleteView(DeleteView):
    model = Client
    template_name = "coreRelback/client_confirm_delete.html"
    success_url = reverse_lazy('coreRelback:client-list')

# ---------------------------
# VIEWS PARA HOSTS
# ---------------------------
class HostListView(ListView):
    model = Host
    template_name = "coreRelback/hosts.html"
    context_object_name = "hosts"

class HostCreateView(CreateView):
    model = Host
    template_name = "coreRelback/host_form.html"
    fields = ['hostname', 'description', 'ip', 'client']
    success_url = reverse_lazy('coreRelback:host-list')

class HostUpdateView(UpdateView):
    model = Host
    template_name = "coreRelback/host_form.html"
    fields = ['hostname', 'description', 'ip', 'client']
    success_url = reverse_lazy('coreRelback:host-list')

class HostDeleteView(DeleteView):
    model = Host
    template_name = "coreRelback/host_confirm_delete.html"
    success_url = reverse_lazy('coreRelback:host-list')

# ---------------------------
# VIEWS PARA DATABASES
# ---------------------------
class DatabaseListView(ListView):
    model = Database
    template_name = "coreRelback/databases.html"
    context_object_name = "databases"

class DatabaseCreateView(CreateView):
    model = Database
    template_name = "coreRelback/database_form.html"
    fields = ['db_name', 'description', 'client', 'host', 'dbid']
    success_url = reverse_lazy('coreRelback:database-list')

class DatabaseUpdateView(UpdateView):
    model = Database
    template_name = "coreRelback/database_form.html"
    fields = ['db_name', 'description', 'client', 'host', 'dbid']
    success_url = reverse_lazy('coreRelback:database-list')

class DatabaseDeleteView(DeleteView):
    model = Database
    template_name = "coreRelback/database_confirm_delete.html"
    success_url = reverse_lazy('coreRelback:database-list')

# Função de exemplo: lista de hosts vinculados a um determinado database
def database_hosts_list(request, pk):
    database = get_object_or_404(Database, pk=pk)
    hosts = Host.objects.filter(client=database.client)
    context = {'database': database, 'hosts': hosts}
    return render(request, "coreRelback/database_hosts_list.html", context)

# ---------------------------
# VIEWS PARA BACKUP POLICIES
# ---------------------------
class BackupPolicyListView(ListView):
    model = BackupPolicy
    template_name = "coreRelback/policies.html"
    context_object_name = "policies"

class BackupPolicyCreateView(CreateView):
    model = BackupPolicy
    template_name = "coreRelback/policy_form.html"
    fields = ['policy_name', 'client', 'database', 'host', 'backup_type', 'destination',
              'minute', 'hour', 'day', 'month', 'day_week', 'duration', 'size_backup', 'status', 'description']
    success_url = reverse_lazy('coreRelback:policy-list')

class BackupPolicyUpdateView(UpdateView):
    model = BackupPolicy
    template_name = "coreRelback/policy_form.html"
    fields = ['policy_name', 'client', 'database', 'host', 'backup_type', 'destination',
              'minute', 'hour', 'day', 'month', 'day_week', 'duration', 'size_backup', 'status', 'description']
    success_url = reverse_lazy('coreRelback:policy-list')

class BackupPolicyDeleteView(DeleteView):
    model = BackupPolicy
    template_name = "coreRelback/policy_confirm_delete.html"
    success_url = reverse_lazy('coreRelback:policy-list')

# Se a detail for necessária (por exemplo, para visualização detalhada de uma política)
class BackupPolicyDetailView(DetailView):
    model = BackupPolicy
    template_name = "coreRelback/policy_detail.html"

# Funções para extras na área de relatórios
def report_read(request):
    # Implemente sua lógica para relatórios
    return render(request, "coreRelback/reports.html")

def report_read_log_detail(request, idPolicy, dbKey, sessionKey):
    # Exemplo: obtenha detalhes a partir dos parâmetros e passe para o template
    context = {"idPolicy": idPolicy, "dbKey": dbKey, "sessionKey": sessionKey}
    return render(request, "coreRelback/reportsReadLog.html", context)

def report_refresh_schedule(request):
    # Lógica para atualizar agendamentos (exemplo)
    # Depois redirecione para a página de relatórios
    return redirect('coreRelback:report-read')
