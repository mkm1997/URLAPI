# Generated by Django 2.0.6 on 2018-06-18 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UrlGenerate', '0009_auto_20180618_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hit',
            name='my_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]