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
from copy import deepcopy






NotExistJson=JsonResponse({'message': '数据不存在！','code':'fail'})
NoMethodJson=JsonResponse({'message': 'No  valid Method','code':'fail'})
NotJson=JsonResponse({'message': 'No  Json Format','code':'fail'})
InsertExsitJson=JsonResponse({'message': 'same id exist','code':'fail'})
IdLostJson=JsonResponse({'message': 'must contian id','code':'fail'})
OKJson=JsonResponse({'message': 'OK','code':'success'})

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
@require_POST
def login(request):
    username = request.POST.get('username')
    print(username)
    password = request.POST.get('password')
    print(password)
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
        if  request.user.person.student_or_teacher==role:
            aul=True 
    if not aul:
        return JsonResponse({'message':'你不是'+role,'code':'fail'})
    
def try_to_save(model):
    try:
        model.save()
    except Exception as e:
        return exception2Json(e)
    return JsonResponse({'message': 'OK','code':'success'})



def try_to_delete(model):
    try:
         model.delete()
    except Exception as e:
        return exception2Json(e)
    return JsonResponse({'message': 'OK','code':'success'})
def model_to_dict(model,fields=None):
    data={}
    if  fields:
        tep=fields
    else:
        tep=model._meta.fields
    for f in tep:
        
        if f.choices and getattr(model, f.name):
            cdict={key:value   for key,value in f.choices}
            #print(cdict)
            data[f.name]=cdict[getattr(model, f.name)]
        else:
            data[f.name]=str(getattr(model, f.name))
    return data
def queryset_to_json (queryset):
        obj_arr=[]
        for o in queryset:
                obj_arr.append(model_to_dict(o))
        return JsonResponse({'message': 'OK','code':'success','data':obj_arr})

def format_one_field(f,readonlylist):
    one_field={}
    one_field['name']=f.name
    if f.name in readonlylist:
        one_field['read_only']='true'
    else :
        one_field['read_only']='false'
    if isinstance(f,ForeignKey) or isinstance(f,OneToOneField):
        one_field['type']='link'
        one_field['alter']={line.id:str(line)   for line in f.related_model.objects.all()}
    elif isinstance(f,AutoField):
        one_field['type']='auto'
    elif isinstance(f,IntegerField):
        one_field['type']='int'
    elif f.choices:
        one_field['type']='choice'
        one_field['alter']={key:value   for key,value in f.choices}
    elif isinstance(f,YMField):
        one_field['type']='YMdate'
    else :
        one_field['type']='text'
    return one_field
def singlemodel(request,model_class,readonlylist=[],plus={}):
    readonlylist=readonlylist+['id']
    try:
        data=json.loads(request.body)
    except JSONDecodeError:
        return NotJson
    data.update(plus)
    method = data.get('method')
    if not method:
        return NoMethodJson
    data.pop('method')
    if ( method == 'DELETE' or method == "EDIT") and data.get('id') is None :
        return IdLostJson
    if method == 'INSERT':
        if model_class.objects.filter(id=data.get('id')).first() is not None:
            return InsertExsitJson
        model = model_class()
        print(data)
        for f in model._meta.fields:
            tep=data.get(f.name)
            print(tep)
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
            forma.append(format_one_field(f,readonlylist))
        #print(forma)
        dic['format']=forma
        return JsonResponse(dic)
    elif method == 'ALL':
        lines = model_class.objects.all()
        return queryset_to_json(lines)
    elif method == "EDIT":
        model_id = data.get('id')
        line = model_class.objects.filter(id=model_id).first()
        if not line:
            return NotExistJson
        else:
            for f in model_class._meta.fields:
                if f.name!='id':
                    tep=data.get(f.name)
                    if (tep):
                        if f.name in readonlylist:
                            return JsonResponse({'message':f.name+"  read ONLY",'code':'fail'})
                        if isinstance(f,AutoField):
                            continue
                        if isinstance(f,ForeignKey) or isinstance(f,OneToOneField):
                            tep=f.related_model.objects.filter(id=tep).first()
                        setattr(line,f.name,tep)
            print(line)
            return try_to_save(line)
    return NoMethodJson
def gen_model(m,field_list,data): 
    model=m()
    return change_model(model,field_list,data)
