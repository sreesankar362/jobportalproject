# Generated by Django 4.1.1 on 2022-10-17 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='savedjobs',
            name='user',
        ),
        migrations.AddField(
            model_name='savedjobs',
            name='candidate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='candidate.candidateprofile'),
        ),
    ]