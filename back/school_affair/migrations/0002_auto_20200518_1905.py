# Generated by Django 3.0.6 on 2020-05-18 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_affair', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade_downward',
            name='cause',
            field=models.CharField(blank=True, choices=[('suspend', '休学'), ('teacher', '支教')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='major_transfer',
            name='youth_league_changed',
            field=models.CharField(blank=True, choices=[('yes', '是'), ('no', '不是'), ('not a', '不是团员')], max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='student_unnormal_change',
            name='change_type',
            field=models.CharField(choices=[('transfer', '转专业'), ('downward', '降级')], max_length=10),
        ),
    ]
