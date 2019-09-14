# Generated by Django 2.2.1 on 2019-09-14 01:33

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('correlator', '0001_initial'),
        ('project_fhcompare', '0003_auto_20190914_0115'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='jason0',
            name='unique_project_fhcompare_jason0',
        ),
        migrations.RemoveField(
            model_name='jason0',
            name='corrfhga',
        ),
        migrations.RemoveField(
            model_name='jason0',
            name='corrfhgv',
        ),
        migrations.RemoveField(
            model_name='jason0',
            name='corrseqga',
        ),
        migrations.RemoveField(
            model_name='jason0',
            name='corrseqgv',
        ),
        migrations.AddField(
            model_name='jason0',
            name='corrseq',
            field=models.ManyToManyField(to='correlator.Correlator'),
        ),
        migrations.AddField(
            model_name='jason0',
            name='listofcorrs',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), default=list, help_text='Text: A list of correlators used', size=None),
        ),
        migrations.AddConstraint(
            model_name='jason0',
            constraint=models.UniqueConstraint(fields=('hash_fit',), name='unique_project_fhcompare_jason0'),
        ),
    ]