def change_model(m,field_list,data,ban_list=[]):
    flag=False 
    for f in field_list:
            if f in ban_list:
                continue
            tep=data.get(f.name)
            if (tep):
                if isinstance(f,ForeignKey) or isinstance(f,OneToOneField):
                    tep=f.related_model.objects.filter(id=tep).first()
                setattr(m,f.name,tep)
                flag=True
    if not flag:
        return None
    return m
def exception2Json(e):
    if hasattr(e,"error_dict"):
        t=getattr(e,"error_dict")
        for i in t.keys():
            t[i]=str(t[i][0])
        return JsonResponse({'message':t,'code':'fail'})
    return JsonResponse({'message':str(e),'code':'fail'})

def change_model_save(m,field_list,data,ban_list=[]):
    tep=change_model(m,field_list,data,ban_list)
    if tep:
        tep.save()

def T_S(request,role,readonlylist=[]):
    entity=None
    if role=="student":
        entity=models.Student
    elif role=="teacher":
        entity=models.Teacher
    banlist=['id','sup']
    supclass=models.Student_teacher
    addtionclass=models.Home_information
    entity_field=[r for r in entity._meta.fields if not r.name in banlist]
    supclass_field=[r for r in supclass._meta.fields if not r.name in ['student_or_teacher']]
    addtionclass_field=[r for r in addtionclass._meta.fields if not r.name in banlist]
    readonlylist=readonlylist+['id','sup','student_or_teacher']
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
        if supclass.objects.filter(id=data.get('id')).first() is not None:
            return InsertExsitJson
        sup_m=gen_model(supclass,supclass_field,data)
        sup_m.student_or_teacher=role
        try:
            sup_m.save()
        except  Exception as e:
            return exception2Json(e)
        entity_m=entity.objects.filter(sup=sup_m).first()
       
        entity_m=change_model(entity_m,entity_field,data)
        print(entity_m)
        add_m=gen_model(addtionclass,addtionclass_field,data)
        if (add_m):
            add_m.sup=sup_m
        try:
            if entity_m:
                entity_m.save()
            if add_m:
                add_m.save()
        except Exception as e:
            entity.objects.filter(sup=sup_m).first().delete()
            return exception2Json(e)
        return JsonResponse({'message': 'OK','code':'success'})
    elif method == 'DELETE':
        data_id= data.get('id')
        sup_m=supclass.objects.filter(id=data_id).first()
        line = entity.objects.filter(sup=sup_m).first()
        if not line:
            return NotExistJson
        else:
            return try_to_delete(line)
    elif method == 'FORMAT':
        dic={'message': 'OK','code':'success'}
        forma=[]
        for f in supclass_field:
            forma.append(format_one_field(f,readonlylist))
        for f in entity_field:
            forma.append(format_one_field(f,readonlylist))
        for f in addtionclass_field:
            forma.append(format_one_field(f,readonlylist))
        #print(forma)
        dic['format']=forma
        return JsonResponse(dic)
    elif method == 'ALL':
        lines = entity.objects.all()
        dic={'message': 'OK','code':'success'}
        all_data=[]
        for i in lines:
            tep=model_to_dict(i.sup,supclass_field)
            tep.update(model_to_dict(i,entity_field))
            add_m=addtionclass.objects.filter(sup=i.sup).first()
            if add_m:
                tep.update(model_to_dict(add_m,addtionclass_field))
            all_data.append(tep)
        #print(all_data)
        dic['data']=all_data
        #print(dic)
        return JsonResponse(dic)
    elif method == "EDIT":
        recover=[]
        sup_m=supclass.objects.filter(id=data.get('id')).first() 
        if sup_m is None:
            return NotExistJson
        recover.append(deepcopy(sup_m))
        try:
            change_model_save(sup_m,supclass_field,data,readonlylist)
        except  Exception as e:
            return exception2Json(e)
        recover.append(deepcopy(entity.objects.filter(sup=sup_m).first()))
        try:
            change_model_save(entity.objects.filter(sup=sup_m).first(),entity_field,data,readonlylist)
        except  Exception as e:
            recover[0].save()
            return exception2Json(e)
        add_m=addtionclass.objects.filter(sup=sup_m).first()
        if add_m:
            add_m=change_model(add_m,addtionclass_field,data,readonlylist)
        else :
            add_m=gen_model(addtionclass,addtionclass_field,data)
            add_m.sup=sup_m
        try:
            if add_m:
                add_m.save()
        except  Exception as e:
            recover[0].save()
            recover[1].save()
            return exception2Json(e)
        return OKJson
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
    return T_S(request,"student")

