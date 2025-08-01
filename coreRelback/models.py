from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.hashers import make_password, check_password

# Modelo para usuários - modelo simples sem herança AbstractBaseUser
class RelbackUser(models.Model):
    id_user = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    status = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(2)],
        help_text="1 = Active, 2 = Inactive"
    )
    email = models.EmailField(max_length=150, blank=True, null=True)
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        constraints = [
            models.CheckConstraint(check=models.Q(status__in=[1, 2]), name="ck_users_status")
        ]

    def __str__(self):
        return self.username or f"User {self.id_user}"
    
    def set_password(self, raw_password):
        """Define a senha usando hash do Django"""
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Verifica a senha"""
        return check_password(raw_password, self.password)
    
    # Propriedades necessárias para compatibilidade com sistema de autenticação
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    @property
    def is_active(self):
        return self.status == 1
    
    @property
    def pk(self):
        return self.id_user


# Modelo para Clientes
class Client(models.Model):
    id_client = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    created_by = models.ForeignKey(
        RelbackUser,
        on_delete=models.PROTECT,
        related_name='created_clients',
        db_column='created_id_user'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        RelbackUser,
        on_delete=models.PROTECT,
        related_name='updated_clients',
        db_column='updated_id_user',
        blank=True,
        null=True
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'clients'
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.name or f"Client {self.id_client}"


# Modelo para Hosts
class Host(models.Model):
    id_host = models.BigAutoField(primary_key=True)
    hostname = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    ip = models.CharField(max_length=15)  # compatível com Oracle VARCHAR2(15)
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='hosts',
        db_column='id_client'
    )
    created_by = models.ForeignKey(
        RelbackUser,
        on_delete=models.PROTECT,
        related_name='created_hosts',
        db_column='created_id_user'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        RelbackUser,
        on_delete=models.PROTECT,
        related_name='updated_hosts',
        db_column='updated_id_user',
        blank=True,
        null=True
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hosts'
        verbose_name = "Host"
        verbose_name_plural = "Hosts"

    def __str__(self):
        return self.hostname


# Modelo para Bancos de Dados
class Database(models.Model):
    id_database = models.BigAutoField(primary_key=True)
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='databases',
        db_column='id_client'
    )
    host = models.ForeignKey(
        Host,
        on_delete=models.CASCADE,
        related_name='databases',
        db_column='id_host'
    )
    db_name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    last_resync = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(
        RelbackUser,
        on_delete=models.PROTECT,
        related_name='created_databases',
        db_column='created_id_user'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        RelbackUser,
        on_delete=models.PROTECT,
        related_name='updated_databases',
        db_column='updated_id_user',
        blank=True,
        null=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    dbid = models.BigIntegerField()

    class Meta:
        db_table = 'databases'
        unique_together = (('id_database', 'client', 'host'),)
        verbose_name = "Banco de Dados"
        verbose_name_plural = "Bancos de Dados"

    def __str__(self):
        return self.db_name


# Modelo para Políticas de Backup
class BackupPolicy(models.Model):
    id_policy = models.BigAutoField(primary_key=True)
    policy_name = models.CharField(max_length=150)
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='backup_policies',
        db_column='id_client'
    )
    database = models.ForeignKey(
        Database,
        on_delete=models.CASCADE,
        related_name='backup_policies',
        db_column='id_database'
    )
    host = models.ForeignKey(
        Host,
        on_delete=models.CASCADE,
        related_name='backup_policies',
        db_column='id_host'
    )
    backup_type = models.CharField(max_length=30)
    destination = models.CharField(max_length=8)
    minute = models.CharField(max_length=100)
    hour = models.CharField(max_length=100)
    day = models.CharField(max_length=100)
    month = models.CharField(max_length=100)
    day_week = models.CharField(max_length=100)
    duration = models.DecimalField(max_digits=10, decimal_places=0)
    size_backup = models.CharField(max_length=10)
    status = models.CharField(max_length=8)
    description = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.ForeignKey(
        RelbackUser,
        on_delete=models.PROTECT,
        related_name='created_backup_policies',
        db_column='created_id_user'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        RelbackUser,
        on_delete=models.PROTECT,
        related_name='updated_backup_policies',
        db_column='updated_id_user',
        blank=True,
        null=True
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'backup_policies'
        verbose_name = "Política de Backup"
        db_table = 'backup_policies'
        verbose_name = "Política de Backup"
        verbose_name_plural = "Políticas de Backup"
<<<<<<< HEAD
        constraints = [
            models.CheckConstraint(
                check=models.Q(backup_type__in=[
                    'ARCHIVELOG', 'DB FULL', 'DB INCR', 'RECVR AREA', 'BACKUPSET'
                ]),
                name="politica_de_backup_ck2"
            ),
            models.CheckConstraint(
                check=models.Q(destination__in=['DISK', 'SBT_TAPE', '*']),
                name="politica_de_backup_ck3"
            ),
            models.CheckConstraint(
                check=models.Q(status__in=['ACTIVE', 'INACTIVE']),
                name="politica_de_backup_ck1"
            )
        ]
=======
>>>>>>> 811bf09f982df832f56f799820e3f43d02b7aae7

    def __str__(self):
        return self.policy_name


# Modelo para Agendamentos (Schedules)
class Schedule(models.Model):
    id_schedule = models.BigAutoField(primary_key=True)
    backup_policy = models.ForeignKey(
        BackupPolicy,
        on_delete=models.CASCADE,
        related_name='schedules'
    )
    schedule_start = models.DateTimeField()

    class Meta:
        db_table = 'schedules'
        unique_together = (('backup_policy', 'schedule_start'),)
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"

    def __str__(self):
        return f"Policy {self.backup_policy.id_policy} at {self.schedule_start}"


# Seções específicas para campos de cron (opcional – se forem realmente usados)
class CronDay(models.Model):
    backup_policy = models.ForeignKey(
        BackupPolicy,
        on_delete=models.CASCADE,
        related_name='cron_days',
        null=True,
        blank=True
    )
    day = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'cron_day'
        unique_together = (('backup_policy', 'day'),)
        verbose_name = "Cron (Dia)"
        verbose_name_plural = "Cron (Dias)"


class CronDayWeek(models.Model):
    backup_policy = models.ForeignKey(
        BackupPolicy,
        on_delete=models.CASCADE,
        related_name='cron_day_weeks',
        null=True,
        blank=True
    )
    day_week = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'cron_day_week'
        unique_together = (('backup_policy', 'day_week'),)
        verbose_name = "Cron (Dia da Semana)"
        verbose_name_plural = "Cron (Dias da Semana)"


class CronHour(models.Model):
    backup_policy = models.ForeignKey(
        BackupPolicy,
        on_delete=models.CASCADE,
        related_name='cron_hours',
        null=True,
        blank=True
    )
    hour = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'cron_hour'
        unique_together = (('backup_policy', 'hour'),)
        verbose_name = "Cron (Hora)"
        verbose_name_plural = "Cron (Horas)"


class CronMinute(models.Model):
    backup_policy = models.ForeignKey(
        BackupPolicy,
        on_delete=models.CASCADE,
        related_name='cron_minutes',
        null=True,
        blank=True
    )
    minute = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'cron_minute'
        unique_together = (('backup_policy', 'minute'),)
        verbose_name = "Cron (Minuto)"
        verbose_name_plural = "Cron (Minutos)"


class CronMonth(models.Model):
    backup_policy = models.ForeignKey(
        BackupPolicy,
        on_delete=models.CASCADE,
        related_name='cron_months',
        null=True,
        blank=True
    )
    month = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'cron_month'
        unique_together = (('backup_policy', 'month'),)
        verbose_name = "Cron (Mês)"
        verbose_name_plural = "Cron (Meses)"


class CronYear(models.Model):
    backup_policy = models.ForeignKey(
        BackupPolicy,
        on_delete=models.CASCADE,
        related_name='cron_years',
        null=True,
        blank=True
    )
    year = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'cron_year'
        unique_together = (('backup_policy', 'year'),)
        verbose_name = "Cron (Ano)"
        verbose_name_plural = "Cron (Anos)"


# Modelos para Views – serão mantidos como não gerenciados pelo Django
class VwBackupPolicies(models.Model):
    id_policy = models.BigIntegerField(primary_key=True)
    schedule_start = models.DateTimeField()
    hostname = models.CharField(max_length=100)
    db_name = models.CharField(max_length=20)
    dbid = models.BigIntegerField()
    destination = models.CharField(max_length=8)
    backup_type = models.CharField(max_length=30)
    duration = models.DecimalField(max_digits=10, decimal_places=0)
    size_backup = models.CharField(max_length=10)
    description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'vw_backup_policies'
        managed = False

# (Outros modelos de views, procedures, etc., podem ser mantidos com managed = False)
# Exemplo:
# class VwRmanBackupJobDetails(models.Model):
#     db_name = models.CharField(max_length=8)
#     dbid = models.BigIntegerField()
#     db_key = models.BigIntegerField()
#     start_time = models.DateTimeField(blank=True, null=True)
#     end_time = models.DateTimeField(blank=True, null=True)
#     status = models.CharField(max_length=23, blank=True, null=True)
#     time_taken_display = models.CharField(max_length=4000, blank=True, null=True)
#     output_bytes_display = models.CharField(max_length=4000, blank=True, null=True)
#     output_device_type = models.CharField(max_length=17, blank=True, null=True)
#     session_key = models.BigIntegerField(blank=True, null=True)
#     session_recid = models.BigIntegerField(blank=True, null=True)
#     session_stamp = models.BigIntegerField(blank=True, null=True)
#     input_type = models.CharField(max_length=13, blank=True, null=True)
#
#     class Meta:
#         db_table = 'vw_rman_backup_job_details'
#         managed = False
