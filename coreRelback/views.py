# Imported from Django
from django.shortcuts import render, redirect
from django.db  import connection
from django.core import serializers
from django.forms.models import model_to_dict


from django.http import JsonResponse
from django.views.generic import TemplateView, View, DeleteView

# Imported from project relBack

# Forms from relBack
from .forms import formClient, formHost, formDatabase, formPolicies

# Models from relBack
from .models import Clients, Hosts, Databases, BackupPolicies, VwRmanOutput, VwRmanBackupJobDetails

# Debug ipdb
from django.http import HttpResponse
import ipdb


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
        clientName = request.GET.get('name', None)
        description = request.GET.get('description', None)

        obj = Clients.objects.create(
            name=clientName,
            description=description,
        )

        client = {'id_client':obj.id_client, 'name':obj.name, 'description':obj.description}

        data = {
            'client': client,
            'description': description
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

class databaseRead(TemplateView):
    template_name = 'databases.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['hosts'] = Hosts.objects.all().order_by('hostname')
        context['clients'] = Clients.objects.all().order_by('name')
        context['databases'] = Databases.objects.all().order_by('id_database')

        return context

class databaseCreate(View):
    def get(self, request):
        idClient = request.GET.get('id_client', None)
        idHost = request.GET.get('id_host', None)
        dbName = request.GET.get('db_name', None)
        dbId = request.GET.get('db_id', None)
        description = request.GET.get('description', None)

        obj = Databases.objects.create(
            id_client_id=idClient,
            id_host_id=idHost,
            db_name=dbName,
            dbid=dbId,
            description=description,
        )

        database = {'id_database':obj.id_database
                    , 'id_client':obj.id_client_id
                    , 'client_name':obj.id_client.name
                    , 'id_host':obj.id_host_id
                    , 'hostname':obj.id_host.hostname                   
                    , 'dbname':obj.db_name
                    , 'dbid':obj.dbid
                    , 'description':obj.description}

        data = {
            'database': database
        }
        # ipdb.set_trace()

        return JsonResponse(data)

class databaseUpdate(View):
    def  get(self, request):
        idDatabase = request.GET.get('id_database', None)
        idClient = request.GET.get('id_client', None)
        idHost = request.GET.get('id_host', None)
        dbName = request.GET.get('db_name', None)
        dbId = request.GET.get('db_id', None)
        description = request.GET.get('description', None)

        obj = Databases.objects.get(pk=idDatabase)
        obj.id_database = idDatabase
        obj.id_client_id = idClient
        obj.id_host_id = idHost
        obj.db_name = dbName
        obj.dbid = dbId
        obj.description = description

        # ipdb.set_trace()

        obj.save()

        database = {'id_database':obj.id_database
                    , 'id_client':obj.id_client_id
                    , 'client_name':obj.id_client.name
                    , 'id_host':obj.id_host_id
                    , 'hostname':obj.id_host.hostname
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
                                        , list(Hosts.objects.filter(id_client_id=id_client).order_by('hostname'))
                                        , fields=('id_host','hostname'))
    return JsonResponse({'hosts': clientHosts})

def databasesList(request):
    id_client = request.GET.get('id_client', None)
    id_host = request.GET.get('id_host', None)
    databases = serializers.serialize('json'
                                        , list(Databases.objects.filter(id_client_id=id_client, id_host_id=id_host).order_by('db_name'))
                                        , fields=('id_database','db_name'))

    # ipdb.set_trace()
    return JsonResponse({'databases': databases})


class databaseDelete(View):
    def get(self, request):
        id_database = request.GET.get('id_database', None)
        Databases.objects.get(pk=id_database).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)

# CRUD - Databases - End

# CRUD - Policies - Initial

class policyRead(TemplateView):
    template_name = 'policies.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['hosts'] = Hosts.objects.all().order_by('hostname')
        context['clients'] = Clients.objects.all().order_by('name')
        context['databases'] = Databases.objects.all().order_by('db_name')
        context['policies'] = BackupPolicies.objects.all().order_by('policy_name')

        return context

    def policyDetail(request):

        idPolicy = request.GET.get('id_policy', None)

        obj = BackupPolicies.objects.get(pk=idPolicy)

        policy = {
                'id_policy':obj.id_policy
                , 'policy_name':obj.policy_name
                , 'id_client':obj.id_client_id
                , 'client_name':obj.id_client.name
                , 'id_host':obj.id_host_id
                , 'hostname':obj.id_host.hostname  
                , 'id_database':obj.id_database_id                
                , 'db_name':obj.id_database.db_name
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

        obj = BackupPolicies.objects.create(
            policy_name=policyName,
            id_client_id=idClient,
            id_host_id=idHost,
            id_database_id=idDatabase,
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
        )

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

        # ipdb.set_trace()

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

        obj = BackupPolicies.objects.get(pk=idPolicy)
        obj.id_policy = idPolicy
        obj.id_database_id = idDatabase
        obj.id_client_id = idClient
        obj.id_host_id = idHost
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
        BackupPolicies.objects.get(pk=id_policy).delete()
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

    reportLog = VwRmanOutput.objects.filter(db_key=dbKey, session_key=sessionKey)

    execDetail = VwRmanBackupJobDetails.objects.filter(db_key=dbKey, session_key=sessionKey)

    policyDetail = BackupPolicies.objects.get(id_policy=idPolicy)

    return render(request, 'reportsReadLog.html', {'reportLog':reportLog, 'execDetail':execDetail, 'policyDetail':policyDetail})

def reportRefreshSchedule(request):

    with connection.cursor() as cursor:
        cursor.callproc('SP_CREATE_SCHEDULE')

    return reportRead(request)