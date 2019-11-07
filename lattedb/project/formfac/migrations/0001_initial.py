# Generated by Django 2.2.6 on 2019-11-07 00:16

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
            name='FormFactor4DFile',
            fields=[
                ('id', models.AutoField(help_text='Primary key for Base class.', primary_key=True, serialize=False)),
                ('type', models.TextField(editable=False, help_text='Type for the base class. Will be auto set to specialized type on save')),
                ('last_modified', models.DateTimeField(auto_now=True, help_text='Date the class was last modified')),
                ('tag', models.CharField(blank=True, help_text='User defined tag for easy searches', max_length=200, null=True)),
                ('name', models.TextField(help_text='Name of the file. Should not include folders.', unique=True)),
                ('ensemble', models.CharField(help_text='Name of the ensemble. E.g., `a15m135XL`.', max_length=100)),
                ('stream', models.CharField(help_text='Name of the HMC stream, e.g., `a`.', max_length=10)),
                ('configuration_range', models.CharField(help_text='Range of configuration in this file. E.g., `500-1745`.', max_length=100)),
                ('source_set', models.CharField(help_text='Set of sources in this file. E.g., `16-23`.', max_length=100)),
                ('current', models.CharField(help_text='Name of the current. E.g., `V2`.', max_length=20)),
                ('state', models.CharField(help_text='Name of the state. E.g., `proton`.', max_length=100)),
                ('parity', models.IntegerField(help_text='Parity of the state. E.g., + or -1.')),
                ('flavor', models.CharField(help_text='Flavor of the state. E.g., `UU`.', max_length=20)),
                ('spin', models.CharField(help_text='Spin of the state. E.g., `up_up`.', max_length=20)),
                ('user', models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Ananymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('ensemble', 'stream', 'configuration_range', 'source_set', 'current', 'state', 'parity', 'flavor', 'spin')},
            },
        ),
        migrations.CreateModel(
            name='TapeFormFactor4DFile',
            fields=[
                ('id', models.AutoField(help_text='Primary key for Base class.', primary_key=True, serialize=False)),
                ('type', models.TextField(editable=False, help_text='Type for the base class. Will be auto set to specialized type on save')),
                ('last_modified', models.DateTimeField(auto_now=True, help_text='Date the class was last modified')),
                ('tag', models.CharField(blank=True, help_text='User defined tag for easy searches', max_length=200, null=True)),
                ('path', models.TextField(help_text='The directory path on tape.')),
                ('exists', models.BooleanField(help_text='Can the file be found `tape_file.path/tape_file.file.name`?.')),
                ('machine', models.CharField(help_text='The machine the file can be found on.', max_length=100)),
                ('size', models.IntegerField(help_text='Size of the file in Bytes.', null=True)),
                ('date_modified', models.DateTimeField(help_text='The last time the file was modified.', null=True)),
                ('file', models.ForeignKey(help_text='The file meta information.', on_delete=django.db.models.deletion.CASCADE, related_name='tape', to='project_formfac.FormFactor4DFile')),
                ('user', models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Ananymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DiskFormFactor4DFile',
            fields=[
                ('id', models.AutoField(help_text='Primary key for Base class.', primary_key=True, serialize=False)),
                ('type', models.TextField(editable=False, help_text='Type for the base class. Will be auto set to specialized type on save')),
                ('last_modified', models.DateTimeField(auto_now=True, help_text='Date the class was last modified')),
                ('tag', models.CharField(blank=True, help_text='User defined tag for easy searches', max_length=200, null=True)),
                ('path', models.TextField(help_text='The directory path on disk.')),
                ('exists', models.BooleanField(help_text='Can the file be found `disk_file.path/disk_file.file.name`?.')),
                ('machine', models.CharField(help_text='The machine the file can be found on.', max_length=100)),
                ('size', models.IntegerField(help_text='Size of the file in Bytes.', null=True)),
                ('date_modified', models.DateTimeField(help_text='The last time the file was modified.', null=True)),
                ('file', models.ForeignKey(help_text='The file meta information.', on_delete=django.db.models.deletion.CASCADE, related_name='disk', to='project_formfac.FormFactor4DFile')),
                ('user', models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Ananymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]