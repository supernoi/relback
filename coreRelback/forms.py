from django import forms

# Models relBack
from .models import Client, Host, Database, BackupPolicy

class formClient(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'description')
        #fields = "__all__"

class formHost(forms.ModelForm):

    # client = forms.ModelChoiceField(label='Client', queryset=Client.objects.all().order_by('name'), empty_label='Choose your option')
    class Meta:
        model = Host
        fields = ('client', 'hostname', 'ip', 'description')
        labels = {
            "hostname": "Hostname",
            "description": "Description",
            "ip": "IP Address",
        }

class formDatabase(forms.ModelForm):
    class Meta:
        model = Database
        fields = ('client', 'host', 'db_name', 'dbid', 'description')
        #fields = '__all__'

class formPolicies(forms.ModelForm):
    class Meta:
        model = BackupPolicy
        fields = ('status', 'policy_name', 'client', 'host', 'database', 'backup_type', 'destination', 'minute', 'hour', 'day', 'month', 'day_week', 'duration', 'size_backup', 'description')
        #fields = '__all__'
