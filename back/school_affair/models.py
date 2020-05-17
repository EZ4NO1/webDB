from django.db import models
from .field import YMField,BirthField
from .field import start_year
import datetime 
var_char_length=45

'''
class Test(models.Model):
    date=BirthField()
'''
class Major_transfer(models.Model):
    student_unnormal_change_id=models.OneToOneField('Student_unnormal_change',on_delete=models.CASCADE,primary_key=True)
    youth_league_changed=(
        ('yes','是'),
        ('no','不是'),
        ('not a','不是团员')
    )
class Student_unnormal_change(models.Model):
    id=models.AutoField(primary_key=True)
    data=YMField()
    class_before=models.ForeignKey('Class', on_delete=models.CASCADE,related_name='before')
    class_after=models.ForeignKey('Class', on_delete=models.CASCADE,related_name='after')
    change_type=(
        ('tranfer','转专业'),
        ('downward','降级')
        )
    student_id=models.ForeignKey("Student",on_delete=models.CASCADE)
class Grade_downward(models.Model):
    student_unnormal_change_id=models.OneToOneField('Student_unnormal_change',on_delete=models.CASCADE,primary_key=True)
    cause=models.TextChoices('休学','支教')
class Major(models.Model):
    id=models.CharField(max_length=var_char_length,primary_key=True)
    name=models.CharField(max_length=var_char_length)
    campus_id=models.ForeignKey('Campus', on_delete=models.CASCADE)
    person_in_charge=models.ForeignKey('Teacher', on_delete=models.CASCADE)
    address=models.CharField(max_length=var_char_length)
class Campus(models.Model):
    id=models.CharField(max_length=var_char_length,primary_key=True)
    name=models.CharField(max_length=var_char_length)
    address=models.CharField(max_length=var_char_length)
class Class(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=var_char_length)
    begin_time=YMField()
    major_id=models.ForeignKey('Major', on_delete=models.CASCADE)
    grade=models.IntegerField()
    header_teacher=models.ForeignKey("Teacher",on_delete=models.CASCADE)
class Student(models.Model):
    student_teacher_idnumber=models.OneToOneField("Student_teacher",on_delete=models.CASCADE,primary_key=True)
    class_id=models.ForeignKey("Class", on_delete=models.CASCADE)
class Course(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=var_char_length)
    examination=models.TextChoices('考试','当堂答辩')
    major_id=models.ForeignKey("Major",on_delete=models.CASCADE)
    teacher_id=models.ForeignKey("Teacher",on_delete=models.CASCADE)
    start_year=models.IntegerField()
    start_semester=models.TextChoices('春','秋')
    course_time=models.CharField(max_length=var_char_length)
    #constriant
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(start_year__gte=start_year), name='past')
        ]

class Teacher(models.Model):
    student_teacher_idnumber=models.OneToOneField("Student_teacher",on_delete=models.CASCADE,primary_key=True)
    major_id=models.ForeignKey("Major", on_delete=models.CASCADE)
    professional_title=models.TextChoices('教授','副教授')
class Course_sign_up(models.Model):
    course_id=models.ForeignKey("Course",on_delete=models.PROTECT)
    student_id=models.ForeignKey("Student",on_delete=models.CASCADE)
    score=models.IntegerField(null=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course_id','student_id'],name='no duplicated sign-up')
        ]
class Student_teacher(models.Model):
    id_number=models.IntegerField(primary_key=True)
    id_number_type=models.TextChoices('省份证','护照')
    name_chinese=models.CharField(max_length=var_char_length)
    gender=models.TextChoices('M','F')
    born_date=BirthField()
    nationality=models.CharField(max_length=var_char_length)
    email=models.EmailField(max_length=254)
    student_teacher_id=models.CharField(max_length=var_char_length,unique=True)
    student_or_teacher=models.TextChoices('教师','学生')
    entry_data=YMField()
    #constriant
class Home_information(models.Model):
    student_teacher_id_number=models.ForeignKey("Student_teacher",on_delete=models.CASCADE)
    home_address=models.CharField(max_length=var_char_length)
    post_code=models.CharField(max_length=var_char_length)
    home_telephone_number=models.CharField(max_length=var_char_length)
# Create your models here.