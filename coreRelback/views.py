# Imported from Django
from django.shortcuts import render, redirect
from django.db  import connection
from django.core import serializers

from django.http import JsonResponse
from django.views.generic import TemplateView, View, DeleteView

# Imported from project relBack

# Forms from relBack
from .forms import formClient, formHost, formDatabase, formPolicies

# Models from relBack
from .models import Clients, Hosts, Databases, BackupPolicies, VwRmanOutput, VwRmanBackupJobDetails

# Debug ipdb
from django.http import HttpResponse
# import ipdb
# ipdb.set_trace()

def index(request):
    return render(request, 'index.html')

def creators(request):
    return render(request, 'creators.html')

# CRUD - Client - Initial

class clientRead(TemplateView):
    template_name = 'clients.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clients'] = Clients.objects.all().order_by('name')
        return context

class clientCreate(View):
    def get(self, request):
        clientName = request.GET.get('clientName', None)
        description = request.GET.get('description', None)

        obj = Clients.objects.create(
            name=clientName,
            description=description,
        )

        client = {'id_client':obj.id_client, 'name':obj.name, 'description':obj.description}

        data = {
            'client': client
        }
        # ipdb.set_trace()

        return JsonResponse(data)

class clientUpdate(View):
    def  get(self, request):
        idclient = request.GET.get('idClient', None)
        name = request.GET.get('name', None)
        description = request.GET.get('description', None)

        obj = Clients.objects.get(pk=idclient)
        obj.name = name
        obj.description = description

        # ipdb.set_trace()

        obj.save()

        client = {'id_client':obj.id_client, 'name':obj.name, 'description':obj.description}

        data = {
            'client': client
        }
        return JsonResponse(data)

class clientDelete(View):
    def get(self, request):
        id_client = request.GET.get('id_client', None)
        Clients.objects.get(pk=id_client).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)

# CRUD - Clients - End

# CRUD - Hosts - Initial

class hostRead(TemplateView):
    template_name = 'hosts.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hosts'] = Hosts.objects.all().order_by('id_host')
        context['clients'] = Clients.objects.all().order_by('name')
        return context

class hostCreate(View):
    def get(self, request):
        idClient = request.GET.get('id_client', None)
        hostname = request.GET.get('hostname', None)
        ip = request.GET.get('ip', None)
        description = request.GET.get('description', None)

        obj = Hosts.objects.create(
            id_client_id=idClient,
            hostname=hostname,
            ip=ip,
            description=description,
        )

        host = {'id_host':obj.id_host, 'id_client':obj.id_client_id, 'client_name':obj.id_client.name, 'hostname':obj.hostname, 'ip':obj.ip, 'description':obj.description}

        data = {
            'host': host
        }
        # ipdb.set_trace()

        return JsonResponse(data)

class hostUpdate(View):
    def  get(self, request):
        idhost = request.GET.get('idHost', None)
        idclient = request.GET.get('idClient', None)
        hostname = request.GET.get('hostname', None)
        ip = request.GET.get('ip', None)
        description = request.GET.get('description', None)

        obj = Hosts.objects.get(pk=idhost)
        obj.id_client_id = idclient
        obj.hostname = hostname
        obj.ip = ip
        obj.description = description

        # ipdb.set_trace()

        obj.save()

        host = {'id_host':obj.id_host, 'id_client':obj.id_client_id, 'hostname':obj.hostname, 'ip':obj.ip, 'description':obj.description}

        data = {
            'host': host
        }
        return JsonResponse(data)

class hostDelete(View):
    def get(self, request):
        id_host = request.GET.get('id_host', None)
        Hosts.objects.get(pk=id_host).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)

# CRUD - Hosts - End

# CRUD - Databases - Initial

def databaseCreate(request):
    if request.method == 'POST':
        formCreateDatabase = formDatabase(request.POST)
        if formCreateDatabase.is_valid():
            formCreateDatabase.save()
    return redirect('coreRelback:database')

def databaseRead(request):
    clients = Clients.objects.all().order_by('pk')
    hosts = Hosts.objects.all().order_by('pk')
    databases = Databases.objects.all().order_by('pk')
    return render(request, 'databases.html', {'clients':clients, 'hosts':hosts, 'databases':databases})

