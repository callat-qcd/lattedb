# Generated by Django 2.2.5 on 2019-11-22 19:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('propagator', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='baryoncoherentseq',
            name='unique_propagator_coherentseq',
        ),
        migrations.RemoveField(
            model_name='baryoncoherentseq',
            name='groupindex',
        ),
        migrations.RemoveField(
            model_name='baryoncoherentseq',
            name='groupsize',
        ),
        migrations.RemoveField(
            model_name='baryoncoherentseq',
            name='sourcesmear',
        ),
        migrations.AlterField(
            model_name='baryoncoherentseq',
            name='fermionaction',
            field=models.ForeignKey(help_text='Foreign Key referencing valence lattice `fermionaction`', on_delete=django.db.models.deletion.CASCADE, to='fermionaction.FermionAction'),
        ),
        migrations.AlterField(
            model_name='baryoncoherentseq',
            name='gaugeconfig',
            field=models.ForeignKey(help_text='Foreign Key referencing specific `gaugeconfig` inverted on', on_delete=django.db.models.deletion.CASCADE, to='gaugeconfig.GaugeConfig'),
        ),
        migrations.RemoveField(
            model_name='baryoncoherentseq',
            name='propagator0',
        ),
        migrations.AddField(
            model_name='baryoncoherentseq',
            name='propagator0',
            field=models.ManyToManyField(help_text='A set of Foreign Keys referencing OneToAll `propagator` (spectator 0) in same source group', related_name='baryoncoherentseq_set0', to='propagator.Propagator'),
        ),
        migrations.RemoveField(
            model_name='baryoncoherentseq',
            name='propagator1',
        ),
        migrations.AddField(
            model_name='baryoncoherentseq',
            name='propagator1',
            field=models.ManyToManyField(help_text='A set of Foreign Keys referencing OneToAll `propagator` (spectator 1) in same source group', related_name='baryoncoherentseq_set1', to='propagator.Propagator'),
        ),
        migrations.AlterField(
            model_name='baryoncoherentseq',
            name='sinksep',
            field=models.SmallIntegerField(help_text='Source-sink separation time'),
        ),
        migrations.AlterField(
            model_name='baryoncoherentseq',
            name='sinksmear',
            field=models.ForeignKey(help_text='Foreign Key pointing to sink `quarksmear`', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='quarksmear.QuarkSmear'),
        ),
        migrations.AlterField(
            model_name='baryoncoherentseq',
            name='sinkwave',
            field=models.ForeignKey(help_text='Foreign Key referencing sink interpolating operator `wavefunction`', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wavefunction.SCSWaveFunction'),
        ),
        migrations.AlterField(
            model_name='feynmanhellmann',
            name='current',
            field=models.ForeignKey(help_text='Foreign Key linking momentum space `current` insertion', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='current.Current'),
        ),
        migrations.AlterField(
            model_name='feynmanhellmann',
            name='fermionaction',
            field=models.ForeignKey(help_text='Foreign Key pointing to valence lattice `fermionaction`', on_delete=django.db.models.deletion.CASCADE, to='fermionaction.FermionAction'),
        ),
        migrations.AlterField(
            model_name='feynmanhellmann',
            name='gaugeconfig',
            field=models.ForeignKey(help_text='Foreign Key pointing to specific `gaugeconfig` inverted on', on_delete=django.db.models.deletion.CASCADE, to='gaugeconfig.GaugeConfig'),
        ),
        migrations.AlterField(
            model_name='feynmanhellmann',
            name='propagator',
            field=models.ForeignKey(help_text='Foreign Key linking RHS OneToAll `propagator`', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='propagator.Propagator'),
        ),
        migrations.AlterField(
            model_name='feynmanhellmann',
            name='sinksmear',
            field=models.ForeignKey(help_text='Foreign Key pointing to sink `quarksmear`', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='quarksmear.QuarkSmear'),
        ),
        migrations.AlterField(
            model_name='feynmanhellmann',
            name='sourcesmear',
            field=models.ForeignKey(help_text='Foreign Key pointing to source `quarksmear`', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='quarksmear.QuarkSmear'),
        ),
        migrations.AlterField(
            model_name='onetoall',
            name='fermionaction',
            field=models.ForeignKey(help_text='Foreign Key pointing to valence lattice `fermionaction`. This is the valence action.', on_delete=django.db.models.deletion.CASCADE, to='fermionaction.FermionAction'),
        ),
        migrations.AlterField(
            model_name='onetoall',
            name='gaugeconfig',
            field=models.ForeignKey(help_text='Foreign Key pointing to specific \\texttt{gaugeconfig} inverted on', on_delete=django.db.models.deletion.CASCADE, to='gaugeconfig.GaugeConfig'),
        ),
        migrations.AlterField(
            model_name='onetoall',
            name='origin_t',
            field=models.PositiveSmallIntegerField(help_text='t-coordinate origin location of the propagator'),
        ),
        migrations.AlterField(
            model_name='onetoall',
            name='origin_x',
            field=models.PositiveSmallIntegerField(help_text='x-coordinate origin location of the propagator'),
        ),
        migrations.AlterField(
            model_name='onetoall',
            name='origin_y',
            field=models.PositiveSmallIntegerField(help_text='y-coordinate origin location of the propagator'),
        ),
        migrations.AlterField(
            model_name='onetoall',
            name='origin_z',
            field=models.PositiveSmallIntegerField(help_text='z-coordinate origin location of the propagator'),
        ),
        migrations.AlterField(
            model_name='onetoall',
            name='sinksmear',
            field=models.ForeignKey(help_text='Foreign Key pointing to sink `quarksmear`', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='quarksmear.QuarkSmear'),
        ),
        migrations.AlterField(
            model_name='onetoall',
            name='sourcesmear',
            field=models.ForeignKey(help_text='Foreign Key pointing to source `quarksmear`', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='quarksmear.QuarkSmear'),
        ),
        migrations.AlterField(
            model_name='propagator',
            name='tag',
            field=models.CharField(blank=True, help_text='User defined tag for easy searches', max_length=200, null=True),
        ),
        migrations.AddConstraint(
            model_name='baryoncoherentseq',
            constraint=models.UniqueConstraint(fields=('gaugeconfig', 'fermionaction', 'sinkwave', 'sinksmear', 'sinksep'), name='unique_propagator_baryoncoherentseq'),
        ),
    ]
