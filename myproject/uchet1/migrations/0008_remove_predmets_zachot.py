# Generated by Django 5.1.6 on 2025-02-26 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uchet1', '0007_predmets_zachot'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='predmets',
            name='zachot',
        ),
    ]
