# Generated by Django 3.2 on 2022-06-14 07:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamification', '0005_alter_customuser_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='customuser',
            table='users',
        ),
    ]
