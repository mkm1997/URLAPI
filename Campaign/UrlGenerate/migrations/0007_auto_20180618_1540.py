# Generated by Django 2.0.6 on 2018-06-18 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UrlGenerate', '0006_auto_20180618_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hit',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]