# Generated by Django 3.1.3 on 2020-12-02 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0013_remove_fileuploader_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shift_result',
            name='file',
        ),
    ]
