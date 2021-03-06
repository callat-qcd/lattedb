# Generated by Django 2.2.7 on 2019-11-19 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quarksmear', '0002_auto_20191107_0016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gaugecovariantgaussian',
            name='radius',
            field=models.DecimalField(decimal_places=6, help_text='Smearing radius in lattice units', max_digits=10),
        ),
        migrations.AlterField(
            model_name='gaugecovariantgaussian',
            name='step',
            field=models.PositiveSmallIntegerField(help_text='Number of smearing steps'),
        ),
        migrations.AlterField(
            model_name='quarksmear',
            name='description',
            field=models.TextField(blank=True, help_text='Description of the quark smearing operator', null=True),
        ),
    ]
