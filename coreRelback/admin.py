from django.contrib import admin
from .models import (
    RelbackUser,
    Client,
    Host,
    Database,
    BackupPolicy,
    Schedule,
    CronHour,
    CronMinute,
    CronDay,
    CronDayWeek,
    CronMonth,
)

@admin.register(RelbackUser)
class RelbackUserAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'username', 'email')
    search_fields = ('username', 'email')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id_client', 'name', 'description')
    search_fields = ('name',)

@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    list_display = ('id_host', 'hostname', 'ip')
    search_fields = ('hostname', 'ip')

@admin.register(Database)
class DatabaseAdmin(admin.ModelAdmin):
    list_display = ('id_database', 'db_name', 'client', 'host')
    search_fields = ('db_name',)

@admin.register(BackupPolicy)
class BackupPolicyAdmin(admin.ModelAdmin):
    list_display = ('id_policy', 'policy_name', 'backup_type', 'destination', 'status')
    search_fields = ('policy_name',)
    list_filter = ('backup_type', 'status')

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id_schedule', 'backup_policy', 'schedule_start')
    search_fields = ('backup_policy__policy_name',)
    list_filter = ('schedule_start',)

@admin.register(CronHour)
class CronHourAdmin(admin.ModelAdmin):
    list_display = ('id', 'backup_policy', 'hour')
    list_filter = ('hour',)

@admin.register(CronMinute)
class CronMinuteAdmin(admin.ModelAdmin):
    list_display = ('id', 'backup_policy', 'minute')
    list_filter = ('minute',)

@admin.register(CronDay)
class CronDayAdmin(admin.ModelAdmin):
    list_display = ('id', 'backup_policy', 'day')
    list_filter = ('day',)

@admin.register(CronDayWeek)
class CronDayWeekAdmin(admin.ModelAdmin):
    list_display = ('id', 'backup_policy', 'day_week')
    list_filter = ('day_week',)

@admin.register(CronMonth)
class CronMonthAdmin(admin.ModelAdmin):
    list_display = ('id', 'backup_policy', 'month')
    list_filter = ('month',)
