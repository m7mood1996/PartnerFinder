# Generated by Django 2.2.7 on 2020-01-02 20:47

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finder', '0012_remove_organizationprofile_tagsandkeywords'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationprofile',
            name='tagsAndKeywords',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), default=1, size=None),
            preserve_default=False,
        ),
    ]
