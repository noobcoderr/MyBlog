# Generated by Django 2.0.6 on 2018-06-10 14:45

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0015_entry_entry_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='text',
            field=ckeditor.fields.RichTextField(),
        ),
    ]