# Generated by Django 3.0.6 on 2020-05-16 09:46

from django.db import migrations
import school_affair.field


class Migration(migrations.Migration):

    dependencies = [
        ('school_affair', '0003_auto_20200516_0821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_unnormal_change',
            name='data',
            field=school_affair.field.YMField(max_length=7),
        ),
    ]
