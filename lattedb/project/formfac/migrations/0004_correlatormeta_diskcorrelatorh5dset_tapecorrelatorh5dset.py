# Generated by Django 2.2.7 on 2020-03-11 16:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project_formfac', '0003_diskspectrum4dfile_disktslicedsaveragedspectrum4dfile_disktslicedspectrum4dfile_spectrum4dfile_tapet'),
    ]

    operations = [
        migrations.CreateModel(
            name='CorrelatorMeta',
            fields=[
                ('id', models.AutoField(help_text='Primary key for Base class.', primary_key=True, serialize=False)),
                ('last_modified', models.DateTimeField(auto_now=True, help_text='Date the class was last modified')),
                ('tag', models.CharField(blank=True, help_text='User defined tag for easy searches', max_length=200, null=True)),
                ('type', models.CharField(choices=[('phi_qq', 'Connected pion-like meson'), ('mres', 'Residual quark mass'), ('spec', 'Pi+, proton, proton np'), ('ff', 'Form Factor of proton for MANY currents'), ('h_spec', 'Hyperon Spectrum')], help_text='Type of the correlator.', max_length=20)),
                ('configuration', models.IntegerField(help_text='Configuration number.')),
                ('source', models.CharField(help_text='Source location (e.g., `xXyYzZtT`).', max_length=20)),
                ('user', models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Ananymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('type', 'configuration', 'source')},
            },
        ),
        migrations.CreateModel(
            name='TapeCorrelatorH5Dset',
            fields=[
                ('id', models.AutoField(help_text='Primary key for Base class.', primary_key=True, serialize=False)),
                ('last_modified', models.DateTimeField(auto_now=True, help_text='Date the class was last modified')),
                ('tag', models.CharField(blank=True, help_text='User defined tag for easy searches', max_length=200, null=True)),
                ('name', models.TextField(help_text='The name of the file.')),
                ('path', models.TextField(help_text='The directory path of the file.')),
                ('dset', models.TextField(help_text='The path to the dset.')),
                ('exists', models.BooleanField(help_text='Can the file be found at `physical_file.path/physical_file.file.name/dset_path`?.')),
                ('machine', models.CharField(help_text='The machine the file can be found on.', max_length=100)),
                ('date_modified', models.DateTimeField(help_text='The last time the file was modified.', null=True)),
                ('meta', models.OneToOneField(help_text='The file meta information.', on_delete=django.db.models.deletion.CASCADE, related_name='tape', to='project_formfac.CorrelatorMeta')),
                ('user', models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Ananymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DiskCorrelatorH5Dset',
            fields=[
                ('id', models.AutoField(help_text='Primary key for Base class.', primary_key=True, serialize=False)),
                ('last_modified', models.DateTimeField(auto_now=True, help_text='Date the class was last modified')),
                ('tag', models.CharField(blank=True, help_text='User defined tag for easy searches', max_length=200, null=True)),
                ('name', models.TextField(help_text='The name of the file.')),
                ('path', models.TextField(help_text='The directory path of the file.')),
                ('dset', models.TextField(help_text='The path to the dset.')),
                ('exists', models.BooleanField(help_text='Can the file be found at `physical_file.path/physical_file.file.name/dset_path`?.')),
                ('machine', models.CharField(help_text='The machine the file can be found on.', max_length=100)),
                ('date_modified', models.DateTimeField(help_text='The last time the file was modified.', null=True)),
                ('meta', models.OneToOneField(help_text='The file meta information.', on_delete=django.db.models.deletion.CASCADE, related_name='disk', to='project_formfac.CorrelatorMeta')),
                ('user', models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Ananymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
