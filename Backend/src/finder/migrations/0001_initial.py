# Generated by Django 2.2.7 on 2020-01-02 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.IntegerField(unique=True)),
                ('legalName', models.CharField(max_length=200)),
                ('businessName', models.CharField(max_length=200)),
                ('classificationType', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('address', models.TextField()),
                ('tagsAndKeywords', models.TextField()),
            ],
        ),
    ]
