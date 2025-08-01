<<<<<<< HEAD
# Imported from Django
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from django.core import serializers
from django.forms.models import model_to_dict
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.http import JsonResponse
from django.views.generic import TemplateView, View, DeleteView

# Imported from project relBack

# Forms from relBack
from .forms import formClient, formHost, formDatabase, formPolicies, RelbackLoginForm, RelbackUserCreationForm

# Models from relBack
from .models import Client, Host, Database, BackupPolicy, VwRmanBackupJobDetails, RelbackUser

# Debug ipdb
from django.http import HttpResponse
import ipdb

# Views de Autenticação
class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('coreRelback:index')
        form = RelbackLoginForm()
        return render(request, 'auth/login.html', {'form': form})
    
    def post(self, request):
        form = RelbackLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.user_cache
            login(request, user)
            
            # Get RelbackUser for the welcome message
            try:
                relback_user = RelbackUser.objects.get(username=user.username)
                welcome_name = relback_user.name or user.username
            except RelbackUser.DoesNotExist:
                welcome_name = user.username
                
            messages.success(request, f'Welcome, {welcome_name}!')
            next_url = request.GET.get('next', 'coreRelback:index')
            return redirect(next_url)
        return render(request, 'auth/login.html', {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, 'Successfully logged out!')
        return redirect('coreRelback:login')

class RegisterView(View):
    def get(self, request):
        form = RelbackUserCreationForm()
        return render(request, 'auth/register.html', {'form': form})
    
    def post(self, request):
        form = RelbackUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('coreRelback:index')
        return render(request, 'auth/register.html', {'form': form})
=======
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Client, Host, Database, BackupPolicy
# Outras importações se forem necessárias, como Schedule ou modelos de relatório
>>>>>>> 811bf09f982df832f56f799820e3f43d02b7aae7

# Função para a página inicial
def index(request):
<<<<<<< HEAD
    context = {}
    
    # If user is authenticated, get stats and RelbackUser data
    if request.user.is_authenticated:
        # Get RelbackUser instance
        try:
            relback_user = RelbackUser.objects.get(username=request.user.username)
            context['relback_user'] = relback_user
        except RelbackUser.DoesNotExist:
            pass
            
        context.update({
            'clients_count': Client.objects.count(),
            'hosts_count': Host.objects.count(),
            'databases_count': Database.objects.count(),
            'policies_count': BackupPolicy.objects.count(),
        })
    
    return render(request, 'index.html', context)
=======
    return render(request, "index.html")
>>>>>>> 811bf09f982df832f56f799820e3f43d02b7aae7

# Função para a página dos criadores
def creators(request):
<<<<<<< HEAD
    return render(request, 'creators.html')

# CRUD - Client - Initial

class clients(LoginRequiredMixin, TemplateView):
    template_name = 'clients.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clients'] = Client.objects.all().order_by('name')
        return context

class clientCreate(LoginRequiredMixin, View):
    def post(self, request):
        clientName = request.POST.get('name', None)
        description = request.POST.get('description', None)
        
        # Criar um usuário temporário se não existir
        try:
            temp_user, created = RelbackUser.objects.get_or_create(
                username='temp_user',
                defaults={
                    'name': 'Temporary User',
                    'email': 'temp@example.com',
                    'password': 'temp_password'
                }
            )
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        if not clientName:
            return JsonResponse({'error': 'Nome é obrigatório'}, status=400)

        try:
            obj = Client.objects.create(
                name=clientName,
                description=description or '',
                created_by=temp_user,
                updated_by=temp_user
            )

            client = {'id_client': obj.id_client, 'name': obj.name, 'description': obj.description}

            data = {
                'client': client,
                'success': True
            }
            return JsonResponse(data)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class clientUpdate(View):
    def post(self, request):
        idclient = request.POST.get('idClient', None)
        name = request.POST.get('name', None)
        description = request.POST.get('description', None)

        try:
            temp_user, created = RelbackUser.objects.get_or_create(
                username='temp_user',
                defaults={
                    'name': 'Temporary User',
                    'email': 'temp@example.com',
                    'password': 'temp_password'
                }
            )
            
            obj = Client.objects.get(pk=idclient)
            obj.name = name
            obj.description = description
            obj.updated_by = temp_user
            obj.save()

            client = {'id_client': obj.id_client, 'name': obj.name, 'description': obj.description}

            data = {
                'client': client,
                'success': True
            }
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class clientDelete(View):
    def post(self, request):
        pass

