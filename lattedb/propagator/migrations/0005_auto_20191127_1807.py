# Generated by Django 2.2.5 on 2019-11-27 18:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('propagator', '0004_auto_20191123_0102'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='baryoncoherentseq',
            name='unique_propagator_baryoncoherentseq',
        ),
    ]
