# Generated by Django 3.2 on 2022-06-27 01:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gamification', '0011_auto_20220626_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='date_created',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='date created'),
        ),
    ]
