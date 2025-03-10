# Generated by Django 5.1.6 on 2025-02-19 08:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uchet1', '0002_remove_predmets_ind'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predmets',
            name='hours_1sem',
            field=models.IntegerField(default=0, verbose_name='Часы (1 семестр)'),
        ),
        migrations.AlterField(
            model_name='predmets',
            name='hours_2sem',
            field=models.IntegerField(default=0, verbose_name='Часы (2 семестр)'),
        ),
        migrations.AlterField(
            model_name='predmets',
            name='hours_remaining',
            field=models.IntegerField(default=0, verbose_name='Оставшиеся часы'),
        ),
        migrations.AlterField(
            model_name='predmets',
            name='hours_total',
            field=models.IntegerField(default=0, verbose_name='Общее количество часов'),
        ),
        migrations.AlterField(
            model_name='predmets',
            name='hours_used',
            field=models.IntegerField(default=0, verbose_name='Использованные часы'),
        ),
        migrations.AlterField(
            model_name='predmets',
            name='pairs_remaining',
            field=models.IntegerField(default=0, verbose_name='Оставшиеся пары'),
        ),
        migrations.CreateModel(
            name='SemesterGrade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.PositiveSmallIntegerField(choices=[(1, '1 семестр'), (2, '2 семестр')], verbose_name='Семестр')),
                ('final_score', models.FloatField(blank=True, null=True, verbose_name='Итоговая оценка')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uchet1.student', verbose_name='Студент')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uchet1.predmets', verbose_name='Предмет')),
            ],
        ),
    ]
