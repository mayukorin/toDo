# Generated by Django 3.1.2 on 2020-12-27 05:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0003_task_site_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]