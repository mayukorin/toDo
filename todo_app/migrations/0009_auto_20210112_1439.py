# Generated by Django 3.1.5 on 2021-01-12 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0008_auto_20210112_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
