# Generated by Django 4.1.1 on 2022-10-06 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('companyaccount', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=100)),
                ('job_description', models.TextField(max_length=800)),
                ('skills', models.TextField(max_length=200)),
                ('job_type', models.CharField(choices=[('full-time', 'full time'), ('part-time', 'Part Time'), ('temporary', 'Temporary'), ('contract', 'Contract'), ('feelance', 'Freelance')], max_length=50)),
                ('published_date', models.DateTimeField(auto_now=True, null=True)),
                ('application_end_date', models.DateField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('experience', models.CharField(blank=True, max_length=20, null=True)),
                ('min_salary', models.IntegerField(blank=True, null=True)),
                ('max_salary', models.IntegerField(blank=True, null=True)),
                ('min_qualification', models.CharField(blank=True, max_length=100, null=True)),
                ('categories', models.CharField(max_length=100)),
                ('work_type', models.CharField(choices=[('wfh', 'Work from Home'), ('wfo', 'Work from Office'), ('hybrid', 'Hybrid')], max_length=50)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employer', to='companyaccount.companyprofile')),
            ],
        ),
    ]
