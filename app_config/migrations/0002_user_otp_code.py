# Generated by Django 5.1.7 on 2025-03-18 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_config', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='otp_code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
