# Generated by Django 2.0.6 on 2018-06-18 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UrlGenerate', '0008_auto_20180618_1546'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hit',
            old_name='date',
            new_name='my_date',
        ),
    ]
