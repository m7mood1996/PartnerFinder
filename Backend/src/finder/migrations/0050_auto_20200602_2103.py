# Generated by Django 2.2.10 on 2020-06-02 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finder', '0049_auto_20200602_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_part',
            field=models.ManyToManyField(blank=True, related_name='Part_Event', to='finder.Participants'),
        ),
    ]
