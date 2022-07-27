# Generated by Django 3.2 on 2022-07-15 08:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamification', '0004_alter_artifact_upload_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artifact',
            name='file',
            field=models.FileField(blank=True, upload_to='assignment_files', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt', 'zip', 'rar', '7z', 'gz', 'tar', 'bz2', 'bzip2', 'bz', 'bzip', 'bzp', 'bzt', 'bz2', 'bz3'])], verbose_name='assignment file'),
        ),
    ]
