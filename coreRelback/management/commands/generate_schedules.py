from django.core.management.base import BaseCommand
from coreRelback.services.schedule_generator import generate_schedules

class Command(BaseCommand):
    help = 'Gera previsões de execução de backup (agenda) para todas políticas ativas.'

    def handle(self, *args, **options):
        generate_schedules()
        self.stdout.write(self.style.SUCCESS('Agendamento de backups gerado com sucesso.'))
