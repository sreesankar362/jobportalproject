# Generated by Django 4.1.1 on 2022-10-14 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0002_remove_membership_type_membership_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
