# Generated by Django 2.0.6 on 2018-06-12 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0022_auto_20180612_1501'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='topic',
            options={'ordering': ['date_add']},
        ),
    ]