@require_POST
def teacher_info(request):
    aul=role_confirm(request,'manager')
    if aul:    
        return aul
    return T_S(request,"teacher")

@require_POST
def student_unnormal_change(request):
    aul=role_confirm(request,'manager')
    if aul:    
        return aul
    entity=None
    try:
        data=json.loads(request.body)
    except JSONDecodeError:
        return NotJson
    banlist=['id','sup']
    supclass=models.Student_unnormal_change
    supclass_field=[r for r in supclass._meta.fields ]
    entity=models.Grade_downward
    other_entity=models.Major_transfer
    entity_field=[r for r in entity._meta.fields if not r.name in banlist]
    other_entity_field=[r for r in other_entity._meta.fields if not r.name in banlist]
    readonlylist=['id','change_type']
    method = data.get('method')
    data.pop('method')
    if (method == 'INSERT' or method == 'DELETE' or method == "EDIT") and data.get('id') is None:
        return IdLostJson
    if method == 'INSERT':
        if not data.get('change_type'):
            return JsonResponse({'message': 'no-change-type','code':'fail'})
        if  data.get('change_type')=='transfer':
            t=entity
            entity=other_entity
            other_entity=entity
            t=entity_field
            entity_field=other_entity_field
            other_entity_field=entity_field
        elif data.get('change_type')=='downward':
            pass
        else:
            return JsonResponse({'message': 'fail','code':'unnkown chang_type'})

        if supclass.objects.filter(id=data.get('id')).first() is not None:
            return InsertExsitJson
        sup_m=gen_model(supclass,supclass_field,data)
        try:
            sup_m.save()
        except  Exception as e:
            return exception2Json(e)
        entity_m=entity.objects.filter(sup=sup_m).first()
        entity_m=change_model(entity_m,entity_field,data)
        try:
            if entity_m:
                entity_m.save()
        except Exception as e:
            entity.objects.filter(sup=sup_m).first().delete()
            return exception2Json(e)
        return JsonResponse({'message': 'OK','code':'success'})
    elif method == 'DELETE':
        data_id= data.get('id')
        print(1111)
        sup_m=supclass.objects.filter(id=data_id).first()
        if not sup_m:
            return NotExistJson
        else:
            return try_to_delete(sup_m)
    elif method == 'FORMAT':
        dic={'message': 'OK','code':'success'}
        forma=[]
        for f in supclass_field:
            forma.append(format_one_field(f,readonlylist))
        for f in entity_field:
            forma.append(format_one_field(f,readonlylist))
        for f in other_entity_field:
            forma.append(format_one_field(f,readonlylist))
        #print(forma)
        dic['format']=forma
        return JsonResponse(dic)
    elif method == 'ALL':
        lines = entity.objects.all()
        dic={'message': 'OK','code':'success'}
        all_data=[]
        for i in lines:
            tep=model_to_dict(i.sup,supclass_field)
            tep.update(model_to_dict(i,entity_field))
            all_data.append(tep)
        lines = other_entity.objects.all()
        for i in lines:
            tep=model_to_dict(i.sup,supclass_field)
            tep.update(model_to_dict(i,other_entity_field))
            all_data.append(tep)
        dic['data']=all_data
        return JsonResponse(dic)
    elif method == "EDIT":
        recover=[]
        sup_m=supclass.objects.filter(id=data.get('id')).first() 
        if sup_m is None:
            return NotExistJson
        recover.append(deepcopy(sup_m))
        if  sup_m.change_type=='transfer':
            t=entity
            entity=other_entity
            other_entity=entity
            t=entity_field
            entity_field=other_entity_field
            other_entity_field=entity_field
        try:
            change_model_save(sup_m,supclass_field,data,readonlylist)
        except  Exception as e:
            return exception2Json(e)
        recover.append(deepcopy(entity.objects.filter(sup=sup_m).first()))
        print(entity)
        try:
            change_model_save(entity.objects.filter(sup=sup_m).first(),entity_field,data,readonlylist)
        except  Exception as e:
            recover[0].save()
            return exception2Json(e)
        return OKJson
    return NoMethodJson

