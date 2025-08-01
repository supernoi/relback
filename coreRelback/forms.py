from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

# Models relBack
from .models import Client, Host, Database, BackupPolicy, RelbackUser

class RelbackLoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'id': 'username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'password'
        })
    )
    
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            try:
                relback_user = RelbackUser.objects.get(username=username)
                if not relback_user.check_password(password):
                    raise forms.ValidationError("Invalid username or password.")
                if relback_user.status != 1:
                    raise forms.ValidationError("User account is inactive.")
                
                # Use our custom authentication backend
                user = authenticate(self.request, username=username, password=password)
                if user is None:
                    raise forms.ValidationError("Authentication failed.")
                
                self.user_cache = user
            except RelbackUser.DoesNotExist:
                raise forms.ValidationError("Invalid username or password.")
        
        return self.cleaned_data

class RelbackUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
    )
    
    class Meta:
        model = RelbackUser
        fields = ('username', 'name', 'email')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
        }
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.status = 1  # Ativo por padrão
        if commit:
            user.save()
        return user

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
