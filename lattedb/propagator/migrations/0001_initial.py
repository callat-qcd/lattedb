# Generated by Django 2.2.2 on 2019-08-26 22:46

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gaugeconfig', '0001_initial'),
        ('current', '0001_initial'),
        ('fermionaction', '0001_initial'),
        ('interpolator', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Propagator',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.TextField(editable=False)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('tag', models.CharField(blank=True, help_text='(Optional) Char(20): User defined tag for easy searches', max_length=20, null=True)),
                ('misc', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text="(Optional) JSON: {'anything': 'you want'}", null=True)),
                ('fermionaction', models.ForeignKey(help_text='ForeignKey pointing to valence lattice fermion action', on_delete=django.db.models.deletion.CASCADE, to='fermionaction.FermionAction')),
                ('gaugeconfig', models.ForeignKey(help_text='ForeignKey pointing to specific gauge configuration inverted on', on_delete=django.db.models.deletion.CASCADE, to='gaugeconfig.GaugeConfig')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CoherentSeq',
            fields=[
                ('propagator_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='propagator.Propagator')),
                ('groupsize', models.PositiveSmallIntegerField(help_text='PositiveSmallint: Total number of propagators sharing a coherent sink')),
                ('groupindex', models.PositiveSmallIntegerField(help_text='PositiveSmallInt: A group index indicating which coherent sink group the propagator belongs to')),
                ('sinksep', models.SmallIntegerField(help_text='SmallInt: Source-sink separation time')),
            ],
            bases=('propagator.propagator',),
        ),
        migrations.CreateModel(
            name='FeynmanHellmann',
            fields=[
                ('propagator_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='propagator.Propagator')),
            ],
            bases=('propagator.propagator',),
        ),
        migrations.CreateModel(
            name='OneToAll',
            fields=[
                ('propagator_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='propagator.Propagator')),
                ('origin_x', models.PositiveSmallIntegerField(help_text='PositiveSmallInt: x-coordinate origin location of the propagator')),
                ('origin_y', models.PositiveSmallIntegerField(help_text='PositiveSmallInt: y-coordinate origin location of the propagator')),
                ('origin_z', models.PositiveSmallIntegerField(help_text='PositiveSmallInt: z-coordinate origin location of the propagator')),
                ('origin_t', models.PositiveSmallIntegerField(help_text='PositiveSmallInt: t-coordinate origin location of the propagator')),
            ],
            bases=('propagator.propagator',),
        ),
        migrations.AddConstraint(
            model_name='propagator',
            constraint=models.UniqueConstraint(fields=('gaugeconfig', 'fermionaction'), name='unique_propagator'),
        ),
        migrations.AddConstraint(
            model_name='onetoall',
            constraint=models.UniqueConstraint(fields=('propagator_ptr_id', 'origin_x', 'origin_y', 'origin_z', 'origin_t'), name='unique_propagator_onetoall'),
        ),
        migrations.AddField(
            model_name='feynmanhellmann',
            name='current',
            field=models.ForeignKey(help_text='ForeignKey linking momentum space current insertion', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='current.Current'),
        ),
        migrations.AddField(
            model_name='feynmanhellmann',
            name='propagator',
            field=models.ForeignKey(help_text='ForeignKey linking RHS propagator', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='propagator.Propagator'),
        ),
        migrations.AddField(
            model_name='coherentseq',
            name='propagator0',
            field=models.ForeignKey(help_text='ForeignKey that link to a coherent propagator (spectator 0)', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='propagator.Propagator'),
        ),
        migrations.AddField(
            model_name='coherentseq',
            name='propagator1',
            field=models.ForeignKey(help_text='ForeignKey that link to a coherent propagator (spectator 1)', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='propagator.Propagator'),
        ),
        migrations.AddField(
            model_name='coherentseq',
            name='sink',
            field=models.ForeignKey(help_text='ForeignKey: Pointer to sink interpolating operator', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='interpolator.Interpolator'),
        ),
        migrations.AddConstraint(
            model_name='feynmanhellmann',
            constraint=models.UniqueConstraint(fields=('propagator_ptr_id', 'propagator', 'current'), name='unique_propagator_feynmanhellmann'),
        ),
        migrations.AddConstraint(
            model_name='coherentseq',
            constraint=models.UniqueConstraint(fields=('propagator_ptr_id', 'propagator0', 'propagator1', 'groupsize', 'groupindex', 'sink', 'sinksep'), name='unique_propagator_coherentseq'),
        ),
    ]