from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate  
from django.contrib.auth import login as django_login,logout
from django.shortcuts import redirect
from . import models
import json
from django.http import JsonResponse
import datetime
from django.db import models as d_model
from django.db.models import ForeignKey,OneToOneField,IntegerField,AutoField
from json import JSONDecodeError
from .field import YMField,BirthField

NotExistJson=JsonResponse({'message': '数据不存在！','code':'fail'})
NoMethodJson=JsonResponse({'message': 'No  valid Method','code':'fail'})
NotJson=JsonResponse({'message': 'No  Json Format','code':'fail'})
InsertExsitJson=JsonResponse({'message': 'same id exist','code':'fail'})
IdLostJson=JsonResponse({'message': 'must contian id','code':'fail'})


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
@require_POST
def login(request):
    username = request.POST.get('username')
    #print(username)
    password = request.POST.get('password')
    #print(password)
    user = authenticate(username=username, password=password)
    
    if user is not None:
        django_login(request,user)
        #print(user.person)
        if  user.person: 
            return HttpResponse("welcome"+str(user.person))
        else :
            return HttpResponse("welcome Manager")
    else:
        return HttpResponse("login fail")

def logout(request):
        logout(request)
        return HttpResponse("Logout success")



def role_confirm(request,role):
    aul=False
    if  not request.user.is_authenticated:
        return JsonResponse({'message':'未登录用户','code':'fail'})
    if request.user.person is  None and role=='manager':
        aul=True
    if request.user.person:
        if  user.person.teacher_or_student==role:
            aul=True 
    if not aul:
        return JsonResponse({'message':'你不是'+role,'code':'fail'})
    
def try_to_save(model):
    try:
         model.save()
    except Exception as e:
        return JsonResponse({'message':str(e),'code':'fail'})
    return JsonResponse({'message': 'OK','code':'success'})
    
def try_to_delete(model):
    try:
         model.delete()
    except Exception as e:
        return JsonResponse({'message':e.message,'code':'fail'})
    return JsonResponse({'message': 'OK','code':'success'})
def model_to_dict(model):
    data={}
    for f in model._meta.fields:
        if f.choices:
            cdict={key:value   for key,value in f.choices}
            data[f.name]=cdict[getattr(model, f.name)]
        else:
            data[f.name]=str(getattr(model, f.name))
    return data
def queryset_to_json (queryset):
        obj_arr=[]
        for o in queryset:
                obj_arr.append(model_to_dict(o))
        return JsonResponse({'message': 'OK','code':'success','data':obj_arr})

def singlemodel(request,model_class,readonlylist=[]):
    readonlylist=readonlylist+['id']
    try:
        data=json.loads(request.body)
    except JSONDecodeError:
        return NotJson
    method = data.get('method')
    if not method:
        return NoMethodJson
    data.pop('method')
    if (method == 'INSERT' or method == 'DELETE' or method == "EDIT") and data.get('id') is None:
        return IdLostJson
    if method == 'INSERT':
        if model_class.objects.filter(id=data.get('id')).first() is not None:
            return InsertExsitJson
        model = model_class()
        for f in model._meta.fields:
            tep=data.get(f.name)
            if (tep):
                if isinstance(f,ForeignKey) or isinstance(f,OneToOneField):
                    tep=f.related_model.objects.filter(id=tep).first()
                setattr(model,f.name,tep)
        return try_to_save(model)
    elif method == 'DELETE':
        data_id= data.get('id')
        line = model_class.objects.filter(id=data_id)
        if not line:
            return NotExistJson
        else:
            return try_to_delete(line)
    elif method == 'FORMAT':
        dic={'message': 'OK','code':'success'}
        forma=[]
        for f in model_class._meta.fields:
            one_field={}
            one_field['name']=f.name
            if isinstance(f,ForeignKey) or isinstance(f,OneToOneField):
                one_field['type']='link'
                one_field['alter']={line.id:str(line)   for line in f.related_model.objects.all()}
            elif isinstance(f,IntegerField):
                one_field['type']='int'
            elif f.choices:
                one_field['type']='choice'
                one_field['alter']={key:value   for key,value in f.choices}
            elif isinstance(f,AutoField):
                one_field['type']='auto'
            elif isinstance(f,YMField):
                one_field['type']='YMdate'
            else :
                one_field['type']='text'
            if f.name in readonlylist:
                one_field['read_only']='true'
            else :
                one_field['read_only']='false'
            forma.append(one_field)
        print(forma)
        dic['format']=forma
        return JsonResponse(dic)
    elif method == 'ALL':
        lines = model_class.objects.all()
        if not lines:
            return NotExistJson
        else:
            return queryset_to_json(lines)
    elif method == "EDIT":
        model_id = data.get('id')
        line = model_class.objects.filter(id=model_id).first()
        if not line:
            return NotExistJson
        else:
            for f in model_class._meta.fields:
                if f in readonlylist:
                    continue
                tep=data.get(f.name)
                if (tep):
                    if isinstance(f,AutoField):
                        continue
                    if isinstance(f,ForeignKey) or isinstance(f,OneToOneField):
                        tep=f.related_model.objects.filter(id=tep).first()
                    setattr(line,f.name,tep)
            return try_to_save(line)
    return NoMethodJson

