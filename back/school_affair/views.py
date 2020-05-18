from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate  
from django.contrib.auth import login as django_login
from django.shortcuts import redirect
from . import models
import json
from django.http import JsonResponse
import datetime

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




def campus(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        method = json_data['method']
        if method == 'INSERT':
            data = models.Campus()
            data.id = json_data['campus_id']
            data.name = json_data['campus_name']
            data.address = json_data['campus_address']
            if not data.id:
                return JsonResponse({'message': '主键不能为空！'})
            else:
                data.save()
                return JsonResponse({'message': 'OK'})
        elif method == 'DELETE':
            campus_id = json_data['campus_id']
            data = models.Campus.objects.filter(id=campus_id)
            if not data:
                return JsonResponse({'message': '数据不存在！'})
            else:
                refer_data = models.Major.objects.filter(campus_id=campus_id)
                if refer_data:
                    return JsonResponse({'message': '存在关联信息：专业'})
                else:
                    data.delete()
                    return JsonResponse({'message': 'OK'})
        elif method == 'QUERY':
            campus_id = json_data['campus_id']
            data = models.Campus.objects.filter(id=campus_id)
            if not data:
                return JsonResponse({'message': '数据不存在！'})
            else:
                return JsonResponse({'message': 'OK',
                                     'campus_id': campus_id,
                                     'campus_name': data['name'],
                                     'campus_address': data['address']})
        elif method == "EDIT":
            campus_id = json_data['campus_id']
            data = models.Campus.objects.filter(id=campus_id)
            if not data:
                return JsonResponse({'message': '数据不存在！'})
            else:
                data.name = json_data['campus_name']
                data.address = json_data['campus_address']
                data.save()
                return JsonResponse({'message': 'OK'})


def major(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        method = json_data['method']
        if method == 'INSERT':
            data = models.Major()
            data.id = json_data['major_id']
            data.name = json_data['major_name']
            data.campus_id = json_data['campus_id']
            data.person_in_charge = json_data['person_in_charge']
            data.address = json_data['major_address']
            if not data.id:
                return JsonResponse({'message': '主键不能为空！'})
            else:
                data.save()
                return JsonResponse({'message': 'OK'})
        elif method == 'DELETE':
            major_id = json_data['major_id']
            data = models.Major.objects.filter(id=major_id)
            if not data:
                return JsonResponse({'message': '数据不存在！'})
            else:
                refer_data = models.Teacher.objects.filter(major_id=major_id)
                if refer_data:
                    return JsonResponse({'message': '存在关联信息：教师'})
                else:
                    data.delete()
                    return JsonResponse({'message': 'OK'})
        elif method == 'QUERY':
            major_id = json_data['major_id']
            data = models.Major.objects.filter(id=major_id)
            if not data:
                return JsonResponse({'message': '数据不存在！'})
            else:
                return JsonResponse({'message': 'OK',
                                     'major_id': major_id,
                                     'major_name': data['name'],
                                     'campus_id': data['campus_id'],
                                     'person_in_charge': data['person_in_charge'],
                                     'major_address': data['address']})
        elif method == "EDIT":
            major_id = json_data['major_id']
            data = models.Campus.objects.filter(id=major_id)
            if not data:
                return JsonResponse({'message': '数据不存在！'})
            else:
                data.name = json_data['major_name']
                data.campus_id = json_data['campus_id']
                data.person_in_charge = json_data['major_person_in_charge']
                data.address = json_data['major_address']
                data.save()
                return JsonResponse({'message': 'OK'})


def class_info(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        method = json_data['method']
        if method == 'INSERT':
            data = models.Class()
            data.id = json_data['class_id']
            data.name = json_data['class_name']
            data.begin_time = json_data['class_begin_time']
            data.major_id = json_data['major_id']
            data.grade = json_data['class_grade']
            data.header_teacher = json_data['header_teacher']
            if not data.id:
                return JsonResponse({'message': '主键不能为空！'})
            else:
                data.save()
                return JsonResponse({'message': 'OK'})
        elif method == 'DELETE':
            class_id = json_data['class_id']
            data = models.Class.objects.filter(id=class_id)
            if not data:
                return JsonResponse({'message': '数据不存在！'})
            else:
                refer_data = models.Student.objects.filter(class_id=class_id)
                if refer_data:
                    return JsonResponse({'message': '存在关联信息：学生'})
                else:
                    data.delete()
                    return JsonResponse({'message': 'OK'})
        elif method == 'QUERY':
            class_id = json_data['class_id']
            data = models.Class.objects.filter(id=class_id)
            if not data:
                return JsonResponse({'message': '数据不存在！'})
            else:
                return JsonResponse({'message': 'OK',
                                     'class_id': class_id,
                                     'class_name': data['name'],
                                     'class_begin_time': data['begin_time'],
                                     'major_id': data['major_id'],
                                     'class_grade': data['grade'],
                                     'header_teacher': data['header_teacher']})
        elif method == "EDIT":
            class_id = json_data['class_id']
            data = models.Class.objects.filter(id=class_id)
            if not data:
                return JsonResponse({'message': '数据不存在！'})
            else:
                data.name = json_data['class_name']
                data.begin_time = json_data['class_begin_time']
                data.major_id = json_data['major_id']
                data.grade = json_data['class_grade']
                data.header_teacher = json_data['header_teacher']
                data.save()
                return JsonResponse({'message': 'OK'})


def student_info(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        method = json_data['method']
        if method == 'INSERT':
            data = models.Student_teacher()
            data_home = models.Home_information()
            data.id_number = json_data['student_teacher_idnumber']
            data.id_number_type = json_data['id_number_type']
            data.name_chinese = json_data['name_chinese']
            data.gender = json_data['gender']
            data.born_date = json_data['born_date']
            data.nationality = json_data['nationality']
            data.email = json_data['email']
            data.student_teacher_id = json_data['student_teacher_id']
            data.student_or_teacher = '学生'
            data.entry_data = json_data['entry_data']
            data_home.student_teacher_id_number = json_data['student_teacher_idnumber']
            data_home.home_address = json_data['home_address']
            data_home.post_code = json_data['post_code']
            data_home.home_telephone_number = json_data['home_telephone_number']
            if not data.id_number:
                return JsonResponse({'message': '主键不能为空！'})
            else:
                data.save()
                data_home.save()
                return JsonResponse({'message': 'OK'})
        elif method == 'DELETE':
            id_number = json_data['student_teacher_idnumber']
            data = models.Student_teacher.objects.filter(id_number=id_number, student_or_teacher='学生')
            data_home = models.Home_information.objects.filter(id_number=id_number)
            if not data:
                return JsonResponse({'message': '数据不存在！'})
            else:
                if int(datetime.datetime.year) - int(json_data['entry_data']) <= 4:
                    return JsonResponse({'message': '学生尚未毕业！'})
                else:
                    data.delete()
                    if data_home:
                        data_home.delete()
                    return JsonResponse({'message': 'OK'})
        elif method == 'QUERY':
            id_number = json_data['student_teacher_idnumber']
            data = models.Student_teacher.objects.filter(id=id_number, student_or_teacher='学生')
            data_home = models.Home_information.objects.filter(id_number=id_number)
            if not data:
                return JsonResponse({'message': '数据不存在！'})
            elif data_home:
                return JsonResponse({'message': 'OK',
                                     'id_number': data['id_number'],
                                     'id_number_type': data['id_number_type'],
                                     'name_chinese': data['name_chinese'],
                                     'gender': data['gender'],
                                     'born_date': data['born_date'],
                                     'nationality': data['nationality'],
                                     'email': data['email'],
                                     'student_teacher_id': data['student_teacher_id'],
                                     'student_or_teacher': '学生',
                                     'entry_data': data['entry_data'],
                                     'home_address': data_home['home_address'],
                                     'post_code': data_home['post_code'],
                                     'home_telephone_number': data_home['home_telephone_number']})
            else:
                return JsonResponse({'message': 'OK',
                                     'id_number': data['id_number'],
                                     'id_number_type': data['id_number_type'],
                                     'name_chinese': data['name_chinese'],
                                     'gender': data['gender'],
                                     'born_date': data['born_date'],
                                     'nationality': data['nationality'],
                                     'email': data['email'],
                                     'student_teacher_id': data['student_teacher_id'],
                                     'student_or_teacher': '学生',
                                     'entry_data': data['entry_data']})
        elif method == "EDIT":
            id_number = json_data['student_teacher_idnumber']
            data = models.Student_teacher.objects.filter(id=id_number, student_or_teacher='学生')
            data_home = models.Home_information.objects.filter(id_number=id_number)
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
                if data_home:
                    data_home.home_address = json_data['home_address']
                    data_home.post_code = json_data['post_code']
                    data_home.home_telephone_number = json_data['home_telephone_number']
                    data_home.save()
                return JsonResponse({'message': 'OK'})


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




