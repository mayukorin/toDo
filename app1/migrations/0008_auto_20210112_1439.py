# Generated by Django 3.1.5 on 2021-01-12 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0007_task_done_flag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
