# Generated by Django 2.2.2 on 2019-10-16 18:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_fhcompare', '0004_auto_20190914_0133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fhcompare',
            name='misc',
        ),
        migrations.RemoveField(
            model_name='sourceavg2pt',
            name='misc',
        ),
        migrations.AlterField(
            model_name='fhcompare',
            name='id',
            field=models.AutoField(help_text='Primary key for Base class.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='fhcompare',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, help_text='Date the class was last modified'),
        ),
        migrations.AlterField(
            model_name='fhcompare',
            name='tag',
            field=models.CharField(blank=True, help_text='User defined tag for easy searches', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='fhcompare',
            name='type',
            field=models.TextField(editable=False, help_text='Type for the base class. Will be auto set to specialized type on save'),
        ),
        migrations.AlterField(
            model_name='fhcompare',
            name='user',
            field=models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Ananymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sourceavg2pt',
            name='id',
            field=models.AutoField(help_text='Primary key for Base class.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='sourceavg2pt',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, help_text='Date the class was last modified'),
        ),
        migrations.AlterField(
            model_name='sourceavg2pt',
            name='tag',
            field=models.CharField(blank=True, help_text='User defined tag for easy searches', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='sourceavg2pt',
            name='type',
            field=models.TextField(editable=False, help_text='Type for the base class. Will be auto set to specialized type on save'),
        ),
        migrations.AlterField(
            model_name='sourceavg2pt',
            name='user',
            field=models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Ananymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
