# Generated by Django 3.1.3 on 2021-01-31 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0025_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]