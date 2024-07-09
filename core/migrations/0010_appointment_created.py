# Generated by Django 5.0.6 on 2024-07-09 08:01

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_appointment'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
