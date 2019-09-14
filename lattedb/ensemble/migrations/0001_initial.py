# Generated by Django 2.2.2 on 2019-09-13 23:53

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gaugeconfig', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ensemble',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.TextField(editable=False)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('tag', models.CharField(blank=True, help_text='(Optional) Char(20): User defined tag for easy searches', max_length=20, null=True)),
                ('misc', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text="(Optional) JSON: {'anything': 'you want'}", null=True)),
                ('label', models.CharField(help_text='(Optional) Char(20): label to identify ensemble for easy searches', max_length=40, unique=True)),
                ('configurations', models.ManyToManyField(to='gaugeconfig.GaugeConfig')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]