# Generated by Django 3.0.6 on 2020-05-20 22:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school_affair', '0004_auto_20200519_2303'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='major',
            name='person_in_charge',
        ),
        migrations.AddField(
            model_name='major',
            name='person_in_charge_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school_affair.Teacher'),
        ),
    ]
