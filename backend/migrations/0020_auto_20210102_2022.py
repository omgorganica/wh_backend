# Generated by Django 3.1.3 on 2021-01-02 15:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0019_auto_20201221_1103'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shifts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('picking', models.IntegerField()),
                ('transportations', models.IntegerField()),
                ('loading', models.IntegerField()),
                ('result', models.DecimalField(decimal_places=1, default=0, max_digits=3)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shifts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='ShiftResult',
        ),
    ]
