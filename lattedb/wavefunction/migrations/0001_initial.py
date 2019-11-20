# Generated by Django 2.2.5 on 2019-10-30 23:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SCSWaveFunction',
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
            name='Hadron',
            fields=[
                ('scswavefunction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wavefunction.SCSWaveFunction')),
                ('description', models.TextField(blank=True, help_text='(Optional) Text: Description of the interpolating operator', null=True)),
                ('strangeness', models.PositiveSmallIntegerField(help_text='PositiveSmallIntegerField: Strangeness of hadronic operator')),
                ('irrep', models.TextField(help_text='Text: Irreducible representations of O^D_h (octahedral group)')),
                ('embedding', models.PositiveSmallIntegerField(help_text='PositiveSmallIntegerField: k-th embedding of O^D_h irrep.')),
                ('parity', models.SmallIntegerField(help_text='SmallIntegerField: Parity of hadronic operator')),
                ('spin_x2', models.PositiveSmallIntegerField(help_text='Text: Total spin times two')),
                ('spin_z_x2', models.SmallIntegerField(help_text='Text: Spin in z-direction')),
                ('isospin_x2', models.PositiveSmallIntegerField(help_text='Text: Total isospin times two')),
                ('isospin_z_x2', models.SmallIntegerField(help_text='Text: Isospin in z-direction times two')),
                ('momentum', models.SmallIntegerField(help_text='SmallInt: Momentum in units of 2 pi / L')),
            ],
            bases=('wavefunction.scswavefunction',),
        ),
        migrations.CreateModel(
            name='Hadron4D',
            fields=[
                ('scswavefunction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wavefunction.SCSWaveFunction')),
                ('description', models.TextField(blank=True, help_text='(Optional) Text: Description of the interpolating operator', null=True)),
                ('strangeness', models.PositiveSmallIntegerField(help_text='PositiveSmallIntegerField: Strangeness of hadronic operator')),
                ('irrep', models.TextField(help_text='Text: Irreducible representations of O^D_h (octahedral group)')),
                ('embedding', models.PositiveSmallIntegerField(help_text='PositiveSmallIntegerField: k-th embedding of O^D_h irrep.')),
                ('parity', models.SmallIntegerField(help_text='SmallIntegerField: Parity of hadronic operator')),
                ('spin_x2', models.PositiveSmallIntegerField(help_text='Text: Total spin times two')),
                ('spin_z_x2', models.SmallIntegerField(help_text='Text: Spin in z-direction')),
                ('isospin_x2', models.PositiveSmallIntegerField(help_text='Text: Total isospin times two')),
                ('isospin_z_x2', models.SmallIntegerField(help_text='Text: Isospin in z-direction times two')),
            ],
            bases=('wavefunction.scswavefunction',),
        ),
        migrations.AddConstraint(
            model_name='hadron4d',
            constraint=models.UniqueConstraint(fields=('strangeness', 'irrep', 'embedding', 'parity', 'spin_x2', 'spin_z_x2', 'isospin_x2', 'isospin_z_x2'), name='unique_hadron_hadron4d'),
        ),
        migrations.AddConstraint(
            model_name='hadron',
            constraint=models.UniqueConstraint(fields=('strangeness', 'irrep', 'embedding', 'parity', 'spin_x2', 'spin_z_x2', 'isospin_x2', 'isospin_z_x2', 'momentum'), name='unique_hadron_hadron'),
        ),
    ]
