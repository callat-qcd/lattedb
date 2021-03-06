# Generated by Django 3.0.6 on 2020-05-28 09:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project_formfac', '0008_auto_20200408_0823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concatenatedformfactor4dfile',
            name='user',
            field=models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Anonymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='correlatormeta',
            name='user',
            field=models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Anonymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='diskconcatenatedformfactor4dfile',
            name='user',
            field=models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Anonymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='diskcorrelatorh5dset',
            name='user',
            field=models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Anonymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='diskformfactor4dfile',
            name='user',
            field=models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Anonymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='diskspectrum4dfile',
            name='user',
            field=models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Anonymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='disktslicedformfactor4dfile',
            name='user',
            field=models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Anonymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='disktslicedsaveragedformfactor4dfile',
            name='user',
            field=models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Anonymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='disktslicedsaveragedspectrum4dfile',
            name='user',
            field=models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Anonymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='disktslicedspectrum4dfile',
            name='user',
            field=models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Anonymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='formfactor4dfile',
            name='user',
            field=models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Anonymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='spectrum4dfile',
            name='user',
            field=models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Anonymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tapeconcatenatedformfactor4dfile',
            name='user',
            field=models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Anonymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tapecorrelatorh5dset',
            name='user',
            field=models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Anonymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tapetslicedsaveragedformfactor4dfile',
            name='user',
            field=models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Anonymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tapetslicedsaveragedspectrum4dfile',
            name='user',
            field=models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Anonymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tslicedformfactor4dfile',
            name='user',
            field=models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Anonymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tslicedsaveragedformfactor4dfile',
            name='user',
            field=models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Anonymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tslicedsaveragedspectrum4dfile',
            name='user',
            field=models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Anonymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tslicedspectrum4dfile',
            name='user',
            field=models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Anonymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
