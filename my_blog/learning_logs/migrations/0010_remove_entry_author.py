# Generated by Django 2.0.6 on 2018-06-09 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0009_auto_20180609_1530'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='author',
        ),
    ]