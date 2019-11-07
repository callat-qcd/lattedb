# Generated by Django 2.2.5 on 2019-10-30 23:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('current', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wavefunction', '0001_initial'),
        ('propagator', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Correlator',
            fields=[
                ('id', models.AutoField(help_text='Primary key for Base class.', primary_key=True, serialize=False)),
                ('type', models.TextField(editable=False, help_text='Type for the base class. Will be auto set to specialized type on save')),
                ('last_modified', models.DateTimeField(auto_now=True, help_text='Date the class was last modified')),
                ('tag', models.CharField(blank=True, help_text='User defined tag for easy searches', max_length=20, null=True)),
                ('user', models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Ananymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Meson2pt',
            fields=[
                ('correlator_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='correlator.Correlator')),
                ('propagator0', models.ForeignKey(help_text='ForeignKey: Pointer to first propagator', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='propagator.Propagator')),
                ('propagator1', models.ForeignKey(help_text='ForeignKey: Pointer to second propagator', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='propagator.Propagator')),
                ('sinkwave', models.ForeignKey(help_text='ForeignKey: Pointer to sink interpolating operator', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wavefunction.SCSWaveFunction')),
                ('sourcewave', models.ForeignKey(help_text='ForeignKey: Pointer to source interpolating operator', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wavefunction.SCSWaveFunction')),
            ],
            bases=('correlator.correlator',),
        ),
        migrations.CreateModel(
            name='DWFTuning',
            fields=[
                ('correlator_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='correlator.Correlator')),
                ('sink5', models.BooleanField(help_text='Boolean: Is the sink on the domain wall?')),
                ('propagator', models.ForeignKey(help_text='ForeignKey: Pointer to first propagator', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='propagator.Propagator')),
                ('wave', models.ForeignKey(help_text='ForeignKey: Pointer to source spin color space wave function', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wavefunction.SCSWaveFunction')),
            ],
            bases=('correlator.correlator',),
        ),
        migrations.CreateModel(
            name='BaryonSeq3pt',
            fields=[
                ('correlator_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='correlator.Correlator')),
                ('current', models.ForeignKey(help_text='Foreign Key to current interaction operator', on_delete=django.db.models.deletion.CASCADE, to='current.Current')),
                ('propagator', models.ForeignKey(help_text='Foreign Key pointing to daughter quark', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='propagator.Propagator')),
                ('seqpropagator', models.ForeignKey(help_text='Foreign Key pointing to sequential propagator (2 spectator quarks + 1 daughter)', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='propagator.Propagator')),
                ('sourcewave', models.ForeignKey(help_text='Foreign Key pointing to source operator', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wavefunction.SCSWaveFunction')),
            ],
            bases=('correlator.correlator',),
        ),
        migrations.CreateModel(
            name='BaryonFH3pt',
            fields=[
                ('correlator_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='correlator.Correlator')),
                ('fhpropagator', models.ForeignKey(help_text='Foreign Key pointing to Feynman-Hellmann propagator', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='propagator.Propagator')),
                ('propagator0', models.ForeignKey(help_text='Foreign Key pointing to spectator propagator', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='propagator.Propagator')),
                ('propagator1', models.ForeignKey(help_text='Foreign Key pointing to spectator propagator', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='propagator.Propagator')),
                ('sinkwave', models.ForeignKey(help_text='Foreign Key pointing to sink operator', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wavefunction.SCSWaveFunction')),
                ('sourcewave', models.ForeignKey(help_text='Foreign Key pointing to source operator', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wavefunction.SCSWaveFunction')),
            ],
            bases=('correlator.correlator',),
        ),
        migrations.CreateModel(
            name='Baryon2pt',
            fields=[
                ('correlator_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='correlator.Correlator')),
                ('propagator0', models.ForeignKey(help_text='ForeignKey: Pointer to first propagator', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='propagator.Propagator')),
                ('propagator1', models.ForeignKey(help_text='ForeignKey: Pointer to second propagator', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='propagator.Propagator')),
                ('propagator2', models.ForeignKey(help_text='ForeignKey: Pointer to third propagator', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='propagator.Propagator')),
                ('sinkwave', models.ForeignKey(help_text='ForeignKey: Pointer to sink interpolating operator', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wavefunction.SCSWaveFunction')),
                ('sourcewave', models.ForeignKey(help_text='ForeignKey: Pointer to source interpolating operator', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wavefunction.SCSWaveFunction')),
            ],
            bases=('correlator.correlator',),
        ),
        migrations.AddConstraint(
            model_name='meson2pt',
            constraint=models.UniqueConstraint(fields=('propagator0', 'propagator1', 'sourcewave', 'sinkwave'), name='unique_correlator_meson2pt'),
        ),
        migrations.AddConstraint(
            model_name='dwftuning',
            constraint=models.UniqueConstraint(fields=('propagator', 'wave', 'sink5'), name='unique_correlator_dwftuning'),
        ),
        migrations.AddConstraint(
            model_name='baryonseq3pt',
            constraint=models.UniqueConstraint(fields=('sourcewave', 'current', 'seqpropagator', 'propagator'), name='unique_correlator_baryonseq3pt'),
        ),
        migrations.AddConstraint(
            model_name='baryonfh3pt',
            constraint=models.UniqueConstraint(fields=('sourcewave', 'fhpropagator', 'propagator0', 'propagator1', 'sinkwave'), name='unique_correlator_baryonfh3pt'),
        ),
        migrations.AddConstraint(
            model_name='baryon2pt',
            constraint=models.UniqueConstraint(fields=('propagator0', 'propagator1', 'propagator2', 'sourcewave', 'sinkwave'), name='unique_correlator_baryon2pt'),
        ),
    ]