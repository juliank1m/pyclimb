# Generated migration for execution_time_ms field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0002_add_test_results'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='execution_time_ms',
            field=models.IntegerField(
                blank=True,
                help_text='Total wall-clock execution time in milliseconds',
                null=True,
            ),
        ),
    ]
