# Generated by Django 3.0.6 on 2020-05-16 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campus',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=45)),
                ('address', models.CharField(max_length=45)),
            ],
        ),
    ]
