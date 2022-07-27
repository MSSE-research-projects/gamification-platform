# Generated by Django 3.2 on 2022-07-27 04:11

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gamification', '0002_change_site_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artifact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload_time', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='upload time')),
                ('file', models.FileField(blank=True, upload_to='assignment_files', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name='assignment file')),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamification.assignment')),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamification.entity')),
            ],
            options={
                'verbose_name': 'artifact',
                'verbose_name_plural': 'artifacts',
                'db_table': 'artifact',
            },
        ),
        migrations.CreateModel(
            name='ArtifactReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artifact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamification.artifact')),
                ('regisration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamification.registration')),
            ],
            options={
                'verbose_name': 'artifact_review',
                'verbose_name_plural': 'artifact_reviews',
                'db_table': 'artifact_review',
            },
        ),
        migrations.CreateModel(
            name='OptionChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'option choice',
                'verbose_name_plural': 'option choices',
                'db_table': 'option_choice',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True)),
                ('is_required', models.BooleanField(default=False)),
                ('is_multiple', models.BooleanField(default=False)),
                ('question_type', models.TextField(choices=[('MULTIPLETEXT', 'Multipletext'), ('FIXEDTEXT', 'Fixedtext'), ('MULTIPLECHOICE', 'Multiplechoice')], default='MULTIPLECHOICE')),
                ('dependent_question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gamification.question')),
            ],
            options={
                'verbose_name': 'question',
                'verbose_name_plural': 'questions',
                'db_table': 'question',
            },
        ),
        migrations.CreateModel(
            name='SurveyTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('instructions', models.TextField(blank=True)),
                ('other_info', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'survey template',
                'verbose_name_plural': 'survey templates',
                'db_table': 'survey_template',
            },
        ),
        migrations.CreateModel(
            name='SurveySection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True)),
                ('is_required', models.BooleanField(default=False)),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamification.surveytemplate')),
            ],
            options={
                'verbose_name': 'survey section',
                'verbose_name_plural': 'survey sections',
                'db_table': 'survey_section',
            },
        ),
        migrations.CreateModel(
            name='QuestionOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_text', models.IntegerField(default=1)),
                ('option_choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamification.optionchoice')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamification.question')),
            ],
            options={
                'verbose_name': 'question option',
                'verbose_name_plural': 'question options',
                'db_table': 'question_option',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='option_choices',
            field=models.ManyToManyField(through='gamification.QuestionOption', to='gamification.OptionChoice'),
        ),
        migrations.AddField(
            model_name='question',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamification.surveysection'),
        ),
        migrations.CreateModel(
            name='FeedbackSurvey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_released', models.DateTimeField(blank=True, null=True)),
                ('date_due', models.DateTimeField(blank=True, null=True)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamification.assignment')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamification.surveytemplate')),
            ],
            options={
                'verbose_name': 'feedback survey',
                'verbose_name_plural': 'feedback surveys',
                'db_table': 'feedback_survey',
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, max_length=800)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('permission_level', models.TextField(choices=[('Public', 'Public'), ('Private', 'Private')], default='Public')),
                ('parent_node', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gamification.feedback')),
                ('review_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamification.artifactreview')),
            ],
            options={
                'verbose_name': 'feedback',
                'verbose_name_plural': 'feedbacks',
                'db_table': 'feedback',
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answerText', models.TextField(blank=True)),
                ('artifact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamification.artifact')),
                ('questionOption', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamification.questionoption')),
                ('registration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamification.registration')),
            ],
            options={
                'verbose_name': 'answer',
                'verbose_name_plural': 'answers',
                'db_table': 'answer',
            },
        ),
    ]
