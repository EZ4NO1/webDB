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
        return exception2Json(e)



def try_to_delete(model):
    try:
         model.delete()
    except Exception as e:
        return JsonResponse({'message':e.message,'code':'fail'})
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
            print(cdict)
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
    return one_field
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
            t[i]=str(t[i])
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
    readonlylist=readonlylist+['id','id_number']
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
        add_m=gen_model(addtionclass,addtionclass_field,data)
        if (add_m):
            add_m.sup=sup_m
        try:
            entity_m.save()
            if (add_m):
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
            add_m=change_model(add_m,addtionclass_field,data,banlist)
        else :
            add_m=gen_model(addtionclass,addtionclass_field,data)
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


def student_unnormal_change(request):
   pass


def course(request):
    pass


def course_sign_up(request):
    pass



