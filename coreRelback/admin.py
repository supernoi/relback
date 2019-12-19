from django.contrib import admin

# Register your models here.
from .models import Users
from .models import Clients
from .models import Hosts
from .models import Databases
from .models import BackupPolicies
from .models import Schedules
from .models import CronHour
from .models import CronMinute
from .models import CronDay
from .models import CronDayWeek
from .models import CronMonth

@admin.register(Users)
class usersAdmin(admin.ModelAdmin):
    pass

@admin.register(Clients)
class clientsAdmin(admin.ModelAdmin):
    pass

@admin.register(Hosts)
class hostsAdmin(admin.ModelAdmin):
    pass

@admin.register(Databases)
class databasesAdmin(admin.ModelAdmin):
    pass

@admin.register(BackupPolicies)
class backuppoliciesAdmin(admin.ModelAdmin):
    pass

@admin.register(Schedules)
class schedulesAdmin(admin.ModelAdmin):
    pass

@admin.register(CronHour)
class cronminuteAdmin(admin.ModelAdmin):
    pass

@admin.register(CronMinute)
class cronhourAdmin(admin.ModelAdmin):
    pass

@admin.register(CronDay)
class crondayAdmin(admin.ModelAdmin):
    pass

@admin.register(CronDayWeek)
class crondayweekAdmin(admin.ModelAdmin):
    pass

@admin.register(CronMonth)
class cronmonthAdmin(admin.ModelAdmin):
    pass
