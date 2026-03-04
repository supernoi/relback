# Phase 19 — Multi-tenant: default client for report scoping

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coreRelback', '0007_add_client_catalog_dsn'),
    ]

    operations = [
        migrations.AddField(
            model_name='relbackuser',
            name='default_client',
            field=models.ForeignKey(
                blank=True,
                db_column='default_id_client',
                help_text='Optional default client for Reports; catalog queries are scoped to this client when set.',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='users_default',
                to='coreRelback.client',
            ),
        ),
    ]
