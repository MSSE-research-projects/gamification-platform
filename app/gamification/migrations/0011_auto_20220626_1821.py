# Generated by Django 3.2 on 2022-06-27 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamification', '0010_auto_20220626_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='total_score',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='weight',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
