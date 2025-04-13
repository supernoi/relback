# Generated by Django 5.2 on 2025-04-13 01:44

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreRelback', '0002_create_sequences_triggers'),
    ]

    operations = [
        migrations.CreateModel(
            name='BackupPolicy',
            fields=[
                ('id_policy', models.BigAutoField(primary_key=True, serialize=False)),
                ('policy_name', models.CharField(max_length=150)),
                ('backup_type', models.CharField(max_length=30)),
                ('destination', models.CharField(max_length=8)),
                ('minute', models.CharField(max_length=100)),
                ('hour', models.CharField(max_length=100)),
                ('day', models.CharField(max_length=100)),
                ('month', models.CharField(max_length=100)),
                ('day_week', models.CharField(max_length=100)),
                ('duration', models.DecimalField(decimal_places=0, max_digits=10)),
                ('size_backup', models.CharField(max_length=10)),
                ('status', models.CharField(max_length=8)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Política de Backup',
                'verbose_name_plural': 'Políticas de Backup',
                'db_table': 'backup_policies',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id_client', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'db_table': 'clients',
            },
        ),
        migrations.CreateModel(
            name='Database',
            fields=[
                ('id_database', models.BigAutoField(primary_key=True, serialize=False)),
                ('db_name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=100)),
                ('last_resync', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('dbid', models.BigIntegerField()),
                ('client', models.ForeignKey(db_column='id_client', on_delete=django.db.models.deletion.CASCADE, related_name='databases', to='coreRelback.client')),
            ],
            options={
                'verbose_name': 'Banco de Dados',
                'verbose_name_plural': 'Bancos de Dados',
                'db_table': 'databases',
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id_host', models.BigAutoField(primary_key=True, serialize=False)),
                ('hostname', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('ip', models.GenericIPAddressField(unpack_ipv4=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(db_column='id_client', on_delete=django.db.models.deletion.CASCADE, related_name='hosts', to='coreRelback.client')),
            ],
            options={
                'verbose_name': 'Host',
                'verbose_name_plural': 'Hosts',
                'db_table': 'hosts',
            },
        ),
        migrations.CreateModel(
            name='RelbackUser',
            fields=[
                ('id_user', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('username', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('status', models.PositiveSmallIntegerField(default=1, help_text='1 = Active, 2 = Inactive', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(2)])),
                ('email', models.EmailField(blank=True, max_length=150, null=True)),
                ('remember_token', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Usuário',
                'verbose_name_plural': 'Usuários',
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id_schedule', models.BigAutoField(primary_key=True, serialize=False)),
                ('schedule_start', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'Agendamento',
                'verbose_name_plural': 'Agendamentos',
                'db_table': 'schedules',
            },
        ),
        migrations.DeleteModel(
            name='BackupPolicies',
        ),
        migrations.DeleteModel(
            name='Clients',
        ),
        migrations.DeleteModel(
            name='Databases',
        ),
        migrations.DeleteModel(
            name='Hosts',
        ),
        migrations.DeleteModel(
            name='Schedules',
        ),
        migrations.DeleteModel(
            name='Users',
        ),
        migrations.DeleteModel(
            name='VwRmanBackupSubjobDetails',
        ),
        migrations.DeleteModel(
            name='VwRmanDatabase',
        ),
        migrations.DeleteModel(
            name='VwRmanOutput',
        ),
        migrations.DeleteModel(
            name='VwRmanStatus',
        ),
        migrations.AlterModelOptions(
            name='cronday',
            options={'verbose_name': 'Cron (Dia)', 'verbose_name_plural': 'Cron (Dias)'},
        ),
        migrations.AlterModelOptions(
            name='crondayweek',
            options={'verbose_name': 'Cron (Dia da Semana)', 'verbose_name_plural': 'Cron (Dias da Semana)'},
        ),
        migrations.AlterModelOptions(
            name='cronhour',
            options={'verbose_name': 'Cron (Hora)', 'verbose_name_plural': 'Cron (Horas)'},
        ),
        migrations.AlterModelOptions(
            name='cronminute',
            options={'verbose_name': 'Cron (Minuto)', 'verbose_name_plural': 'Cron (Minutos)'},
        ),
        migrations.AlterModelOptions(
            name='cronmonth',
            options={'verbose_name': 'Cron (Mês)', 'verbose_name_plural': 'Cron (Meses)'},
        ),
        migrations.AlterModelOptions(
            name='cronyear',
            options={'verbose_name': 'Cron (Ano)', 'verbose_name_plural': 'Cron (Anos)'},
        ),
        migrations.AddField(
            model_name='backuppolicy',
            name='client',
            field=models.ForeignKey(db_column='id_client', on_delete=django.db.models.deletion.CASCADE, related_name='backup_policies', to='coreRelback.client'),
        ),
        migrations.AddField(
            model_name='backuppolicy',
            name='database',
            field=models.ForeignKey(db_column='id_database', on_delete=django.db.models.deletion.CASCADE, related_name='backup_policies', to='coreRelback.database'),
        ),
        migrations.AddField(
            model_name='database',
            name='host',
            field=models.ForeignKey(db_column='id_host', on_delete=django.db.models.deletion.CASCADE, related_name='databases', to='coreRelback.host'),
        ),
        migrations.AddField(
            model_name='backuppolicy',
            name='host',
            field=models.ForeignKey(db_column='id_host', on_delete=django.db.models.deletion.CASCADE, related_name='backup_policies', to='coreRelback.host'),
        ),
        migrations.AddField(
            model_name='host',
            name='created_by',
            field=models.ForeignKey(db_column='created_id_user', on_delete=django.db.models.deletion.PROTECT, related_name='created_hosts', to='coreRelback.relbackuser'),
        ),
        migrations.AddField(
            model_name='host',
            name='updated_by',
            field=models.ForeignKey(blank=True, db_column='updated_id_user', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='updated_hosts', to='coreRelback.relbackuser'),
        ),
        migrations.AddField(
            model_name='database',
            name='created_by',
            field=models.ForeignKey(db_column='created_id_user', on_delete=django.db.models.deletion.PROTECT, related_name='created_databases', to='coreRelback.relbackuser'),
        ),
        migrations.AddField(
            model_name='database',
            name='updated_by',
            field=models.ForeignKey(blank=True, db_column='updated_id_user', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='updated_databases', to='coreRelback.relbackuser'),
        ),
        migrations.AddField(
            model_name='client',
            name='created_by',
            field=models.ForeignKey(db_column='created_id_user', on_delete=django.db.models.deletion.PROTECT, related_name='created_clients', to='coreRelback.relbackuser'),
        ),
        migrations.AddField(
            model_name='client',
            name='updated_by',
            field=models.ForeignKey(blank=True, db_column='updated_id_user', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='updated_clients', to='coreRelback.relbackuser'),
        ),
        migrations.AddField(
            model_name='backuppolicy',
            name='created_by',
            field=models.ForeignKey(db_column='created_id_user', on_delete=django.db.models.deletion.PROTECT, related_name='created_backup_policies', to='coreRelback.relbackuser'),
        ),
        migrations.AddField(
            model_name='backuppolicy',
            name='updated_by',
            field=models.ForeignKey(blank=True, db_column='updated_id_user', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='updated_backup_policies', to='coreRelback.relbackuser'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='backup_policy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='coreRelback.backuppolicy'),
        ),
        migrations.AlterUniqueTogether(
            name='database',
            unique_together={('id_database', 'client', 'host')},
        ),
        migrations.AlterUniqueTogether(
            name='schedule',
            unique_together={('backup_policy', 'schedule_start')},
        ),
    ]
