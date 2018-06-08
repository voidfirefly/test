# Generated by Django 2.0.3 on 2018-06-08 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0008_auto_20180526_2012'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestKlassDepence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('klass', models.CharField(blank=True, max_length=255, null=True, verbose_name='Класс вопроса')),
                ('count', models.PositiveSmallIntegerField(default=0)),
                ('appointed_test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tests.AppointedTest', verbose_name='Назначение')),
                ('available_test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tests.AvailableTest', verbose_name='Доступ')),
            ],
            options={
                'verbose_name': 'Класс вопроса',
                'verbose_name_plural': 'Классы вопросов',
            },
        ),
    ]