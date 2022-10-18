# Generated by Django 4.1.1 on 2022-10-17 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('companyaccount', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=100)),
                ('message', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='JobModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=100)),
                ('job_description', models.TextField(max_length=800)),
                ('skills', models.TextField(max_length=200)),
                ('job_type', models.CharField(choices=[('Full Time', 'full time'), ('Part Time', 'Part Time'), ('Temporary', 'Temporary'), ('Contract', 'Contract'), ('Freelance', 'Freelance')], max_length=50)),
                ('published_date', models.DateTimeField(auto_now=True, null=True)),
                ('application_end_date', models.DateField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('experience', models.CharField(blank=True, max_length=20, null=True)),
                ('min_salary', models.IntegerField(blank=True, null=True)),
                ('max_salary', models.IntegerField(blank=True, null=True)),
                ('No_of_openings', models.IntegerField(blank=True, null=True)),
                ('min_qualification', models.CharField(blank=True, max_length=100, null=True)),
                ('categories', models.CharField(max_length=100)),
                ('work_type', models.CharField(choices=[('Work From Home', 'Work from Home'), ('Work From Office', 'Work from Office'), ('Hybrid', 'Hybrid')], max_length=50)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employer', to='companyaccount.companyprofile')),
            ],
        ),
    ]