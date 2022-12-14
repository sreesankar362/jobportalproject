# Generated by Django 4.1.1 on 2022-10-19 08:31

import autoslug.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0001_initial'),
        ('companyaccount', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CandidateProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('total_exp', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('summary', models.TextField(blank=True, max_length=500, null=True)),
                ('candidate_image', models.ImageField(blank=True, null=True, upload_to='candidate_images', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])])),
                ('dob', models.DateField(blank=True, null=True)),
                ('resume', models.FileField(blank=True, null=True, upload_to='resumes')),
                ('languages_known', models.CharField(blank=True, max_length=300, null=True)),
                ('skills', models.CharField(blank=True, max_length=300, null=True)),
                ('address', models.TextField(blank=True, max_length=350, null=True)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('state', models.CharField(blank=True, max_length=255, null=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='user', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='LatEducation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qualification', models.CharField(blank=True, max_length=255, null=True)),
                ('institute', models.CharField(blank=True, max_length=50, null=True)),
                ('university', models.CharField(blank=True, max_length=50, null=True)),
                ('percent', models.IntegerField(validators=[django.core.validators.MinValueValidator(25), django.core.validators.MaxValueValidator(100)])),
                ('passed_year', models.IntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SavedJobs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('candidate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='candidate.candidateprofile')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_job', to='home.jobmodel')),
            ],
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_status', models.CharField(default='applied', max_length=20)),
                ('applied_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('processed_date', models.DateTimeField(blank=True, null=True)),
                ('candidate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='candidate.candidateprofile')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='companyaccount.companyprofile')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.jobmodel')),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experience_field', models.CharField(blank=True, max_length=255, null=True)),
                ('job_position', models.CharField(blank=True, max_length=50, null=True)),
                ('company', models.CharField(blank=True, max_length=50, null=True)),
                ('experience_describe', models.TextField(blank=True, max_length=300, null=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('exp_duration', models.IntegerField(default=0)),
                ('candidate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exp', to='candidate.candidateprofile')),
            ],
        ),
        migrations.AddField(
            model_name='candidateprofile',
            name='latest_edu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='candidate.lateducation'),
        ),
    ]
