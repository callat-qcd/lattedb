# Generated by Django 2.2.5 on 2019-11-22 23:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wavefunction', '0004_auto_20191122_1932'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scswavefunction',
            name='type',
        ),
    ]
