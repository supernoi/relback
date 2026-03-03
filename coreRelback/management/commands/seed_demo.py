"""
Management command: seed_demo

Populates the SQLite database with realistic fictitious data so the UI
can be previewed locally without an Oracle connection.

Usage:
    DJANGO_SETTINGS_MODULE=projectRelback.settings_local python manage.py migrate
    DJANGO_SETTINGS_MODULE=projectRelback.settings_local python manage.py seed_demo
    DJANGO_SETTINGS_MODULE=projectRelback.settings_local python manage.py runserver

    Login: admin / demo1234

Running again with --flush first wipes all data and reseeds from scratch:
    python manage.py seed_demo --flush
"""
from django.core.management.base import BaseCommand
from django.db import transaction


DEMO_CLIENTS = [
    {"name": "Acme Corp",        "description": "Retail e-commerce platform"},
    {"name": "TechNova",         "description": "SaaS product company"},
    {"name": "GlobalBank",       "description": "Core banking systems"},
    {"name": "MediCare Systems", "description": "Hospital management & HL7"},
]

DEMO_HOSTS = [
    # (client_idx, hostname, ip, description)
    (0, "acme-db01",   "10.0.0.11", "Primary Oracle node"),
    (0, "acme-db02",   "10.0.0.12", "DR standby node"),
    (1, "nova-db01",   "10.1.0.11", "Production Oracle 19c"),
    (1, "nova-db02",   "10.1.0.12", "Reporting replica"),
    (2, "bank-db01",   "10.2.0.11", "Core banking DB primary"),
    (2, "bank-db02",   "10.2.0.12", "Core banking DB standby"),
    (2, "bank-dw01",   "10.2.0.13", "Data warehouse"),
    (3, "medi-db01",   "10.3.0.11", "Patient records DB"),
]

DEMO_DATABASES = [
    # (host_idx, client_idx, db_name, description, dbid)
    (0, 0, "ACMEPROD",  "Production OLTP DB",           3951648617),
    (1, 0, "ACMEDR",    "DR standby OLTP DB",           3951648618),
    (2, 1, "NOVAPROD",  "Production SaaS database",     1234567890),
    (3, 1, "NOVAREP",   "Reporting read-only DB",       1234567891),
    (4, 2, "BANKCORE",  "Core banking OLTP",            9876543210),
    (5, 2, "BANKDR",    "Core banking DR",              9876543211),
    (6, 2, "BANKDW",    "Data warehouse",               1122334455),
    (7, 3, "MEDIEHR",   "Electronic health records",    5544332211),
]

DEMO_POLICIES = [
    # (db_idx, host_idx, client_idx, policy_name, backup_type, dest, minute, hour, day, month, day_week, duration, size)
    (0, 0, 0, "ACMEPROD Full Daily",    "DB FULL",     "DISK",     "0", "2",  "*", "*", "0,6",  120, "50G"),
    (0, 0, 0, "ACMEPROD Arch Hourly",   "ARCHIVELOG",  "DISK",     "30","*",  "*", "*", "*",     15, "2G"),
    (2, 2, 1, "NOVA Full Weekly",       "DB FULL",     "SBT_TAPE", "0", "1",  "*", "*", "0",    180, "80G"),
    (2, 2, 1, "NOVA Incr Daily",        "DB INCR",     "DISK",     "0", "3",  "*", "*", "1-6",   60, "10G"),
    (4, 4, 2, "BANK Full Daily",        "DB FULL",     "SBT_TAPE", "0", "0",  "*", "*", "*",    240, "200G"),
    (4, 4, 2, "BANK Arch 30min",        "ARCHIVELOG",  "DISK",     "*/30","*","*", "*", "*",     10, "5G"),
    (6, 6, 2, "DW Full Weekly",         "DB FULL",     "SBT_TAPE", "0", "4",  "*", "*", "0",    360, "500G"),
    (7, 7, 3, "MEDI Full Daily",        "DB FULL",     "DISK",     "0", "1",  "*", "*", "*",    120, "30G"),
]


