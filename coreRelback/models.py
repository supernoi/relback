from django.db import models


class Users(models.Model):
    id_user = models.FloatField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=60, blank=True, null=True)
    status = models.BigIntegerField(blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    timestamps = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class Clients(models.Model):
    id_client = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    created_id_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='created_id_user', related_name='client_user_creator', blank=True, default=1)
    created_at = models.DateField(auto_now_add=True)
    updated_id_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='updated_id_user', related_name='client_user_updater', blank=True, null=True)
    updated_at = models.DateField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 'clients'

    def __str__(self):
        return self.name

    def __unicode__(self):
        return unicode(self.id_client)

class Hosts(models.Model):
    id_host = models.AutoField(primary_key=True)
    hostname = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    ip = models.CharField(max_length=39)
    id_client = models.ForeignKey('Clients', models.DO_NOTHING, db_column='id_client', related_name='host_client_id')
    created_id_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='created_id_user', related_name='host_user_creator', default=1)
    created_at = models.DateField(auto_now_add=True)
    updated_id_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='updated_id_user', related_name='host_user_updater', blank=True, null=True)
    updated_at = models.DateField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 'hosts'

    def __str__(self):
        return self.hostname

class Databases(models.Model):
    id_database = models.BigIntegerField(primary_key=True)
    id_client = models.ForeignKey('Clients', models.DO_NOTHING, db_column='id_client', related_name='database_client_id')
    id_host = models.ForeignKey('Hosts', models.DO_NOTHING, db_column='id_host', related_name='database_host_id')
    db_name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    last_resync = models.DateField(blank=True, null=True)
    created_id_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='created_id_user', related_name='database_user_creator', default=1)
    created_at = models.DateField(auto_now_add=True)
    updated_id_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='updated_id_user', related_name='database_user_updater', blank=True, null=True)
    updated_at = models.DateField(blank=True, null=True, auto_now=True)
    dbid = models.FloatField()

    class Meta:
        managed = False
        db_table = 'databases'
        unique_together = (('id_database', 'id_client', 'id_host'),)

    def __str__(self):
        return self.db_name

class BackupPolicies(models.Model):
    id_policy = models.BigIntegerField(primary_key=True)
    policy_name = models.CharField(max_length=150, blank=True, null=True)
    id_client = models.ForeignKey('Clients', models.DO_NOTHING, db_column='id_client', related_name='policy_client_id')
    id_database = models.ForeignKey('Databases', models.DO_NOTHING, db_column='id_database', related_name='policy_database_id')
    id_host = models.ForeignKey('Hosts', models.DO_NOTHING, db_column='id_host', related_name='policy_host_id')
    backup_type = models.CharField(max_length=30)
    destination = models.CharField(max_length=8)
    minute = models.CharField(max_length=100)
    hour = models.CharField(max_length=100)
    day = models.CharField(max_length=100)
    month = models.CharField(max_length=100)
    day_week = models.CharField(max_length=100)
    duration = models.FloatField()
    size_backup = models.CharField(max_length=10)
    status = models.CharField(max_length=8)
    description = models.CharField(max_length=100, blank=True, null=True)
    created_id_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='created_id_user', related_name='policy_user_creator', default=1)
    created_at = models.DateField(auto_now_add=True)
    updated_id_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='updated_id_user', related_name='policy_user_updater', blank=True, null=True)
    updated_at = models.DateField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 'backup_policies'
        #unique_together = (('id_database', 'id_client', 'id_host'),)


class Schedules(models.Model):
    id_policy = models.BigIntegerField(primary_key=True)
    schedule_start = models.DateField()

    class Meta:
        managed = False
        db_table = 'schedules'
        unique_together = (('id_policy', 'schedule_start'),)


class CronDay(models.Model):
    id_policy = models.BigIntegerField(primary_key=True)
    day = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'cron_day'
        unique_together = (('id_policy', 'day'),)


class CronDayWeek(models.Model):
    id_policy = models.BigIntegerField(primary_key=True)
    day_week = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'cron_day_week'
        unique_together = (('id_policy', 'day_week'),)


class CronHour(models.Model):
    id_policy = models.BigIntegerField(primary_key=True)
    hour = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'cron_hour'
        unique_together = (('id_policy', 'hour'),)


class CronMinute(models.Model):
    id_policy = models.BigIntegerField(primary_key=True)
    minute = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'cron_minute'
        unique_together = (('id_policy', 'minute'),)


class CronMonth(models.Model):
    id_policy = models.BigIntegerField(primary_key=True)
    month = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'cron_month'
        unique_together = (('id_policy', 'month'),)


class CronYear(models.Model):
    id_policy = models.BigIntegerField(primary_key=True)
    year = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'cron_year'
        unique_together = (('id_policy', 'year'),)


class VwBackupPolicies(models.Model):
    id_policy = models.BigIntegerField()
    schedule_start = models.DateField()
    hostname = models.CharField(max_length=100)
    db_name = models.CharField(max_length=20)
    dbid = models.FloatField()
    destination = models.CharField(max_length=8)
    backup_type = models.CharField(max_length=30)
    duration = models.FloatField()
    size_backup = models.CharField(max_length=10)
    description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'vw_backup_policies'


class VwRmanBackupJobDetails(models.Model):
    db_name = models.CharField(max_length=8)
    dbid = models.FloatField()
    db_key = models.FloatField()
    start_time = models.DateField(blank=True, null=True)
    end_time = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=23, blank=True, null=True)
    time_taken_display = models.CharField(max_length=4000, blank=True, null=True)
    output_bytes_display = models.CharField(max_length=4000, blank=True, null=True)
    output_device_type = models.CharField(max_length=17, blank=True, null=True)
    session_key = models.FloatField(blank=True, null=True)
    session_recid = models.FloatField(blank=True, null=True)
    session_stamp = models.FloatField(blank=True, null=True)
    input_type = models.CharField(max_length=13, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'vw_rman_backup_job_details'


class VwRmanBackupSubjobDetails(models.Model):
    db_name = models.CharField(max_length=8)
    dbid = models.FloatField()
    operation = models.CharField(max_length=33, blank=True, null=True)
    input_type = models.CharField(max_length=13, blank=True, null=True)
    status = models.CharField(max_length=23, blank=True, null=True)
    session_stamp = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'vw_rman_backup_subjob_details'


class VwRmanDatabase(models.Model):
    db_key = models.FloatField()
    dbinc_key = models.FloatField(blank=True, null=True)
    dbid = models.FloatField()
    name = models.CharField(max_length=8)
    resetlogs_change_field = models.FloatField(db_column='resetlogs_change#')  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    resetlogs_time = models.DateField()

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'vw_rman_database'


class VwRmanOutput(models.Model):
    db_key = models.FloatField()
    session_key = models.FloatField()
    recid = models.FloatField(primary_key=True)
    stamp = models.FloatField()
    output = models.CharField(max_length=130)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'vw_rman_output'

class VwRmanStatus(models.Model):
    db_key = models.FloatField()
    db_name = models.CharField(max_length=8)
    row_level = models.FloatField(blank=True, null=True)
    operation = models.CharField(max_length=33, blank=True, null=True)
    object_type = models.CharField(max_length=80, blank=True, null=True)
    status = models.CharField(max_length=33, blank=True, null=True)
    session_key = models.IntegerField(blank=True, null=True)
    session_recid = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'vw_rman_status'
