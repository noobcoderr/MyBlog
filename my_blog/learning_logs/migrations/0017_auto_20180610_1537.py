# Generated by Django 2.0.6 on 2018-06-10 15:37

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0016_auto_20180610_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
