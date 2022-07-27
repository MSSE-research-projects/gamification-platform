# Generated by Django 3.2 on 2022-07-15 08:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gamification', '0003_artifact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artifact',
            name='upload_time',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='upload_time'),
        ),
    ]
