# Phase 19 — Multi-tenant: optional per-client RMAN catalog DSN

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreRelback', '0006_add_user_preferences'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='catalog_dsn',
            field=models.CharField(
                blank=True,
                help_text='Optional Oracle RMAN catalog DSN for this client (e.g. host:port/service). When set, report queries use this catalog; credentials from ORACLE_CATALOG_*.',
                max_length=256,
                null=True,
            ),
        ),
    ]
