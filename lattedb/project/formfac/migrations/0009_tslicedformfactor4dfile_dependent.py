# Generated by Django 2.2.7 on 2019-11-11 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_formfac', '0008_formfactor4dfile_dependent'),
    ]

    operations = [
        migrations.AddField(
            model_name='tslicedformfactor4dfile',
            name='dependent',
            field=models.ForeignKey(help_text='Link to t-sliced source averaged form factor file.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dependencies', to='project_formfac.TSlicedSAveragedFormFactor4DFile'),
        ),
    ]