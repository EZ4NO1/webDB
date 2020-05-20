from django.db import models
from .field import YMField,BirthField
from .field import start_year,datatonum
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
import datetime 
from django.db.models import ProtectedError
from django.contrib.auth.models import AbstractUser 
from django.core.validators import MinLengthValidator
from django.core.exceptions import  ValidationError
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

class clean_model(models.Model):
    def save(self,*args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    def sup_save(self,*args, **kwargs):
        super().save(*args, **kwargs)
    class Meta:
        abstract = True

class NoDeleteManager(models.Manager):
    def get_query_set(self):
        return MyQuerySet(self.model, using=self._db)

class Major_transfer(clean_model):
    id=models.AutoField(primary_key=True)
    sup=models.OneToOneField('Student_unnormal_change',on_delete=models.CASCADE)
    youth_league_changed=models.CharField(max_length=5,choices=(
        ('yes','是'),
        ('no','不是'),
        ('not a','不是团员')
    ),null=True,blank=True
    )
    def __str__(self):
        return str(self.sup.student_id)
    def delete(self):
        self.sup.delete()
    def clean(self):
        super().clean()
        if self.sup.change_type!='transfer':
            raise ValidationError('cannot change sub')
class Student_unnormal_change(clean_model):
    id=models.CharField(validators=[MinLengthValidator(1)],max_length=var_char_length,primary_key=True)
    data=YMField()
    class_before=models.ForeignKey('Class', on_delete=models.CASCADE,related_name='before')
    class_after=models.ForeignKey('Class', on_delete=models.CASCADE,related_name='after')
    change_type=models.CharField(max_length=10,choices=(
        ('transfer','转专业'),
        ('downward','降级')
        )
    )
    student_id=models.ForeignKey("Student",on_delete=models.CASCADE)
    def __str__(self):
        return str(self.student_id)+'-'+self.change_type

@receiver(post_save, sender=Student_unnormal_change, dispatch_uid="create unormal_change_sub-entity")
def Create_CASCADE_Unormal_Change(sender, instance,created, **kwargs):
    if (created):
        if (instance.change_type=='transfer'):
            Major_transfer.objects.create(sup=instance)
        if (instance.change_type=='downward'):
            Grade_downward.objects.create(sup=instance)

class Grade_downward(clean_model):
    id=models.AutoField(primary_key=True)
    sup=models.OneToOneField('Student_unnormal_change',on_delete=models.CASCADE)
    cause=models.CharField(max_length=10,choices=(('suspend','休学'),('teacher','支教')),null=True,blank=True)
    def __str__(self):
        return str(self.sup.student_id)
    def delete(self):
        self.sup.delete()
    def clean(self):
        super().clean()
        if self.sup.change_type!='downward':
            raise ValidationError('cannot change sub')




class Major(clean_model):
    id=models.CharField(validators=[MinLengthValidator(1)],max_length=var_char_length,primary_key=True)
    name=models.CharField(validators=[MinLengthValidator(1)],max_length=var_char_length)
    campus_id=models.ForeignKey('Campus', on_delete=models.PROTECT)
    person_in_charge_id=models.ForeignKey('Teacher', on_delete=models.SET_NULL,null=True,blank=True)
    address=models.CharField(validators=[MinLengthValidator(1)],max_length=var_char_length)
    def __str__(self):
        return self.name
class Campus(clean_model):
    id=models.CharField(validators=[MinLengthValidator(1)],max_length=var_char_length,primary_key=True)
    name=models.CharField(validators=[MinLengthValidator(1)],max_length=var_char_length)
    address=models.CharField(validators=[MinLengthValidator(1)],max_length=var_char_length)
    def __str__(self):
        return self.name
class Class(clean_model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(validators=[MinLengthValidator(1)],max_length=var_char_length)
    begin_time=YMField()
    major_id=models.ForeignKey('Major', on_delete=models.CASCADE)
    grade=models.IntegerField()
    header_teacher=models.ForeignKey("Teacher",on_delete=models.CASCADE)
    def __str__(self):
        return str(self.major_id)+'-'+self.name
class Student(clean_model):
    id=models.AutoField(primary_key=True)
    sup=models.OneToOneField("Student_teacher",on_delete=models.PROTECT)
    class_id=models.ForeignKey("Class", on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return self.sup.name_chinese
    def delete(self):
        t=datatonum(self.sup.entry_data)
        entry_m=t[0]*12+t[1]
        now_m=datetime.date.today().year*12+datetime.date.today().month
        if now_m-entry_m >=48:
            t=self.sup
            super().delete()
            t.delete()
        else :
            raise NotGraduateError('cannot delete student not graduated')
    objects = NoDeleteManager()
    def sup_delete(self):
        super().delete()
    def clean(self):
        super().clean()
        if self.sup.student_or_teacher!='student':
            raise ValidationError('cannot change sub')

class Course(clean_model):
    id=models.CharField(validators=[MinLengthValidator(1)],max_length=var_char_length,primary_key=True)
    name=models.CharField(validators=[MinLengthValidator(1)],max_length=var_char_length)
    examination=models.CharField(max_length=10,choices=(('exam','考试'),('query','当堂答辩')))
    major_id=models.ForeignKey("Major",on_delete=models.CASCADE)
    teacher_id=models.ForeignKey("Teacher",on_delete=models.CASCADE)
    start_year=models.IntegerField()
    start_semester=models.CharField(max_length=10,choices=(('spring','春'),('fall','秋')))
    course_time=models.CharField(validators=[MinLengthValidator(1)],max_length=var_char_length)
    #constriant
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(start_year__gte=start_year), name='past')
        ]
    def __str__(self):
        return self.name+'-'+self.teacher_id.sup.name_chinese+'-'+str(self.start_year)+self.get_start_semester_display()
class Teacher(clean_model):
    id=models.AutoField(primary_key=True)
    sup=models.OneToOneField("Student_teacher",on_delete=models.PROTECT)
    major_id=models.ForeignKey("Major", on_delete=models.PROTECT,null=True,blank=True)
    professional_title=models.CharField(max_length=20,choices=(('professor','教授'),('associate professor','副教授')),null=True,blank=True)
    def __str__(self):
        return self.sup.name_chinese
    def delete(self):
        t=self.sup
        super().delete()

        t.delete()
    objects = NoDeleteManager()
    def clean(self):
        super().clean()
        if self.sup.student_or_teacher!='teacher':
            raise ValidationError('cannot change sub')

class Course_sign_up(clean_model):
    id=models.AutoField(primary_key=True)
    course_id=models.ForeignKey("Course",on_delete=models.PROTECT)
    student_id=models.ForeignKey("Student",on_delete=models.CASCADE)
    score=models.IntegerField(null=True,blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course_id','student_id'],name='no duplicated sign-up')
        ]
    def __str__(self):
        return self.student_id.sup.name_chinese+'-'+self.course_id.name
class Student_teacher(clean_model):
    id=models.CharField(validators=[MinLengthValidator(1)],max_length=var_char_length,primary_key=True)
    id_number=models.CharField(validators=[MinLengthValidator(1)],max_length=var_char_length,unique=True)
    id_number_type=models.CharField(validators=[MinLengthValidator(1)],max_length=20,choices=(('ID card','省份证'),('pass port','护照')))
    name_chinese=models.CharField(validators=[MinLengthValidator(1)],max_length=var_char_length)
    gender=models.CharField(validators=[MinLengthValidator(1)],max_length=20,choices=((('M','男'),('F','女'))))
    born_date=BirthField()
    nationality=models.CharField(validators=[MinLengthValidator(1)],max_length=var_char_length)
    email=models.EmailField(max_length=254)
    student_or_teacher=models.CharField(validators=[MinLengthValidator(1)],max_length=10,choices=(
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
            Student.objects.create(sup=instance)
        if (instance.student_or_teacher=='teacher'):
            Teacher.objects.create(sup=instance)
        school_user.objects.create_user(instance.id,password=instance.id_number,person=instance)

class Home_information(clean_model):
    id=models.AutoField(primary_key=True)
    sup=models.OneToOneField("Student_teacher",on_delete=models.CASCADE)
    home_address=models.CharField(validators=[MinLengthValidator(1)],max_length=var_char_length,null=True,blank=True)
    post_code=models.CharField(validators=[MinLengthValidator(1)],max_length=var_char_length,null=True,blank=True)
    home_telephone_number=models.CharField(validators=[MinLengthValidator(1)],max_length=var_char_length,null=True,blank=True)
    def __str__(self):
        return self.setudent_teacher_id_number.student_or_teacher+self.setudent_teacher_id_number.name_chinese+" 的家庭信息"

class school_user(AbstractUser):
    person=models.OneToOneField("Student_teacher",on_delete=models.CASCADE,null=True,blank=True,unique=True)

# Create your models here.