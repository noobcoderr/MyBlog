# Generated by Django 2.0.6 on 2018-06-14 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0023_auto_20180612_1647'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReadNum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('views', models.IntegerField(default=0)),
                ('entry', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='learning_logs.Entry')),
            ],
        ),
    ]
