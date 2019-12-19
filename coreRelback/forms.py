from django import forms

# Models relBack
from .models import Clients
from .models import Hosts
from .models import Databases
from .models import BackupPolicies

class formClient(forms.ModelForm):
    class Meta:
        model = Clients
        fields = ('name', 'description')
        #fields = "__all__"

class formHost(forms.ModelForm):
    class Meta:
        model = Hosts
        fields = ('id_client', 'hostname', 'ip', 'description')
        #fields = '__all__'

class formDatabase(forms.ModelForm):
    class Meta:
        model = Databases
        fields = ('id_client', 'id_host', 'db_name', 'dbid', 'description')
        #fields = '__all__'

class formPolicies(forms.ModelForm):
    class Meta:
        model = BackupPolicies
        fields = ('status', 'policy_name', 'id_client', 'id_host', 'id_database', 'backup_type', 'destination'
        , 'minute', 'hour', 'day', 'month', 'day_week', 'duration', 'size_backup', 'description')
        #fields = '__all__'
