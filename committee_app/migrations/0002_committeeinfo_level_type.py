# Generated by Django 4.2.10 on 2024-02-19 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('committee_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='committeeinfo',
            name='level_type',
            field=models.CharField(blank=True, max_length=500, null=True, unique=True, verbose_name='Level Type'),
        ),
    ]
