# Generated by Django 3.1.3 on 2020-11-26 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_auto_20201125_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='balance_modifier_history',
            name='comment',
            field=models.TextField(default=0, max_length=300),
            preserve_default=False,
        ),
    ]
