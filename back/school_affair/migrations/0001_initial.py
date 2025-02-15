# Generated by Django 3.0.6 on 2020-05-18 18:07

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import school_affair.field


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campus',
            fields=[
                ('id', models.CharField(max_length=45, primary_key=True, serialize=False, validators=[django.core.validators.MinLengthValidator(1)])),
                ('name', models.CharField(max_length=45, validators=[django.core.validators.MinLengthValidator(1)])),
                ('address', models.CharField(max_length=45, validators=[django.core.validators.MinLengthValidator(1)])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=45, validators=[django.core.validators.MinLengthValidator(1)])),
                ('begin_time', school_affair.field.YMField(max_length=7)),
                ('grade', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.CharField(max_length=45, primary_key=True, serialize=False, validators=[django.core.validators.MinLengthValidator(1)])),
                ('name', models.CharField(max_length=45, validators=[django.core.validators.MinLengthValidator(1)])),
                ('examination', models.CharField(choices=[('exam', '考试'), ('query', '当堂答辩')], max_length=10)),
                ('start_year', models.IntegerField()),
                ('start_semester', models.CharField(choices=[('spring', '春'), ('fall', '秋')], max_length=10)),
                ('course_time', models.CharField(max_length=45, validators=[django.core.validators.MinLengthValidator(1)])),
            ],
        ),
        migrations.CreateModel(
            name='Major',
            fields=[
                ('id', models.CharField(max_length=45, primary_key=True, serialize=False, validators=[django.core.validators.MinLengthValidator(1)])),
                ('name', models.CharField(max_length=45, validators=[django.core.validators.MinLengthValidator(1)])),
                ('address', models.CharField(max_length=45, validators=[django.core.validators.MinLengthValidator(1)])),
                ('campus_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='school_affair.Campus')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('class_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='school_affair.Class')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Student_teacher',
            fields=[
                ('id', models.CharField(max_length=45, primary_key=True, serialize=False, validators=[django.core.validators.MinLengthValidator(1)])),
                ('id_number', models.CharField(max_length=45, unique=True, validators=[django.core.validators.MinLengthValidator(1)])),
                ('id_number_type', models.CharField(choices=[('ID card', '省份证'), ('pass port', '护照')], max_length=20, validators=[django.core.validators.MinLengthValidator(1)])),
                ('name_chinese', models.CharField(max_length=45, validators=[django.core.validators.MinLengthValidator(1)])),
                ('gender', models.CharField(choices=[('M', '男'), ('F', '女')], max_length=20, validators=[django.core.validators.MinLengthValidator(1)])),
                ('born_date', school_affair.field.BirthField()),
                ('nationality', models.CharField(max_length=45, validators=[django.core.validators.MinLengthValidator(1)])),
                ('email', models.EmailField(max_length=254)),
                ('student_or_teacher', models.CharField(choices=[('student', '学生'), ('teacher', '教师')], max_length=10, validators=[django.core.validators.MinLengthValidator(1)])),
                ('entry_data', school_affair.field.YMField(max_length=7)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('professional_title', models.CharField(blank=True, choices=[('professor', '教授'), ('associate professor', '副教授')], max_length=20, null=True)),
                ('major_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='school_affair.Major')),
                ('sup', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='school_affair.Student_teacher')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Student_unnormal_change',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('data', school_affair.field.YMField(max_length=7)),
                ('change_type', models.CharField(choices=[('tranfer', '转专业'), ('downward', '降级')], max_length=10)),
                ('class_after', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='after', to='school_affair.Class')),
                ('class_before', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='before', to='school_affair.Class')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_affair.Student')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='student',
            name='sup',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='school_affair.Student_teacher'),
        ),
        migrations.CreateModel(
            name='Major_transfer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('youth_league_changed', models.CharField(choices=[('yes', '是'), ('no', '不是'), ('not a', '不是团员')], max_length=5)),
                ('sup', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='school_affair.Student_unnormal_change')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='major',
            name='person_in_cahrge',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school_affair.Teacher'),
        ),
        migrations.CreateModel(
            name='Home_information',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('home_address', models.CharField(max_length=45, validators=[django.core.validators.MinLengthValidator(1)])),
                ('post_code', models.CharField(max_length=45, validators=[django.core.validators.MinLengthValidator(1)])),
                ('home_telephone_number', models.CharField(max_length=45, validators=[django.core.validators.MinLengthValidator(1)])),
                ('sup', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='school_affair.Student_teacher')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Grade_downward',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cause', models.CharField(choices=[('suspend', '休学'), ('teacher', '支教')], max_length=10)),
                ('sup', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='school_affair.Student_unnormal_change')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Course_sign_up',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('score', models.IntegerField(blank=True, null=True)),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='school_affair.Course')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_affair.Student')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='major_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_affair.Major'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_affair.Teacher'),
        ),
        migrations.AddField(
            model_name='class',
            name='header_teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_affair.Teacher'),
        ),
        migrations.AddField(
            model_name='class',
            name='major_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_affair.Major'),
        ),
        migrations.CreateModel(
            name='school_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('person', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='school_affair.Student_teacher')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddConstraint(
            model_name='course_sign_up',
            constraint=models.UniqueConstraint(fields=('course_id', 'student_id'), name='no duplicated sign-up'),
        ),
        migrations.AddConstraint(
            model_name='course',
            constraint=models.CheckConstraint(check=models.Q(start_year__gte=1960), name='past'),
        ),
    ]