@require_POST
def campus(request):
    aul=role_confirm(request,'manager')
    if aul:    
        return aul
    return singlemodel(request,models.Campus)

@require_POST
def major(request):
    aul=role_confirm(request,'manager')
    if aul:    
        return aul
    return singlemodel(request,models.Major)

@require_POST
def class_info(request):
    aul=role_confirm(request,'manager')
    if aul:    
        return aul
    return singlemodel(request,models.Class)

@require_POST
def student_info(request):
    aul=role_confirm(request,'manager')
    if aul:    
        return aul
    return singlemodel(request,models.Class)


def teacher_info(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        method = json_data['method']
        if method == 'INSERT':
            data = models.Student_teacher()
            data_teacher = models.Teacher()
            data_home = models.Home_information()
            data.id_number = json_data['student_teacher_idnumber']
            data.id_number_type = json_data['id_number_type']
            data.name_chinese = json_data['name_chinese']
            data.gender = json_data['gender']
            data.born_date = json_data['born_date']
            data.nationality = json_data['nationality']
            data.email = json_data['email']
            data.student_teacher_id = json_data['student_teacher_idnumber']
            data.student_or_teacher = '教师'
            data.entry_data = json_data['entry_data']
            data_home.student_teacher_id_number = json_data['student_teacher_idnumber']
            data_home.home_address = json_data['home_address']
            data_home.post_code = json_data['post_code']
            data_home.home_telephone_number = json_data['home_telephone_number']
            data_teacher.student_teacher_idnumber = json_data['student_teacher_idnumber']
            data_teacher.major_id = json_data['major_id']
            data_teacher.professional_title = json_data['professional_title']
            if not data.id_number:
                return JsonResponse({'message': '主键不能为空！'})
            else:
                data.save()
                data_home.save()
                data_teacher.save()
                return JsonResponse({'message': 'OK'})
        elif method == 'DELETE':
            id_number = json_data['student_teacher_idnumber']
            data = models.Student_teacher.objects.filter(id_number=id_number, student_or_teacher='教师')
            data_home = models.Home_information.objects.filter(student_teacher_id_number=id_number)
            data_teacher = models.Teacher.objects.filter(student_teacher_idnumber=id_number)
            if not data:
                return JsonResponse({'message': '数据不存在！'})
            else:
                refer_data = models.Class.objects.filter(header_teacher=id_number)
                if refer_data:
                    return JsonResponse({'message': '存在关联信息：班级'})
                else:
                    data.delete()
                    if data_home:
                        data_home.delete()
                    if data_teacher:
                        data_teacher.delete()
                    return JsonResponse({'message': 'OK'})
        elif method == 'QUERY':
            id_number = json_data['id_number']
            data = models.Student_teacher.objects.filter(id=id_number, student_or_teacher='教师')
            data_home = models.Home_information.objects.filter(student_teacher_id_number=id_number)
            data_teacher = models.Teacher.objects.filter(student_teacher_idnumber=id_number)
            if not data:
                return JsonResponse({'message': '数据不存在！'})
            elif data_home:
                return JsonResponse({'message': 'OK',
                                     'student_teacher_idnumber': data['id_number'],
                                     'id_number_type': data['id_number_type'],
                                     'name_chinese': data['name_chinese'],
                                     'gender': data['gender'],
                                     'born_date': data['born_date'],
                                     'nationality': data['nationality'],
                                     'email': data['email'],
                                     'student_teacher_id': data['student_teacher_id'],
                                     'student_or_teacher': '教师',
                                     'entry_data': data['entry_data'],
                                     'home_address': data_home['home_address'],
                                     'post_code': data_home['post_code'],
                                     'home_telephone_number': data_home['home_telephone_number'],
                                     'major_id': data_teacher['major_id'],
                                     'professional_title': data_teacher['professional_title']})
            else:
                return JsonResponse({'message': 'OK',
                                     'student_teacher_idnumber': data['id_number'],
                                     'id_number_type': data['id_number_type'],
                                     'name_chinese': data['name_chinese'],
                                     'gender': data['gender'],
                                     'born_date': data['born_date'],
                                     'nationality': data['nationality'],
                                     'email': data['email'],
                                     'student_teacher_id': data['student_teacher_id'],
                                     'student_or_teacher': '教师',
                                     'entry_data': data['entry_data'],
                                     'major_id': data_teacher['major_id'],
                                     'professional_title': data_teacher['professional_title']})
        elif method == "EDIT":
            id_number = json_data['id_number']
            data = models.Student_teacher.objects.filter(id=id_number, student_or_teacher='教师')
            data_home = models.Home_information.objects.filter(student_teacher_id_number=id_number)
            data_teacher = models.Teacher.objects.filter(student_teacher_idnumber=id_number)
            if not data:
                return JsonResponse({'message': '数据不存在！'})
            else:
                data.id_number_type = json_data['id_number_type']
                data.name_chinese = json_data['name_chinese']
                data.gender = json_data['gender']
                data.born_date = json_data['born_date']
                data.nationality = json_data['nationality']
                data.email = json_data['email']
                data.student_teacher_id = json_data['student_teacher_id']
                data.entry_data = json_data['entry_data']
                data.save()
                data_home.student_teacher_id_number = json_data['student_teacher_idnumber']
                data_home.home_address = json_data['home_address']
                data_home.post_code = json_data['post_code']
                data_home.home_telephone_number = json_data['home_telephone_number']
                data_home.save()
                data_teacher.student_teacher_idnumber = json_data['student_teacher_idnumber']
                data_teacher.major_id = json_data['major_id']
                data_teacher.professional_title = json_data['professional_title']
                data_teacher.save()
                return JsonResponse({'message': 'OK'})


def student_unnormal_change(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        method = json_data['method']
        if method == 'INSERT':
            data = models.Student_unnormal_change()
            data.id = json_data['student_unnormal_change_id']
            data.data = json_data['student_unnormal_change_data']
            data.class_before = json_data['student_unnormal_change_class_before']
            data.class_after = json_data['student_unnormal_change_class_after']
            data.change_type = json_data['student_unnormal_change_type']
            if not data.id:
                return JsonResponse({'message': '主键不能为空！'})
            else:
                data.save()
                return JsonResponse({'message': 'OK'})
        elif method == 'DELETE':
            student_unnormal_change_id = json_data['student_unnormal_change_id']
            data = models.Student_unnormal_change.objects.filter(id=student_unnormal_change_id)
            if not data:
                return JsonResponse({'message': '数据不存在！'})
            else:
                data.delete()
                return JsonResponse({'message': 'OK'})
        elif method == 'QUERY':
            student_unnormal_change_id = json_data['student_unnormal_change_id']
            data = models.Student_unnormal_change.objects.filter(id=student_unnormal_change_id)
            if not data:
                return JsonResponse({'message': '数据不存在！'})
            else:
                return JsonResponse({'message': 'OK',
                                     'student_unnormal_change_id': student_unnormal_change_id,
                                     'student_unnormal_change_data': data['data'],
                                     'student_unnormal_change_class_before': data['class_before'],
                                     'student_unnormal_change_class_after': data['class_after'],
                                     'student_unnormal_change_type': data['change_type']})
        elif method == "EDIT":
            student_unnormal_change_id = json_data['student_unnormal_change_id']
            data = models.Student_unnormal_change.objects.filter(id=student_unnormal_change_id)
            if not data:
                return JsonResponse({'message': '数据不存在！'})
            else:
                data.data = json_data['student_unnormal_change_data']
                data.class_before = json_data['student_unnormal_change_class_before']
                data.class_after = json_data['student_unnormal_change_class_after']
                data.change_type = json_data['student_unnormal_change_type']
                data.save()
                return JsonResponse({'message': 'OK'})


def course(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        method = json_data['method']
        if method == 'INSERT':
            data = models.Course()
            data.id = json_data['course_id']
            data.name = json_data['course_name']
            data.examination = json_data['course_examination']
            data.major_id = json_data['major_id']
            data.teacher_id = json_data['student_teacher_idnumber']
            data.start_year = json_data['course_start_year']
            data.start_semester = json_data['course_start_semester']
            data.course_time = json_data['course_time']
            if not data.id:
                return JsonResponse({'message': '主键不能为空！'})
            else:
                data.save()
                return JsonResponse({'message': 'OK'})
        elif method == 'DELETE':
            course_id = json_data['course_id']
            data = models.Course.objects.filter(id=course_id)
            if not data:
                return JsonResponse({'message': '数据不存在！'})
            else:
                refer_data = models.Course_sign_up.objects.filter(course_id=course_id)
                if refer_data:
                    return JsonResponse({'message': '存在关联信息：开课'})
                else:
                    data.delete()
                    return JsonResponse({'message': 'OK'})
        elif method == 'QUERY':
            course_id = json_data['course_id']
            data = models.Course.objects.filter(id=course_id)
            if not data:
                return JsonResponse({'message': '数据不存在！'})
            else:
                return JsonResponse({'message': 'OK',
                                     'course_id': course_id,
                                     'course_name': data['name'],
                                     'course_examination': data['examination'],
                                     'major_id': data['major_id'],
                                     'student_teacher_idnumber': data['teacher_id'],
                                     'course_start_year': data['start_year'],
                                     'course_start_semester': data['start_semester'],
                                     'course_time': data['course_time']})
        elif method == "EDIT":
            course_id = json_data['course_id']
            data = models.Course.objects.filter(id=course_id)
            if not data:
                return JsonResponse({'message': '数据不存在！'})
            else:
                data.name = json_data['course_name']
                data.examination = json_data['course_examination']
                data.major_id = json_data['major_id']
                data.teacher_id = json_data['student_teacher_idnumber']
                data.start_year = json_data['course_start_year']
                data.start_semester = json_data['course_start_semester']
                data.course_time = json_data['course_time']
                data.save()
                return JsonResponse({'message': 'OK'})


def course_sign_up(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        method = json_data['method']
        if method == 'INSERT':
            data = models.Course_sign_up()
            data.course_id = json_data['course_id']
            data.student_id = json_data['student_teacher_idnumber']
            data.score = json_data['course_sign_up_score']
            if not data.course_id:
                return JsonResponse({'message': '主键不能为空！'})
            elif not data.student_id:
                return JsonResponse({'message': '主键不能为空！'})
            else:
                data.save()
                return JsonResponse({'message': 'OK'})
        elif method == 'DELETE':
            course_id = json_data['course_id']
            student_id = json_data['student_teacher_idnumber']
            data = models.Course_sign_up.objects.filter(course_id=course_id, student_id=student_id)
            if not data:
                return JsonResponse({'message': '数据不存在！'})
            else:
                data.delete()
                return JsonResponse({'message': 'OK'})
        elif method == 'QUERY':
            course_id = json_data['course_id']
            student_id = json_data['student_teacher_idnumber']
            data = models.Course_sign_up.objects.filter(course_id=course_id, student_id=student_id)
            if not data:
                return JsonResponse({'message': '数据不存在！'})
            else:
                return JsonResponse({'message': 'OK',
                                     'course_id': course_id,
                                     'student_teacher_idnumber': data['student_id'],
                                     'student_sign_up_score': data['score']})
        elif method == "EDIT":
            course_id = json_data['course_id']
            student_id = json_data['student_teacher_idnumber']
            data = models.Course_sign_up.objects.filter(course_id=course_id, student_id=student_id)
            if not data:
                return JsonResponse({'message': '数据不存在！'})
            else:
                data.score = json_data['student_sign_up_score']
                data.save()
                return JsonResponse({'message': 'OK'})




