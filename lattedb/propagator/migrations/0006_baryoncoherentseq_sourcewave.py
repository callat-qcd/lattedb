# Generated by Django 2.2.7 on 2020-02-13 20:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wavefunction', '0005_remove_scswavefunction_type'),
        ('propagator', '0005_auto_20191127_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='baryoncoherentseq',
            name='sourcewave',
            field=models.ForeignKey(default=1, help_text='Foreign Key pointing to source operator `wavefunction`', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wavefunction.SCSWaveFunction'),
            preserve_default=False,
        ),
    ]
