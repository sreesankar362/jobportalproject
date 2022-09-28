# Generated by Django 4.1.1 on 2022-09-28 07:30

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companyaccount', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='type',
        ),
        migrations.RemoveField(
            model_name='company',
            name='user',
        ),
        migrations.AlterField(
            model_name='company',
            name='company_logo',
            field=models.ImageField(null=True, upload_to='company_images', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])]),
        ),
        migrations.AlterField(
            model_name='company',
            name='location',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='social_profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='companyaccount.socialprofile'),
        ),
        migrations.AlterField(
            model_name='company',
            name='team_size',
            field=models.CharField(choices=[('0-100', '0-100'), ('100-500', '100-500'), ('500-1000', '500-1000'), ('1000+', '1000+')], max_length=10, null=True),
        ),
    ]