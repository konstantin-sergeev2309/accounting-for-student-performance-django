# Generated by Django 5.1.6 on 2025-02-23 08:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uchet1', '0005_grade_semester_pa_semester'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='prepod',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='uchet1.prepods', verbose_name='Преподаватель'),
        ),
    ]
