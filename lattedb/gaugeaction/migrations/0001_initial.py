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
            name='GaugeAction',
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
            name='LuescherWeisz',
            fields=[
                ('gaugeaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='gaugeaction.GaugeAction')),
                ('beta', models.DecimalField(decimal_places=6, help_text='Decimal(10,6): Coupling constant', max_digits=10)),
                ('a_fm', models.DecimalField(decimal_places=6, help_text='(Optional) Decimal(10,6): Lattice spacing in fermi', max_digits=10, null=True)),
                ('u0', models.DecimalField(decimal_places=6, help_text='Decimal(10,6): Tadpole improvement coefficient', max_digits=10)),
            ],
            bases=('gaugeaction.gaugeaction',),
        ),
        migrations.AddConstraint(
            model_name='luescherweisz',
            constraint=models.UniqueConstraint(fields=('beta', 'u0'), name='unique_gaugeaction_luescherweisz'),
        ),
    ]
