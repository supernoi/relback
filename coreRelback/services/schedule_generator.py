import datetime
from django.db import transaction
from coreRelback.models import BackupPolicy, Schedule, Database, Host

# Utilitário para expandir expressões crontab (ex: '1,2,5-7,*')
def expand_cron_field(field, min_value, max_value):
    result = set()
    if field == '*':
        return set(range(min_value, max_value + 1))
    for part in field.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            result.update(range(start, end + 1))
        else:
            try:
                result.add(int(part))
            except ValueError:
                pass
    return result

# Gera previsões de execução para todas políticas ativas
@transaction.atomic
def generate_schedules(reference_date=None):
    if reference_date is None:
        reference_date = datetime.date.today()
    # Limpa agenda anterior
    Schedule.objects.all().delete()
    policies = BackupPolicy.objects.filter(status__iexact='ACTIVE').select_related('database', 'host')
    for policy in policies:
        # Expande campos crontab
        minutes = expand_cron_field(policy.minute, 0, 59)
        hours = expand_cron_field(policy.hour, 0, 23)
        days = expand_cron_field(policy.day, 1, 31)
        months = expand_cron_field(policy.month, 1, 12)
        weekdays = expand_cron_field(policy.day_week, 0, 6)
        # Para cada combinação válida, gera previsão
        for month in months:
            for day in days:
                try:
                    date = datetime.date(reference_date.year, month, day)
                except ValueError:
                    continue  # Dia inválido para o mês
                if date < reference_date:
                    continue
                if date.weekday() not in weekdays and policy.day_week != '*':
                    continue
                for hour in hours:
                    for minute in minutes:
                        schedule_dt = datetime.datetime(date.year, date.month, date.day, hour, minute)
                        Schedule.objects.create(
                            backup_policy=policy,
                            schedule_start=schedule_dt
                        )
