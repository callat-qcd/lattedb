# Generated by Django 2.2.5 on 2019-11-22 23:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ga_q2', '0002_auto_20191107_0016'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='onetoallstatus',
            name='type',
        ),
    ]