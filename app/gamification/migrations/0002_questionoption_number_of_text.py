# Generated by Django 3.2 on 2022-07-19 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamification', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionoption',
            name='number_of_text',
            field=models.IntegerField(default=1),
        ),
    ]