# Imported from Django
from django.shortcuts import render, redirect
from django.db  import connection

# Imported from project relBack

# Forms from relBack
from .forms import formClient, formHost, formDatabase, formPolicies

# Models from relBack
from .models import Clients, Hosts, Databases, BackupPolicies

# Debug ipdb
# import ipdb
# ipdb.set_trace()

def index(request):
    return render(request, 'index.html')

def creators(request):
    return render(request, 'creators.html')

# CRUD - Client - Initial

def clientCreate(request):
    if request.method == 'POST':
        formCreateClient = formClient(request.POST)
        if formCreateClient.is_valid():
            formCreateClient.save()
        return redirect('coreRelback:client')
    formCreateClient = formClient()
    return render(request, 'clients.html', {'hostForm': formCreateClient})

def clientRead(request):
    clients = Clients.objects.all().order_by('pk')
    return render(request, 'clients.html', {'clients':clients})

def clientReadDetails(request, idClient):
    clientIdDetails = Clients.objects.get(pk=idClient)
    return render(request, 'clients.html', {'clientiddetails':clientIdDetails})

def clientUpdate(request, idClient):
    clientIdSelected = Clients.objects.get(pk=idClient)
    if request.method == 'POST':
        formClientUpdate = formClient(request.POST, instance=clientIdSelected)
        if formClientUpdate.is_valid():
            formClientUpdate.save()
            return redirect('coreRelback:client')
    else:
        formClientUpdate = formClient(instance=clientIdSelected)
    return render(request, 'clients.html', {'form': formClientUpdate})

def clientDelete(request, idClient):
    try:
        clientIdSelected = Clients.objects.get(pk=idClient)
    except Clients.DoesNotExist:
        return redirect('coreRelback:client')
    clientIdSelected.delete()
    return redirect('coreRelback:client')

# CRUD - Clients - End

# CRUD - Hosts - Initial

def hostCreate(request):
    if request.method == 'POST':
        formCreateHost = formHost(request.POST)
        if formCreateHost.is_valid():
            formCreateHost.save()
        return redirect('coreRelback:host')
    formCreateHost = formHost()
    return render(request, 'hosts.html', {'hostForm':formCreateHost})

def hostRead(request):
    clients = Clients.objects.all().order_by('pk')
    hosts = Hosts.objects.all().order_by('pk')
    return render(request, 'hosts.html', {'clients':clients, 'hosts':hosts})

def hostUpdate(request, idHost):
    hostIdSelected = Hosts.objects.get(pk=idHost)
    if request.method == 'POST':
        formHostUpdate = formHost(request.POST, instance=hostIdSelected)
        if formHostUpdate.is_valid():
            formHostUpdate.save()
    return render(request, 'hosts.html')

def hostDelete(request, idHost):
    try:
        hostIdSelected = Hosts.objects.get(pk=idHost)
    except Hosts.DoesNotExist:
        return redirect('coreRelback:host')
    hostIdSelected.delete()
    return redirect('coreRelback:host')

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
    return redirect('coreRelback:database', {'form':formDatabaseUpdate})

def databaseDelete(request, idDatabase):
    try:
        databaseIdSelect = Databases.objects.get(pk=idDatabase)
    except Databases.DoesNotExist:
        return redirect('coreRelback:database')
    databaseIdSelect.delete()
    return redirect('coreRelback:database')

# CRUD - Databases - End# CRUD - Policiess - Initial

def policiesCreate(request):
    if request.method == 'POST':
        formCreatePolicies = formPolicies(request.POST)
        if formCreatePolicies.is_valid():
            formCreatePolicies.save()
    return redirect('coreRelback:policies')

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

# CRUD - Policiess - End

def reportRead(request):
    cursor = connection.cursor()
    resultQueryReportRead = cursor.execute("""select
                        to_number(pbv.id_policy)                                                                            id_policy,
                        upper(substr(pbv.hostname,1,30))                                                                    hostname,
                        upper(pbv.db_name)                                                                                  db_name,
                        db_key																							  db_key,
                        to_char(pbv.schedule_start, 'dd/mm/yy hh24:mi')                                                  		schedule_start,
                        to_char(bjd.start_time, 'dd/mm/yy hh24:mi')                                                      		start_r,
                        case 
                        when bjd.status is null and pbv.schedule_start > sysdate then 'SCHEDULED' 
                        when bjd.status is null and bjd.start_time is null then 'NOT RUN'
                        when bjd.status is not null then bjd.status
                        end	                                                       										  status,
                        bjd.time_taken_display                                                                              duration_r,
                        TO_CHAR(TRUNC(pbv.duration/3600),'FM9900') || ':' ||
                        TO_CHAR(TRUNC(MOD(pbv.duration,3600)/60),'FM00') || ':' ||
                        TO_CHAR(MOD(pbv.duration,60),'FM00')                                                               duration_e,
                        trunc(decode(substr(bjd.output_bytes_display,-1,1),'M',
                        to_number(substr(bjd.output_bytes_display,1,    length(bjd.output_bytes_display)-1)/1024),
                        'G',to_number(substr(bjd.output_bytes_display,1,length(bjd.output_bytes_display)-1)),
                        'T',to_number(substr(bjd.output_bytes_display,1,length(bjd.output_bytes_display)-1*1024))),2)   size_r_gb,
                        trunc(decode(substr(pbv.size_backup,-1,1),'M',
                        to_number(substr(pbv.size_backup,1,    length(pbv.size_backup)-1)/1024),
                        'G',to_number(substr(pbv.size_backup,1,length(pbv.size_backup)-1)),
                        'T',to_number(substr(pbv.size_backup,1,length(pbv.size_backup)-1*1024))),2)                     size_p_gb,
                        pbv.destination                                                                                 destination,
                        pbv.backup_type                                                                                  backup_type,
                        bjd.session_key																				  session_key,
                        pbv.description                                                                                     description
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
    return render(request, 'reports.html', {'report':resultQueryReportRead})