def databaseUpdate(request, idDatabase):
    databaseIdSelect = Databases.objects.get(pk=idDatabase)
    if request.method == 'POST':
        formDatabaseUpdate = formDatabase(request.POST, instance=databaseIdSelect)
        if formDatabaseUpdate.is_valid():
            formDatabaseUpdate.save()
        else:
            return render(request, 'databases.html', {'form': formDatabaseUpdate})
    return redirect('coreRelback:database')

def databaseDelete(request, idDatabase):
    try:
        databaseIdSelect = Databases.objects.get(pk=idDatabase)
    except Databases.DoesNotExist:
        return redirect('coreRelback:database')
    databaseIdSelect.delete()
    return redirect('coreRelback:database')

# CRUD - Databases - End

# CRUD - Policiess - Initial

def policiesCreate(request):
    if request.method == 'POST':
        formCreatePolicies = formPolicies(request.POST)
        if formCreatePolicies.is_valid():
            formCreatePolicies.save()
            return render(request, 'policies.html')
            # return redirect('coreRelback:policies')
    return render(request, 'policies.html', {'form':formCreatePolicies})

def policiesRead(request):
    clients = Clients.objects.all().order_by('name')
    hosts = Hosts.objects.all().order_by('hostname')
    databases = Databases.objects.all().order_by('db_name')
    policies = BackupPolicies.objects.all().order_by('pk')
    return render(request, 'policies.html', {'clients':clients, 'hosts':hosts, 'databases':databases, 'policies':policies})

def policiesUpdate(request, idPolicy):
    policieIdSelected = BackupPolicies.objects.get(pk=idPolicy)
    if request.method == 'POST':
        formPoliciesUpdate = formPolicies(request.POST, instance=policieIdSelected)
        if formPoliciesUpdate.is_valid():
            formPoliciesUpdate.save()
    return redirect('coreRelback:policies')

def policiesDelete(request, idPolicy):
    try:
        policyIdSelected = BackupPolicies.objects.get(pk=idPolicy)
    except BackupPolicies.DoesNotExist:
        return redirect('coreRelback:policies')
    policyIdSelected.delete()
    return redirect('coreRelback:policies')

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
                        db_key as db_key,
                        to_char(pbv.schedule_start, 'dd/mm/yy hh24:mi') as schedule_start,
                        to_char(bjd.start_time, 'dd/mm/yy hh24:mi') as start_r,
                        case 
                        when bjd.status is null and pbv.schedule_start > sysdate then 'SCHEDULED' 
                        when bjd.status is null and bjd.start_time is null then 'NOT RUN'
                        when bjd.status is not null then bjd.status
                        end as status,
                        bjd.time_taken_display as duration_r,
                        TO_CHAR(TRUNC(pbv.duration/3600),'FM9900') || ':' ||
                        TO_CHAR(TRUNC(MOD(pbv.duration,3600)/60),'FM00') || ':' ||
                        TO_CHAR(MOD(pbv.duration,60),'FM00') as duration_e,
                        trunc(decode(substr(bjd.output_bytes_display,-1,1),'M',
                        to_number(substr(bjd.output_bytes_display,1,    length(bjd.output_bytes_display)-1)/1024),
                        'G',to_number(substr(bjd.output_bytes_display,1,length(bjd.output_bytes_display)-1)),
                        'T',to_number(substr(bjd.output_bytes_display,1,length(bjd.output_bytes_display)-1*1024))),2) as size_r_gb,
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
                    where
                        trunc(pbv.schedule_start) between trunc(sysdate) - 7 and trunc(sysdate)
                        order by pbv.schedule_start desc""")
    # ipdb.set_trace()
    # return HttpResponse(dictfetchall(resultQueryReportRead))
    return render(request, 'reports.html', {'report':dictfetchall(resultQueryReportRead)})

def reportReadLogDetail(request, idPolicy, dbKey, sessionKey):

    reportLog = VwRmanOutput.objects.filter(db_key=dbKey, session_key=sessionKey)

    execDetail = VwRmanBackupJobDetails.objects.filter(db_key=dbKey, session_key=sessionKey)

    policyDetail = BackupPolicies.objects.get(id_policy=idPolicy)

    return render(request, 'reportsReadLog.html', {'reportLog':reportLog, 'execDetail':execDetail, 'policyDetail':policyDetail})
