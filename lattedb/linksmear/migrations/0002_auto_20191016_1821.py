# Generated by Django 2.2.2 on 2019-10-16 18:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('linksmear', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='linksmear',
            name='misc',
        ),
        migrations.AlterField(
            model_name='linksmear',
            name='id',
            field=models.AutoField(help_text='Primary key for Base class.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='linksmear',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, help_text='Date the class was last modified'),
        ),
        migrations.AlterField(
            model_name='linksmear',
            name='tag',
            field=models.CharField(blank=True, help_text='User defined tag for easy searches', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='linksmear',
            name='type',
            field=models.TextField(editable=False, help_text='Type for the base class. Will be auto set to specialized type on save'),
        ),
        migrations.AlterField(
            model_name='linksmear',
            name='user',
            field=models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Ananymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
