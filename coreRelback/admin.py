from django.contrib import admin
from .models import (
    Users,
    Clients,
    Hosts,
    Databases,
    BackupPolicies,
    Schedules,
    CronHour,
    CronMinute,
    CronDay,
    CronDayWeek,
    CronMonth,
)

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')
    search_fields = ('username', 'email')

@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    list_display = ('id_client', 'name', 'description')
    search_fields = ('name',)

@admin.register(Hosts)
class HostsAdmin(admin.ModelAdmin):
    list_display = ('id_host', 'hostname', 'ip')
    search_fields = ('hostname', 'ip')

@admin.register(Databases)
class DatabasesAdmin(admin.ModelAdmin):
    list_display = ('id_database', 'db_name', 'client', 'host')
    search_fields = ('db_name',)

@admin.register(BackupPolicies)
class BackupPoliciesAdmin(admin.ModelAdmin):
    list_display = ('id_policy', 'policy_name', 'backup_type', 'destination', 'status')
    search_fields = ('policy_name',)
    list_filter = ('backup_type', 'status')

@admin.register(Schedules)
class SchedulesAdmin(admin.ModelAdmin):
    list_display = ('id', 'backup_policy', 'schedule_start')
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
