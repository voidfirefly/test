# Generated by Django 2.0.3 on 2018-06-02 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('answers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='answers.Answer')),
            ],
            options={
                'verbose_name': 'Лог ответов',
                'verbose_name_plural': 'Логи ответов',
            },
        ),
    ]
