<<<<<<< HEAD
# Generated by Django 4.1.1 on 2022-10-07 10:42

import autoslug.fields
import datetime
=======
# Generated by Django 4.1.1 on 2022-10-16 13:24

import autoslug.fields
>>>>>>> main
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
<<<<<<< HEAD
        ('home', '0002_jobmodel_no_of_openings_alter_jobmodel_job_type'),
=======
        ('companyaccount', '0001_initial'),
        ('home', '0001_initial'),
>>>>>>> main
    ]

    operations = [
        migrations.CreateModel(
<<<<<<< HEAD
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exp_field', models.CharField(blank=True, max_length=255, null=True)),
                ('exp_position', models.CharField(blank=True, max_length=50, null=True)),
                ('exp_company', models.CharField(blank=True, max_length=50, null=True)),
                ('exp_description', models.TextField(blank=True, max_length=300, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(default=datetime.date(2022, 10, 7))),
                ('exp_duration', models.IntegerField(default=0, editable=False)),
=======
            name='CandidateProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('total_exp', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('summary', models.TextField(blank=True, max_length=500, null=True)),
                ('candidate_image', models.ImageField(blank=True, default='candidate/default_image.jpg', null=True, upload_to='candidate_images', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])])),
                ('dob', models.DateField(blank=True, null=True)),
                ('resume', models.FileField(blank=True, null=True, upload_to='resumes')),
                ('languages_known', models.CharField(blank=True, max_length=300, null=True)),
                ('skills', models.CharField(blank=True, max_length=300, null=True)),
                ('address', models.TextField(blank=True, max_length=350, null=True)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('state', models.CharField(blank=True, max_length=255, null=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='user', unique=True)),
>>>>>>> main
            ],
        ),
        migrations.CreateModel(
            name='LatEducation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
<<<<<<< HEAD
                ('qual_name', models.CharField(blank=True, max_length=255, null=True)),
                ('qual_institute', models.CharField(blank=True, max_length=50, null=True)),
                ('qual_university', models.CharField(blank=True, max_length=50, null=True)),
                ('percent', models.IntegerField(validators=[django.core.validators.MinValueValidator(25), django.core.validators.MaxValueValidator(100)])),
                ('grad_year', models.IntegerField(blank=True)),
                ('qual_country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills', to=settings.AUTH_USER_MODEL)),
=======
                ('qualification', models.CharField(blank=True, max_length=255, null=True)),
                ('institute', models.CharField(blank=True, max_length=50, null=True)),
                ('university', models.CharField(blank=True, max_length=50, null=True)),
                ('percent', models.IntegerField(validators=[django.core.validators.MinValueValidator(25), django.core.validators.MaxValueValidator(100)])),
                ('passed_year', models.IntegerField(blank=True)),
>>>>>>> main
            ],
        ),
        migrations.CreateModel(
            name='SavedJobs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_job', to='home.jobmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
<<<<<<< HEAD
            name='CandidateProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('dob', models.DateField(blank=True, max_length=8, null=True)),
                ('resume', models.FileField(blank=True, null=True, upload_to='resumes')),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='user', unique=True)),
                ('experience', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='candidate.experience')),
                ('latest_edu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='candidate.lateducation')),
            ],
        ),
        migrations.CreateModel(
            name='AppliedJobs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applied_job', to='home.jobmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applied_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
=======
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
>>>>>>> main
    ]
