# Generated by Django 2.2.7 on 2020-01-02 20:51

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finder', '0017_auto_20200102_2249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizationprofile',
            name='address',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True),
        ),
    ]
