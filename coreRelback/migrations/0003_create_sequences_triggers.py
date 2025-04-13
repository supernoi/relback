from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        # Dependendo do número da migration inicial do seu app.
        ('coreRelback', '0001_initial', '0002_backuppolicy_client_database_host_relbackuser_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            -- Criação de sequence e trigger para a tabela USERS
            CREATE SEQUENCE users_seq START WITH 1000 INCREMENT BY 1 NOCACHE;

            CREATE OR REPLACE TRIGGER trg_users_bir
            BEFORE INSERT ON users
            FOR EACH ROW
            WHEN (new.id_user IS NULL)
            BEGIN
              SELECT users_seq.NEXTVAL INTO :new.id_user FROM dual;
            END;
            /

            -- Criação de sequence e trigger para a tabela CLIENTS
            CREATE SEQUENCE clients_seq START WITH 1000 INCREMENT BY 1 NOCACHE;

            CREATE OR REPLACE TRIGGER trg_clients_bir
            BEFORE INSERT ON clients
            FOR EACH ROW
            WHEN (new.id_client IS NULL)
            BEGIN
              SELECT clients_seq.NEXTVAL INTO :new.id_client FROM dual;
            END;
            /

            -- Criação de sequence e trigger para a tabela HOSTS
            CREATE SEQUENCE hosts_seq START WITH 1000 INCREMENT BY 1 NOCACHE;

            CREATE OR REPLACE TRIGGER trg_hosts_bir
            BEFORE INSERT ON hosts
            FOR EACH ROW
            WHEN (new.id_host IS NULL)
            BEGIN
              SELECT hosts_seq.NEXTVAL INTO :new.id_host FROM dual;
            END;
            /

            -- Semelhantemente, para DATABASES e BACKUP_POLICIES, se necessário:
            CREATE SEQUENCE databases_seq START WITH 1000 INCREMENT BY 1 NOCACHE;

            CREATE OR REPLACE TRIGGER trg_databases_bir
            BEFORE INSERT ON databases
            FOR EACH ROW
            WHEN (new.id_database IS NULL)
            BEGIN
              SELECT databases_seq.NEXTVAL INTO :new.id_database FROM dual;
            END;
            /

            CREATE SEQUENCE backup_policies_seq START WITH 1000 INCREMENT BY 1 NOCACHE;

            CREATE OR REPLACE TRIGGER trg_backup_policies_bir
            BEFORE INSERT ON backup_policies
            FOR EACH ROW
            WHEN (new.id_policy IS NULL)
            BEGIN
              SELECT backup_policies_seq.NEXTVAL INTO :new.id_policy FROM dual;
            END;
            /
            """,
            reverse_sql="""
            DROP TRIGGER trg_users_bir;
            DROP SEQUENCE users_seq;

            DROP TRIGGER trg_clients_bir;
            DROP SEQUENCE clients_seq;

            DROP TRIGGER trg_hosts_bir;
            DROP SEQUENCE hosts_seq;

            DROP TRIGGER trg_databases_bir;
            DROP SEQUENCE databases_seq;

            DROP TRIGGER trg_backup_policies_bir;
            DROP SEQUENCE backup_policies_seq;
            """
        ),
    ]
