# Generated by Django 3.2 on 2022-12-13 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamification', '0009_alter_progress_cur_point'),
    ]

    operations = [
        migrations.AddField(
            model_name='constraint',
            name='description',
            field=models.TextField(blank=True, verbose_name='description'),
        ),
    ]
