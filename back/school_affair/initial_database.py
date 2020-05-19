from school_affair import models


def initial_database():
    del_list = models.Grade_downward.objects.all()
    for i in del_list:
        i.delete()
    del_list = models.Major_transfer.objects.all()
    for i in del_list:
        i.delete()
    del_list = models.Student_unnormal_change.objects.all()
    for i in del_list:
        i.delete()
    del_list = models.Course_sign_up.objects.all()
    for i in del_list:
        i.delete()
    del_list = models.Course.objects.all()
    for i in del_list:
        i.delete()
    del_list = models.Home_information.objects.all()
    for i in del_list:
        i.delete()
    del_list = models.Student.objects.all()
    for i in del_list:
        i.delete()
    del_list = models.Class.objects.all()
    for i in del_list:
        i.delete()
    del_list = models.Teacher.objects.all()
    for i in del_list:
        i.delete()
    del_list = models.Major.objects.all()
    for i in del_list:
        i.delete()
    del_list = models.Student_teacher.objects.all()
    for i in del_list:
        i.delete()
    del_list = models.Campus.objects.all()
    for i in del_list:
        i.delete()
    models.Campus.objects.create(id='Campus1', name='西校区', address='肥西路')
    models.Campus.objects.create(id='Campus2', name='东校区', address='肥西路')
    models.Campus.objects.create(id='Campus3', name='中校区', address='金寨路')
    Campus1 = models.Campus.objects.get(id='Campus1')
    Campus2 = models.Campus.objects.get(id='Campus2')
    models.Student_teacher.objects.create(id_number='10000001', id_number_type='ID card', name_chinese='王一', gender='M',
                                          born_date='1981-01-01', nationality='中国', email='wangyi@ustc.edu.cn',
                                          id='T001', student_or_teacher='teacher', entry_data='2010-09')
    models.Student_teacher.objects.create(id_number='10000002', id_number_type='ID card', name_chinese='王二', gender='M',
                                          born_date='1982-01-01', nationality='中国', email='wanger@ustc.edu.cn',
                                          id='T002', student_or_teacher='teacher', entry_data='2011-09')
    models.Student_teacher.objects.create(id_number='10000003', id_number_type='ID card', name_chinese='王三', gender='F',
                                          born_date='1983-01-01', nationality='中国', email='wangsan@ustc.edu.cn',
                                          id='T003', student_or_teacher='teacher', entry_data='2012-09')
    models.Student_teacher.objects.create(id_number='10000004', id_number_type='ID card', name_chinese='王四', gender='M',
                                          born_date='1984-01-01', nationality='中国', email='wangsi@ustc.edu.cn',
                                          id='T004', student_or_teacher='teacher', entry_data='2013-09')
    models.Student_teacher.objects.create(id_number='10000005', id_number_type='ID card', name_chinese='王五', gender='F',
                                          born_date='1985-01-01', nationality='中国', email='wangwu@ustc.edu.cn',
                                          id='T005', student_or_teacher='teacher', entry_data='2010-09')
    models.Student_teacher.objects.create(id_number='10000006', id_number_type='pass port', name_chinese='王六', gender='M',
                                          born_date='1986-01-01', nationality='美国', email='wangliu@ustc.edu.cn',
                                          id='T006', student_or_teacher='teacher', entry_data='2010-09')
    models.Student_teacher.objects.create(id_number='20000001', id_number_type='ID card', name_chinese='张一', gender='M',
                                          born_date='2000-01-01', nationality='中国', email='zhangyi@mail.ustc.edu.cn',
                                          id='S001', student_or_teacher='student', entry_data='2007-09')
    models.Student_teacher.objects.create(id_number='20000002', id_number_type='ID card', name_chinese='张二', gender='F',
                                          born_date='2001-01-01', nationality='中国', email='zhanger@mail.ustc.edu.cn',
                                          id='S002', student_or_teacher='student', entry_data='2008-09')
    models.Student_teacher.objects.create(id_number='20000003', id_number_type='ID card', name_chinese='张三', gender='M',
                                          born_date='2002-01-01', nationality='中国', email='zhangsan@mail.ustc.edu.cn',
                                          id='S003', student_or_teacher='student', entry_data='2009-09')
    models.Student_teacher.objects.create(id_number='20000004', id_number_type='ID card', name_chinese='张四', gender='M',
                                          born_date='2000-01-01', nationality='中国', email='zhangsi@mail.ustc.edu.cn',
                                          id='S004', student_or_teacher='student', entry_data='2007-09')
    models.Student_teacher.objects.create(id_number='20000005', id_number_type='ID card', name_chinese='张五', gender='M',
                                          born_date='2001-01-01', nationality='中国', email='zhangwu@mail.ustc.edu.cn',
                                          id='S005', student_or_teacher='student', entry_data='2008-09')
    models.Student_teacher.objects.create(id_number='20000006', id_number_type='ID card', name_chinese='张六', gender='M',
                                          born_date='2000-01-01', nationality='中国', email='zhangliu@mail.ustc.edu.cn',
                                          id='S006', student_or_teacher='student', entry_data='2007-09')
    TT001 = models.Student_teacher.objects.get(id='T001')
    TT002 = models.Student_teacher.objects.get(id='T002')
    TT003 = models.Student_teacher.objects.get(id='T003')
    TT004 = models.Student_teacher.objects.get(id='T004')
    TT005 = models.Student_teacher.objects.get(id='T005')
    TT006 = models.Student_teacher.objects.get(id='T006')
    SS001 = models.Student_teacher.objects.get(id='S001')
    SS002 = models.Student_teacher.objects.get(id='S002')
    SS003 = models.Student_teacher.objects.get(id='S003')
    SS004 = models.Student_teacher.objects.get(id='S004')
    SS005 = models.Student_teacher.objects.get(id='S005')
    SS006 = models.Student_teacher.objects.get(id='S006')
    models.Major.objects.create(id='M001', name='Math', campus_id=Campus2, address='金寨路')
    models.Major.objects.create(id='M002', name='Physics', campus_id=Campus2, address='金寨路')
    models.Major.objects.create(id='M003', name='SC', campus_id=Campus1, address='肥西路')
    models.Major.objects.create(id='M004', name='Engineering', campus_id=Campus1, address='肥西路')
    M001 = models.Major.objects.get(id='M001')
    M002 = models.Major.objects.get(id='M002')
    M003 = models.Major.objects.get(id='M003')
    M004 = models.Major.objects.get(id='M004')
    T001 = models.Teacher.objects.get(sup=TT001)
    T001.major_id = M001
    T001.professional_title = 'professor'
    T001.save()
    T002 = models.Teacher.objects.get(sup=TT002)
    T002.major_id = M001
    T002.professional_title = 'associate professor'
    T002.save()
    T003 = models.Teacher.objects.get(sup=TT003)
    T003.major_id = M001
    T003.professional_title = 'associate professor'
    T003.save()
    T004 = models.Teacher.objects.get(sup=TT004)
    T004.major_id = M002
    T004.professional_title = 'associate professor'
    T004.save()
    T005 = models.Teacher.objects.get(sup=TT005)
    T005.major_id = M003
    T005.professional_title = 'professor'
    T005.save()
    T006 = models.Teacher.objects.get(sup=TT006)
    T006.major_id = M004
    T006.professional_title = 'professor'
    T006.save()
    M001.person_in_charge = T001
    M001.save()
    M002.person_in_charge = T002
    M002.save()
    M003.person_in_charge = T003
    M003.save()
    M004.person_in_charge = T004
    M004.save()
    Cl001 = models.Class.objects.create(id=1001, name='1班', begin_time='2017-09', major_id=M001, grade=3, header_teacher=T001)
    Cl002 = models.Class.objects.create(id=1002, name='2班', begin_time='2018-09', major_id=M001, grade=2, header_teacher=T002)
    Cl003 = models.Class.objects.create(id=1003, name='3班', begin_time='2017-09', major_id=M002, grade=3, header_teacher=T003)
    Cl004 = models.Class.objects.create(id=1004, name='4班', begin_time='2019-09', major_id=M003, grade=1, header_teacher=T004)
    Cl005 = models.Class.objects.create(id=1005, name='5班', begin_time='2018-09', major_id=M003, grade=2, header_teacher=T005)
    Cl006 = models.Class.objects.create(id=1006, name='6班', begin_time='2017-09', major_id=M003, grade=3, header_teacher=T006)
    S001 = models.Student.objects.get(sup=SS001)
    S001.class_id = Cl001
    S001.save()
    S002 = models.Student.objects.get(sup=SS002)
    S002.class_id = Cl001
    S002.save()
    S003 = models.Student.objects.get(sup=SS003)
    S003.class_id = Cl002
    S003.save()
    S004 = models.Student.objects.get(sup=SS004)
    S004.class_id = Cl003
    S004.save()
    S005 = models.Student.objects.get(sup=SS005)
    S005.class_id = Cl004
    S005.save()
    S006 = models.Student.objects.get(sup=SS006)
    S006.class_id = Cl006
    S006.save()
    models.Home_information.objects.create(sup=TT001, home_address='合肥', post_code='111001',
                                           home_telephone_number='88880001')
    models.Home_information.objects.create(sup=TT002, home_address='合肥', post_code='111001',
                                           home_telephone_number='88880002')
    models.Home_information.objects.create(sup=TT003, home_address='合肥', post_code='111001',
                                           home_telephone_number='88880003')
    models.Home_information.objects.create(sup=SS001, home_address='合肥', post_code='111001',
                                           home_telephone_number='88880004')
    models.Home_information.objects.create(sup=SS002, home_address='合肥', post_code='111001',
                                           home_telephone_number='88880005')
    models.Home_information.objects.create(sup=SS003, home_address='合肥', post_code='111001',
                                           home_telephone_number='88880006')
    models.Course.objects.create(id='C001', name='Math1', examination='exam', major_id=M001, teacher_id=T001,
                                 start_year=2019, start_semester='spring', course_time='Monday-1')
    models.Course.objects.create(id='C002', name='Math2', examination='query', major_id=M001, teacher_id=T002,
                                 start_year=2019, start_semester='fall', course_time='Tuesday-1')
    models.Course.objects.create(id='C003', name='Physics1', examination='exam', major_id=M002, teacher_id=T004,
                                 start_year=2019, start_semester='fall', course_time='Monday-2')
    models.Course.objects.create(id='C004', name='CS1', examination='exam', major_id=M003, teacher_id=T005,
                                 start_year=2020, start_semester='spring', course_time='Monday-5')
    models.Course.objects.create(id='C005', name='CS2', examination='exam', major_id=M003, teacher_id=T005,
                                 start_year=2020, start_semester='spring', course_time='Friday-1')
    models.Course.objects.create(id='C006', name='Engineering1', examination='exam', major_id=M004, teacher_id=T006,
                                 start_year=2020, start_semester='spring', course_time='Wednesday-3')
    C001 = models.Course.objects.get(id='C001')
    C002 = models.Course.objects.get(id='C002')
    C003 = models.Course.objects.get(id='C003')
    C004 = models.Course.objects.get(id='C004')
    C005 = models.Course.objects.get(id='C005')
    C006 = models.Course.objects.get(id='C006')
    models.Course_sign_up.objects.create(course_id=C001, student_id=S001, score=90)
    models.Course_sign_up.objects.create(course_id=C001, student_id=S002, score=85)
    models.Course_sign_up.objects.create(course_id=C002, student_id=S001, score=95)
    models.Course_sign_up.objects.create(course_id=C003, student_id=S003, score=90)
    models.Course_sign_up.objects.create(course_id=C004, student_id=S004, score=90)
    models.Course_sign_up.objects.create(course_id=C005, student_id=S005, score=80)
    models.Course_sign_up.objects.create(course_id=C006, student_id=S005, score=95)
    models.Course_sign_up.objects.create(course_id=C006, student_id=S006, score=85)
    models.Student_unnormal_change.objects.create(id='UC001', data='2019-06', class_before=Cl003, class_after=Cl001,
                                                  change_type='transfer', student_id=S003)
    models.Student_unnormal_change.objects.create(id='UC002', data='2019-06', class_before=Cl005, class_after=Cl002,
                                                  change_type='transfer', student_id=S004)
    models.Student_unnormal_change.objects.create(id='UC003', data='2019-06', class_before=Cl001, class_after=Cl002,
                                                  change_type='downward', student_id=S002)
    UC001 = models.Student_unnormal_change.objects.get(id='UC001')
    UC002 = models.Student_unnormal_change.objects.get(id='UC002')
    UC003 = models.Student_unnormal_change.objects.get(id='UC003')
    Mt001 = models.Major_transfer.objects.get(sup=UC001)
    Mt001.youth_league_changed = 'yes'
    Mt001.save()
    Mt002 = models.Major_transfer.objects.get(sup=UC002)
    Mt002.youth_league_changed = 'yes'
    Mt002.save()
    Gd001 = models.Grade_downward.objects.get(sup=UC003)
    Gd001.cause = 'suspend'
    Gd001.save()
