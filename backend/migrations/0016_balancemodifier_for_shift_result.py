# Generated by Django 3.1.3 on 2020-12-04 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0015_auto_20201203_2249'),
    ]

    operations = [
        migrations.AddField(
            model_name='balancemodifier',
            name='for_shift_result',
            field=models.BooleanField(default=False),
        ),
    ]
