# Generated by Django 3.1.3 on 2020-12-02 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0011_auto_20201202_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileuploader',
            name='file',
            field=models.FileField(default='None', upload_to='files/'),
        ),
    ]