PermissionJson=JsonResponse({'message': 'permisiion deny','code':'fail'})
@require_POST
def course(request):
    try:
        data=json.loads(request.body)
    except JSONDecodeError:
        return NotJson
    method = data.get('method')
    if  not request.user.is_authenticated:
        return JsonResponse({'message':'未登录用户','code':'fail'})
    if request.user.person is  None:
        return singlemodel(request,models.Course)
    if request.user.person.student_or_teacher=='student':
        if method=='ALL' or method=='FORMAT':
            return singlemodel(request,models.Course)
        elif method=='DELETE' or method=='EDIT' or method=='INSERT':
            return PermissionJson
        else:
            return NoMethodJson
    if request.user.person.student_or_teacher=='teacher':
        print(method)
        if method=='ALL' or method=='FORMAT':
            return singlemodel(request,models.Course)
        if method=='INSERT':
            return singlemodel(request,models.Course,{'teacher_id':str(models.Teacher.objects.get(sup=request.user.person).id)})
        if method=='DELETE' or method=='EDIT':
            if not data.get('id'):
                return IdLostJson
            tep=models.Course.objects.filter(id=data.get('id')).first()
            if tep:
                if tep.teacher_id==models.Teacher.objects.get(sup=request.user.person):
                    return singlemodel(request,models.Course,['teacher_id'])
                else:
                    return PermissionJson
            else:
                return NotExistJson
        return NoMethodJson

request_methods=['ALL','FORMAT','DELETE','EDIT','INSERT']
@require_POST
def course_sign_up(request):
    try:
        data=json.loads(request.body)
    except JSONDecodeError:
        return NotJson
    method = data.get('method')
    read_only=['course_id','student_id']
    if  not request.user.is_authenticated:
        return JsonResponse({'message':'未登录用户','code':'fail'})
    if request.user.person is  None:
        return singlemodel(request,models.Course_sign_up)
    if request.user.person.student_or_teacher=='student':
        entity=models.Student.objects.get(sup=request.user.person)
        if method=='FORMAT':
            return singlemodel(request,models.Course_sign_up,read_only)
        if  method=='ALL':
            dataout=[]
            for j in models.Course_sign_up.objects.filter(student_id=entity):
                dataout.append(model_to_dict(j))
            return JsonResponse({'message': 'OK','code':'success','data':dataout})
        if method=='INSERT':
            return singlemodel(request,models.Course_sign_up,read_only,{'student_id':entity.id})
        if method=='DELETE':
            if not data.get('id'):
                return IdLostJson
            tep=models.Course_sign_up.objects.filter(id=data.get('id')).first()
            if tep:
                #print(models.Course_sign_up.objects.all()[0].id)
                if tep.student_id==entity:
                    if tep.score is not None:
                        return JsonResponse({'message':'cannot quit a course having score','code':'fail'})
                    else:
                        return singlemodel(request,models.Course_sign_up,read_only)
                else:
                    return PermissionJson
            else:
                return NotExistJson
        if method in request_methods:
            return PermissionJson
        return NoMethodJson
    if request.user.person.student_or_teacher=='teacher':
        entity=models.Teacher.objects.get(sup=request.user.person)
        if method=='FORMAT':
            return singlemodel(request,models.Course_sign_up,read_only)
        if  method=='ALL':
            my_courses=models.Course.objects.filter(teacher_id=entity)
            dataout=[]
            for i in my_courses:
                for j in models.Course_sign_up.objects.filter(course_id=i):
                    dataout.append(model_to_dict(j))
            return JsonResponse({'message': 'OK','code':'success','data':dataout})
        if method=='EDIT':
            if not data.get('id'):
                return IdLostJson
            tep=models.Course_sign_up.objects.filter(id=data.get('id')).first()
            if tep:
                if tep.score is not None:
                    return JsonResponse({'message':'already has score','code':'fail'})
                if tep.course_id.teacher_id==entity:
                    return singlemodel(request,models.Course_sign_up,read_only)
                return PermissionJson
            else:
                return NotExistJson
        if method in request_methods:
            return PermissionJson
        return NoMethodJson



