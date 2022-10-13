# Generated by Django 4.1.1 on 2022-10-13 05:59

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100)),
                ('company_logo', models.ImageField(blank=True, null=True, upload_to='company_images', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])])),
                ('company_description', models.CharField(blank=True, max_length=500, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('industry', models.CharField(blank=True, max_length=100, null=True)),
                ('category', models.CharField(blank=True, max_length=100, null=True)),
                ('team_size', models.CharField(blank=True, choices=[('0-100', '0-100'), ('100-500', '100-500'), ('500-1000', '500-1000'), ('1000+', '1000+')], max_length=10, null=True)),
                ('founded', models.PositiveIntegerField(blank=True, null=True)),
                ('company_address', models.TextField(blank=True, max_length=250, null=True)),
                ('is_activated', models.BooleanField(default=False)),
                ('is_approved', models.BooleanField(default=False)),
                ('is_mail_verified', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