class Command(BaseCommand):
    help = "Seed the database with fictitious demo data for local UI preview."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete all existing data before seeding.",
        )

    def handle(self, *args, **options):
        from coreRelback.models import (
            RelbackUser, Client, Host, Database, BackupPolicy
        )

        if options["flush"]:
            self.stdout.write(self.style.WARNING("Flushing all existing data…"))
            BackupPolicy.objects.all().delete()
            Database.objects.all().delete()
            Host.objects.all().delete()
            Client.objects.all().delete()
            RelbackUser.objects.filter(username__startswith="demo").delete()

        with transaction.atomic():
            # 1. Admin user
            admin, created = RelbackUser.objects.get_or_create(
                username="admin",
                defaults={
                    "name": "Demo Admin",
                    "email": "admin@relback.local",
                    "status": 1,
                },
            )
            if created or not admin.check_password("demo1234"):
                admin.set_password("demo1234")
                admin.save()
                self.stdout.write(self.style.SUCCESS("  ✓ Created admin user (admin / demo1234)"))
            else:
                self.stdout.write("  · admin user already exists")

            # 2. Clients
            clients = []
            for c in DEMO_CLIENTS:
                obj, created = Client.objects.get_or_create(
                    name=c["name"],
                    defaults={"description": c["description"], "created_by": admin},
                )
                clients.append(obj)
                status = "✓ Created" if created else "· Exists"
                self.stdout.write(f"  {status}: Client {obj.name}")

            # 3. Hosts
            hosts = []
            for client_idx, hostname, ip, description in DEMO_HOSTS:
                obj, created = Host.objects.get_or_create(
                    hostname=hostname,
                    defaults={
                        "ip": ip,
                        "description": description,
                        "client": clients[client_idx],
                        "created_by": admin,
                    },
                )
                hosts.append(obj)
                status = "✓ Created" if created else "· Exists"
                self.stdout.write(f"  {status}: Host {obj.hostname}")

            # 4. Databases
            databases = []
            for host_idx, client_idx, db_name, description, dbid in DEMO_DATABASES:
                obj, created = Database.objects.get_or_create(
                    db_name=db_name,
                    defaults={
                        "description": description,
                        "dbid": dbid,
                        "host": hosts[host_idx],
                        "client": clients[client_idx],
                        "created_by": admin,
                    },
                )
                databases.append(obj)
                status = "✓ Created" if created else "· Exists"
                self.stdout.write(f"  {status}: Database {obj.db_name}")

            # 5. Backup Policies
            for db_idx, host_idx, client_idx, name, btype, dest, minute, hour, day, month, day_week, duration, size in DEMO_POLICIES:
                obj, created = BackupPolicy.objects.get_or_create(
                    policy_name=name,
                    defaults={
                        "database": databases[db_idx],
                        "host": hosts[host_idx],
                        "client": clients[client_idx],
                        "backup_type": btype,
                        "destination": dest,
                        "minute": minute,
                        "hour": hour,
                        "day": day,
                        "month": month,
                        "day_week": day_week,
                        "duration": duration,
                        "size_backup": size,
                        "status": "ACTIVE",
                        "description": f"Demo policy — {btype} to {dest}",
                        "created_by": admin,
                    },
                )
                status = "✓ Created" if created else "· Exists"
                self.stdout.write(f"  {status}: Policy '{obj.policy_name}'")

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Demo seed complete!"))
        self.stdout.write("")
        self.stdout.write("  Run the server:")
        self.stdout.write("  DJANGO_SETTINGS_MODULE=projectRelback.settings_local python manage.py runserver")
        self.stdout.write("")
        self.stdout.write("  Login: admin / demo1234")
        self.stdout.write("  Reports will show simulated RMAN backup jobs (DEMO_MODE=True).")
