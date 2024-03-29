# Generated by Django 3.1.3 on 2020-12-01 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_balance_modifier_history_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balance_modifier_history',
            name='comment',
            field=models.TextField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='shift_result',
            name='operation_result',
            field=models.BooleanField(default=False),
        ),
    ]
