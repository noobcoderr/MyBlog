# Generated by Django 2.0.6 on 2018-06-12 07:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0021_topic_abstract'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='topic',
            options={'ordering': ['-date_add']},
        ),
    ]