# Generated by Django 4.1.1 on 2022-10-16 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobmodel',
            name='max_experience',
            field=models.PositiveIntegerField(blank=True, max_length=20, null=True),
        ),
    ]
