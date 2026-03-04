# Generated manually for Phase 16 — User Roles & Permissions

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("coreRelback", "0006_add_user_preferences"),
    ]

    operations = [
        migrations.AddField(
            model_name="relbackuser",
            name="role",
            field=models.CharField(
                choices=[
                    ("admin", "Administrator"),
                    ("operator", "Operator"),
                    ("viewer", "Viewer"),
                ],
                default="operator",
                help_text="admin: full access; operator: create/update; viewer: read-only",
                max_length=20,
            ),
        ),
    ]
