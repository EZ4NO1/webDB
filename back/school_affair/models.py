from django.db import models
from .field import YMField,BirthField
from .field import start_year,datatonum
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
import datetime 
from django.db.models import ProtectedError
from django.contrib.auth.models import AbstractUser 
class NotGraduateError(Exception):
    pass
var_char_length=45

'''
class Test(models.Model):
    date=BirthField()
'''
class MyQuerySet(models.query.QuerySet):

    def delete(self):
        pass  # you can throw an exception

class NoDeleteManager(models.Manager):
    def get_query_set(self):
        return MyQuerySet(self.model, using=self._db)

class Major_transfer(models.Model):
    student_unnormal_change_id=models.OneToOneField('Student_unnormal_change',on_delete=models.CASCADE,primary_key=True)
    youth_league_changed=models.CharField(max_length=5,choices=(
        ('yes','是'),
        ('no','不是'),
        ('not a','不是团员')
    )
    )
    def __str__(self):
        return str(self.student_unnormal_change_id.student_id)
class Student_unnormal_change(models.Model):
    id=models.AutoField(primary_key=True)
    data=YMField()
    class_before=models.ForeignKey('Class', on_delete=models.CASCADE,related_name='before')
    class_after=models.ForeignKey('Class', on_delete=models.CASCADE,related_name='after')
    change_type=models.CharField(max_length=10,choices=(
        ('tranfer','转专业'),
        ('downward','降级')
        )
    )
    student_id=models.ForeignKey("Student",on_delete=models.CASCADE)
    def __str__(self):
        return str(self.student_id)+'-'+self.change_type
class Grade_downward(models.Model):
    student_unnormal_change_id=models.OneToOneField('Student_unnormal_change',on_delete=models.CASCADE,primary_key=True)
    cause=models.CharField(max_length=10,choices=(('suspend','休学'),('teacher','支教')))
    def __str__(self):
        return str(self.student_unnormal_change_id.student_id)
class Major(models.Model):
    id=models.CharField(max_length=var_char_length,primary_key=True)
    name=models.CharField(max_length=var_char_length)
    campus_id=models.ForeignKey('Campus', on_delete=models.PROTECT)
    person_in_cahrge=models.ForeignKey('Teacher', on_delete=models.SET_NULL,null=True,blank=True)
    address=models.CharField(max_length=var_char_length)
    def __str__(self):
        return self.name
class Campus(models.Model):
    id=models.CharField(max_length=var_char_length,primary_key=True)
    name=models.CharField(max_length=var_char_length)
    address=models.CharField(max_length=var_char_length)
    def __str__(self):
        return self.name
class Class(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=var_char_length)
    begin_time=YMField()
    major_id=models.ForeignKey('Major', on_delete=models.CASCADE)
    grade=models.IntegerField()
    header_teacher=models.ForeignKey("Teacher",on_delete=models.CASCADE)
    def __str__(self):
        return str(self.major_id)+'-'+self.name
class Student(models.Model):
    student_teacher_idnumber=models.OneToOneField("Student_teacher",on_delete=models.PROTECT,primary_key=True)
    class_id=models.ForeignKey("Class", on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return self.student_teacher_idnumber.name_chinese
    def delete(self):
        t=datatonum(self.student_teacher_idnumber.entry_data)
        entry_m=t[0]*12+t[1]
        now_m=datetime.date.today().year*12+datetime.date.today().month
        if now_m-entry_m >=48:
            t=self.student_teacher_idnumber
            super().delete()
            t.delete()
        else :
            raise NotGraduateError('cannot delete student not graduated')
    objects = NoDeleteManager()

class Course(models.Model):
    id=models.CharField(max_length=var_char_length,primary_key=True)
    name=models.CharField(max_length=var_char_length)
    examination=models.CharField(max_length=10,choices=(('exam','考试'),('query','当堂答辩')))
    major_id=models.ForeignKey("Major",on_delete=models.CASCADE)
    teacher_id=models.ForeignKey("Teacher",on_delete=models.CASCADE)
    start_year=models.IntegerField()
    start_semester=models.CharField(max_length=10,choices=(('spring','春'),('fall','秋')))
    course_time=models.CharField(max_length=var_char_length)
    #constriant
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(start_year__gte=start_year), name='past')
        ]
    def __str__(self):
        return self.name+'-'+self.teacher_id.student_teacher_idnumber.name+'-'+str(self.start_year)+self.get_start_semester_display()
class Teacher(models.Model):
    student_teacher_idnumber=models.OneToOneField("Student_teacher",on_delete=models.PROTECT,primary_key=True)
    major_id=models.ForeignKey("Major", on_delete=models.PROTECT,null=True,blank=True)
    professional_title=models.CharField(max_length=20,choices=(('professor','教授'),('associate professor','副教授')),null=True,blank=True)
    def __str__(self):
        return self.student_teacher_idnumber.name_chinese
    def delete(self):
        t=self.student_teacher_idnumber
        super().delete()
        t.delete()
    objects = NoDeleteManager()

class Course_sign_up(models.Model):
    course_id=models.ForeignKey("Course",on_delete=models.PROTECT)
    student_id=models.ForeignKey("Student",on_delete=models.CASCADE)
    score=models.IntegerField(null=True,blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course_id','student_id'],name='no duplicated sign-up')
        ]
    def __str__(self):
        return self.student_id.name_chinese+'-'+self.course_id.name
class Student_teacher(models.Model):
    id_number=models.CharField(max_length=var_char_length,primary_key=True)
    id_number_type=models.CharField(max_length=20,choices=(('ID card','省份证'),('pass port','护照')))
    name_chinese=models.CharField(max_length=var_char_length)
    gender=models.CharField(max_length=20,choices=((('M','男'),('F','女'))))
    born_date=BirthField()
    nationality=models.CharField(max_length=var_char_length)
    email=models.EmailField(max_length=254)
    student_teacher_id=models.CharField(max_length=var_char_length,unique=True)
    student_or_teacher=models.CharField(max_length=10,choices=(
        ('student','学生'),
        ('teacher','教师')
    )
    )
    entry_data=YMField()
    def __str__(self):
        return self.get_student_or_teacher_display()+'-'+self.name_chinese
    objects = NoDeleteManager()
@receiver(post_save, sender=Student_teacher, dispatch_uid="create sub-entity")
def Create_CASCADE(sender, instance,created, **kwargs):
    if (created):
        if (instance.student_or_teacher=='student'):
            Student.objects.create(student_teacher_idnumber=instance)
        if (instance.student_or_teacher=='teacher'):
            Teacher.objects.create(student_teacher_idnumber=instance)

class Home_information(models.Model):
    student_teacher_id_number=models.ForeignKey("Student_teacher",on_delete=models.CASCADE)
    home_address=models.CharField(max_length=var_char_length)
    post_code=models.CharField(max_length=var_char_length)
    home_telephone_number=models.CharField(max_length=var_char_length)
    def __str__(self):
        return self.setudent_teacher_id_number.student_or_teacher+self.setudent_teacher_id_number.name_chinese+" 的家庭信息"

class school_user(AbstractUser):
    person=models.OneToOneField("Student_teacher",on_delete=models.CASCADE,null=True,blank=True,unique=True)

# Create your models here.