# CRUD - Clients - End

# CRUD - Hosts - Initial

class hostRead(LoginRequiredMixin, TemplateView):
    template_name = 'hosts.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hosts'] = Host.objects.all().order_by('id_host')
        context['clients'] = Client.objects.all().order_by('name')
        return context

class hostCreate(View):
    def get(self, request):
        idClient = request.GET.get('id_client', None)
        hostname = request.GET.get('hostname', None)
        ip = request.GET.get('ip', None)
        description = request.GET.get('description', None)

        # Get a user for created_by field
        user = RelbackUser.objects.first()
        if not user:
            user = RelbackUser.objects.create(
                name="System Admin",
                username="admin",
                password="temp_password",
                email="admin@relback.com"
            )

        obj = Host.objects.create(
            client_id=idClient,
            hostname=hostname,
            ip=ip,
            description=description,
            created_by=user,
        )

        host = {'id_host':obj.id_host, 'id_client':obj.client.id_client, 'client_name':obj.client.name, 'hostname':obj.hostname, 'ip':obj.ip, 'description':obj.description}

        data = {
            'host': host
        }
        # ipdb.set_trace()

        return JsonResponse(data)
    
    def post(self, request):
        try:
            name = request.POST.get('name')
            address = request.POST.get('address')
            client_id = request.POST.get('client')
            
            # Validações básicas
            if not name or not address or not client_id:
                return JsonResponse({'success': False, 'error': 'Todos os campos obrigatórios devem ser preenchidos'})
            
            # Verificar se o cliente existe
            try:
                client = Client.objects.get(id_client=client_id)
            except Client.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Cliente não encontrado'})
            
            # Criar o host (assumindo que temos um usuário padrão para created_by)
            # Você pode ajustar isso conforme sua lógica de autenticação
            user = RelbackUser.objects.first()  # ou request.user se tiver autenticação
            
            obj = Host.objects.create(
                hostname=name,
                ip=address,
                description='',  # Pode adicionar campo description no form se necessário
                client=client,
                created_by=user,
                updated_by=user
            )
            
            return JsonResponse({'success': True, 'message': 'Host criado com sucesso'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Erro interno: {str(e)}'})

class hostUpdate(View):
    def  get(self, request):
        idhost = request.GET.get('idHost', None)
        idclient = request.GET.get('idClient', None)
        hostname = request.GET.get('hostname', None)
        ip = request.GET.get('ip', None)
        description = request.GET.get('description', None)

        obj = Host.objects.get(pk=idhost)
        obj.client = Client.objects.get(id_client=idclient)
        obj.hostname = hostname
        obj.ip = ip
        obj.description = description

        # ipdb.set_trace()

        obj.save()

        host = {'id_host':obj.id_host, 'id_client':obj.client.id_client, 'hostname':obj.hostname, 'ip':obj.ip, 'description':obj.description}

        data = {
            'host': host
        }
        return JsonResponse(data)
    
    def post(self, request):
        try:
            id_host = request.POST.get('id_host')
            name = request.POST.get('name')
            address = request.POST.get('address')
            client_id = request.POST.get('client')
            
            # Validações básicas
            if not id_host or not name or not address or not client_id:
                return JsonResponse({'success': False, 'error': 'Todos os campos obrigatórios devem ser preenchidos'})
            
            # Verificar se o host existe
            try:
                host = Host.objects.get(id_host=id_host)
            except Host.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Host não encontrado'})
            
            # Verificar se o cliente existe
            try:
                client = Client.objects.get(id_client=client_id)
            except Client.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Cliente não encontrado'})
            
            # Atualizar o host
            user = RelbackUser.objects.first()  # ou request.user se tiver autenticação
            
            host.hostname = name
            host.ip = address
            host.client = client
            host.updated_by = user
            host.save()
            
            return JsonResponse({'success': True, 'message': 'Host atualizado com sucesso'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Erro interno: {str(e)}'})

class hostDelete(View):
    def get(self, request):
        id_host = request.GET.get('id_host', None)
        Host.objects.get(pk=id_host).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)
    
    def post(self, request):
        try:
            id_host = request.POST.get('id_host')
            
            if not id_host:
                return JsonResponse({'success': False, 'error': 'ID do host é obrigatório'})
            
            # Verificar se o host existe
            try:
                host = Host.objects.get(id_host=id_host)
            except Host.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Host não encontrado'})
            
            # Deletar o host
            host.delete()
            
            return JsonResponse({'success': True, 'message': 'Host excluído com sucesso'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Erro interno: {str(e)}'})

# CRUD - Hosts - End

# CRUD - Databases - Initial

class databaseRead(LoginRequiredMixin, TemplateView):
    template_name = 'databases.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['hosts'] = Host.objects.all().order_by('hostname')
        context['clients'] = Client.objects.all().order_by('name')
        context['databases'] = Database.objects.all().order_by('id_database')

        return context

class databaseCreate(View):
    def post(self, request):
        idClient = request.POST.get('id_client', None)
        idHost = request.POST.get('id_host', None)
        dbName = request.POST.get('db_name', None)
        dbId = request.POST.get('dbid', None)
        description = request.POST.get('description', None)

        try:
            temp_user, created = RelbackUser.objects.get_or_create(
                username='temp_user',
                defaults={
                    'name': 'Temporary User',
                    'email': 'temp@example.com',
                    'password': 'temp_password'
                }
            )
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        if not (idClient and idHost and dbName and dbId):
            return JsonResponse({'error': 'Todos os campos obrigatórios devem ser preenchidos.'}, status=400)

        try:
            obj = Database.objects.create(
                client_id=idClient,
                host_id=idHost,
                db_name=dbName,
                dbid=dbId,
                description=description or '',
                created_by=temp_user,
                updated_by=temp_user
            )

            database = {
                'id_database': obj.id_database,
                'id_client': obj.client_id,
                'client_name': obj.client.name,
                'id_host': obj.host_id,
                'hostname': obj.host.hostname,
                'dbname': obj.db_name,
                'dbid': obj.dbid,
                'description': obj.description
            }

            data = {
                'database': database,
                'success': True
            }
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class databaseUpdate(View):
    def  get(self, request):
        idDatabase = request.GET.get('id_database', None)
        idClient = request.GET.get('id_client', None)
        idHost = request.GET.get('id_host', None)
        dbName = request.GET.get('db_name', None)
        dbId = request.GET.get('db_id', None)
        description = request.GET.get('description', None)

        obj = Database.objects.get(pk=idDatabase)
        obj.client = Client.objects.get(id_client=idClient)
        obj.host = Host.objects.get(id_host=idHost)
        obj.db_name = dbName
        obj.dbid = dbId
        obj.description = description

        # ipdb.set_trace()

        obj.save()

        database = {'id_database':obj.id_database
                    , 'id_client':obj.client.id_client
                    , 'client_name':obj.client.name
                    , 'id_host':obj.host.id_host
                    , 'hostname':obj.host.hostname
                    , 'db_name':obj.db_name
                    , 'dbid':obj.dbid
                    , 'description':obj.description
                    }

        data = {
            'database': database
        }
        return JsonResponse(data)

def hostsList(request):
    id_client = request.GET.get('id_client', None)
    clientHosts = serializers.serialize('json'
                                        , list(Host.objects.filter(client_id=id_client).order_by('hostname'))
                                        , fields=('id_host','hostname'))
    return JsonResponse({'hosts': clientHosts})

def databasesList(request):
    id_client = request.GET.get('id_client', None)
    id_host = request.GET.get('id_host', None)
    databases = serializers.serialize(
        'json',
        list(Database.objects.filter(client_id=id_client, host_id=id_host).order_by('db_name')),
        fields=('id_database', 'db_name')
    )
    return JsonResponse({'databases': databases})


class databaseDelete(View):
    def get(self, request):
        id_database = request.GET.get('id_database', None)
        Database.objects.get(pk=id_database).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)

    def post(self, request):
        id_database = request.POST.get('id_database', None)
        try:
            Database.objects.get(pk=id_database).delete()
            data = {
                'deleted': True,
                'success': True
            }
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'error': str(e), 'success': False}, status=400)

# CRUD - Databases - End

# CRUD - Policies - Initial

class policyRead(LoginRequiredMixin, TemplateView):
    template_name = 'policies.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['hosts'] = Host.objects.all().order_by('hostname')
        context['clients'] = Client.objects.all().order_by('name')
        context['databases'] = Database.objects.all().order_by('db_name')
        context['policies'] = BackupPolicy.objects.all().order_by('policy_name')

        return context

    def policyDetail(request):

        idPolicy = request.GET.get('id_policy', None)

        obj = BackupPolicy.objects.get(pk=idPolicy)

        policy = {
                'id_policy':obj.id_policy
                , 'policy_name':obj.policy_name
                , 'id_client':obj.client.id_client
                , 'client_name':obj.client.name
                , 'id_host':obj.host.id_host
                , 'hostname':obj.host.hostname  
                , 'id_database':obj.database.id_database                
                , 'db_name':obj.database.db_name
                , 'backup_type':obj.backup_type
                , 'destination':obj.destination
                , 'minute':obj.minute 
                , 'hour':obj.hour 
                , 'day':obj.day 
                , 'month':obj.month 
                , 'day_week':obj.day_week 
                , 'duration':obj.duration 
                , 'size_backup':obj.size_backup
                , 'status':obj.status
                , 'description':obj.description
        }

        data = {
            'policy': policy
        }

        return JsonResponse(data)


class policyCreate(View):
    def get(self, request):
        pass

    def post(self, request):
        idClient = request.POST.get('id_client', None)
        idHost = request.POST.get('id_host', None)
        idDatabase = request.POST.get('id_database', None)
        policyName = request.POST.get('policy_name', None)
        backupType = request.POST.get('backup_type', None)
        destination = request.POST.get('destination', None)
        minute = request.POST.get('minute', None)
        hour = request.POST.get('hour', None)
        day = request.POST.get('day', None)
        month = request.POST.get('month', None)
        dayWeek = request.POST.get('day_week', None)
        duration = request.POST.get('duration', None)
        sizeBackup = request.POST.get('size_backup', None)
        status = request.POST.get('status', None)
        description = request.POST.get('description', None)

        # Get current RelbackUser
        try:
            relback_user = RelbackUser.objects.get(username=request.user.username)
        except RelbackUser.DoesNotExist:
            # Fallback to first user if association doesn't exist
            relback_user = RelbackUser.objects.first()
            if not relback_user:
                # Create a default user if none exists
                relback_user = RelbackUser.objects.create(
                    name="System Admin",
                    username="admin",
                    password="temp_password",
                    email="admin@relback.com"
                )

        # Get the objects by ID
        client_obj = Client.objects.get(id_client=idClient)
        host_obj = Host.objects.get(id_host=idHost)
        database_obj = Database.objects.get(id_database=idDatabase)

        obj = BackupPolicy.objects.create(
            policy_name=policyName,
            client=client_obj,
            host=host_obj,
            database=database_obj,
            backup_type=backupType,
            destination=destination,
            minute=minute,
            hour=hour,
            day=day,
            month=month,
            day_week=dayWeek,
            duration=duration,
            size_backup=sizeBackup,
            status=status,
            description=description,
            created_by=relback_user,
        )

        policy = {
            'id_policy': obj.id_policy,
            'policy_name': obj.policy_name,
            'id_client': obj.client.id_client,
            'client_name': obj.client.name,
            'id_host': obj.host.id_host,
            'hostname': obj.host.hostname,
            'id_database': obj.database.id_database,
            'dbname': obj.database.db_name,
            'backup_type': obj.backup_type,
            'destination': obj.destination,
            'minute': obj.minute,
            'hour': obj.hour,
            'day': obj.day,
            'month': obj.month,
            'day_week': obj.day_week,
            'duration': obj.duration,
            'size_backup': obj.size_backup,
            'status': status,
            'description': obj.description
        }

        data = {
            'policy': policy
        }
        return JsonResponse(data)

class policyUpdate(View):
    def  get(self, request):
        idPolicy = request.GET.get('id_policy', None)
        idClient = request.GET.get('id_client', None)
        idHost = request.GET.get('id_host', None)
        idDatabase = request.GET.get('id_database', None)
        policyName = request.GET.get('policy_name', None)
        backupType = request.GET.get('backup_type', None)
        destination = request.GET.get('destination', None)
        minute = request.GET.get('minute', None)
        hour = request.GET.get('hour', None)
        day = request.GET.get('day', None)
        month = request.GET.get('month', None)
        dayWeek = request.GET.get('day_week', None)
        duration = request.GET.get('duration', None)
        sizeBackup = request.GET.get('size_backup', None)
        status = request.GET.get('status', None)               
        description = request.GET.get('description', None)

        obj = BackupPolicy.objects.get(pk=idPolicy)
        obj.database = Database.objects.get(id_database=idDatabase)
        obj.client = Client.objects.get(id_client=idClient)
        obj.host = Host.objects.get(id_host=idHost)
        obj.policy_name = policyName
        obj.backup_type = backupType
        obj.destination = destination
        obj.minute = minute
        obj.hour = hour
        obj.day = day
        obj.day_week = dayWeek
        obj.month = month
        obj.duration = duration
        obj.size_backup = sizeBackup
        obj.status = status
        obj.description = description

        # import ipdb
        # ipdb.set_trace()

        obj.save()

        policy = {'id_policy':obj.id_policy
                    , 'policy_name':obj.policy_name
                    , 'id_client':obj.id_client_id
                    , 'client_name':obj.id_client.name
                    , 'id_host':obj.id_host_id
                    , 'hostname':obj.id_host.hostname  
                    , 'id_database':obj.id_database_id                
                    , 'dbname':obj.id_database.db_name
                    , 'backup_type':obj.backup_type
                    , 'destination':obj.destination
                    , 'minute':obj.minute 
                    , 'hour':obj.hour 
                    , 'day':obj.day 
                    , 'month':obj.month 
                    , 'day_week':obj.day_week 
                    , 'duration':obj.duration 
                    , 'size_backup':obj.size_backup
                    , 'status':status
                    , 'description':obj.description}

        data = {
            'policy': policy
        }

        return JsonResponse(data)

class policyDelete(View):
    def get(self, request):
        id_policy = request.GET.get('id_policy', None)
        BackupPolicy.objects.get(pk=id_policy).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)

# CRUD - Policies - End

def dictfetchall(cursor):
    # "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def reportRead(request):
    cursor = connection.cursor()
    resultQueryReportRead = cursor.execute("""select
                        to_number(pbv.id_policy) as id_policy,
                        upper(substr(pbv.hostname,1,30)) as hostname,
                        upper(pbv.db_name) as db_name,
                        rd.db_key as db_key,
                        to_char(pbv.schedule_start, 'dd/mm/yy hh24:mi') as schedule_start,
                        to_char(bjd.start_time, 'dd/mm/yy hh24:mi') as start_r,
                        case 
                        when bjd.status is null and pbv.schedule_start > sysdate then 'SCHEDULED' 
                        when bjd.status is null and bjd.start_time is null and pbv.schedule_start < (select max(r.resync_time) as last_resync from vw_rman_resync r where r.db_key = rd.db_key and upper(r.db_name) = upper(pbv.db_name)) then 'NOT RUN'
                        when bjd.status is null and bjd.start_time is null and pbv.schedule_start > (select max(r.resync_time) as last_resync from vw_rman_resync r where r.db_key = rd.db_key and upper(r.db_name) = upper(pbv.db_name)) then 'NO RESYNC'
                        when bjd.status is not null then bjd.status
                        end as status,
                        bjd.time_taken_display as duration_r,
                        TO_CHAR(TRUNC(pbv.duration/3600),'FM9900') || ':' ||
                        TO_CHAR(TRUNC(MOD(pbv.duration,3600)/60),'FM00') || ':' ||
                        TO_CHAR(MOD(pbv.duration,60),'FM00') as duration_e,
                        round(output_bytes/1024/1024/1024, 2) as size_r_gb,
                        trunc(decode(substr(pbv.size_backup,-1,1),'M',
                        to_number(substr(pbv.size_backup,1,    length(pbv.size_backup)-1)/1024),
                        'G',to_number(substr(pbv.size_backup,1,length(pbv.size_backup)-1)),
                        'T',to_number(substr(pbv.size_backup,1,length(pbv.size_backup)-1*1024))),2) as size_p_gb,
                        pbv.destination as destination,
                        pbv.backup_type as backup_type,
                        bjd.session_key as session_key,
                        pbv.description as description
                    from
                        relback.vw_rman_backup_job_details bjd
                        right outer join relback.vw_backup_policies pbv on (
                        upper(bjd.db_name)                                                            = upper(pbv.db_name)          and
                        upper(bjd.dbid)                                                               = upper(pbv.dbid)             and
                        upper(decode(bjd.output_device_type,null,'SBT_TAPE',bjd.output_device_type))  = upper(pbv.destination)  	and
                        upper(bjd.input_type)                                                         = upper(pbv.backup_type)      and 
                        bjd.start_time between  pbv.schedule_start - 1/24/4 and
                                    pbv.schedule_start + 1/24/4)
                        right join relback.vw_rman_database rd on (rd.dbid = pbv.dbid)
                    where
                        trunc(pbv.schedule_start) between trunc(sysdate) - 7 and trunc(sysdate)
                        order by pbv.schedule_start desc""")
    # ipdb.set_trace()
    # return HttpResponse(dictfetchall(resultQueryReportRead))
    return render(request, 'reports.html', {'report':dictfetchall(resultQueryReportRead)})

def reportReadLogDetail(request, idPolicy, dbKey, sessionKey):

    # reportLog = VwRmanOutput.objects.filter(db_key=dbKey, session_key=sessionKey)
    reportLog = []  # Temporário até a view VwRmanOutput ser criada

    execDetail = VwRmanBackupJobDetails.objects.filter(db_key=dbKey, session_key=sessionKey)

    policyDetail = BackupPolicy.objects.get(id_policy=idPolicy)

    return render(request, 'reportsReadLog.html', {'reportLog':reportLog, 'execDetail':execDetail, 'policyDetail':policyDetail})

def reportRefreshSchedule(request):

    with connection.cursor() as cursor:
        cursor.callproc('SP_CREATE_SCHEDULE')

    return reportRead(request)
=======
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
>>>>>>> 811bf09f982df832f56f799820e3f43d02b7aae7
