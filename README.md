# :pencil:概述

一个基于mysql+django+vue的前后端完全分离的web高校管理系统

# :mortar_board:组内人员和分工情况

# :house:系统架构

![Untitled Diagram (3)](D:\3spring\数据库\lab3\Untitled Diagram (5).png)

如图所示，使用的是前后端完全分离的架构，django代理MySQL的控制，MySQl中的数据用Django.models封装，一切开放给终端用户的操作封装在Django Web API中。前端页面由Vue+Vuetify生成，用vue-cli4生成静态页面，再由django router充当web服务器统一路由。

其中权限控制由Django Web API管理，数据的进一步处理（如搜索，排序，分类）由前端负责

**整个系统的工作流程是：**

浏览器请求网页，Django Router返回网页，浏览器请求数据，发送POST请求给Django Web API，Django Web API验证身份后，从django.models中提取数据，返回数据给浏览器，填充网页中数据表中的数据。

在浏览器中用户对数据进行增删改操作，发送POST请求给Django Web API，Django Web API验证身份后，对django.models进行增删改，django自动把更改同步到MySQL中。

Vue+Vuetify只负责静态页面的生成，在用户使用时不工作。



# :paperclip:系统详细设计  

## **数据库设计**

### 数据库中的表

#### **1.校区表Campus**

```python
class Campus(clean_model):
    id=models.CharField(validators=[MinLengthValidator(1)],max_length=var_char_length,primary_key=True)
    name=models.CharField(validators=[MinLengthValidator(1)],max_length=var_char_length)
    address=models.CharField(validators=[MinLengthValidator(1)],max_length=var_char_length)
    def __str__(self):
        return self.name
```

校区表包括3个属性：

- id校区代码为主键
- name为校区名称
- address为校区地址

三个属性类型均为CharField

#### **2.专业表Major**

```python
class Major(clean_model):
    id=models.CharField(validators=[MinLengthValidator(1)],max_length=var_char_length,primary_key=True)
    name=models.CharField(validators=[MinLengthValidator(1)],max_length=var_char_length)
    campus_id=models.ForeignKey('Campus', on_delete=models.PROTECT)
    person_in_charge_id=models.ForeignKey('Teacher', on_delete=models.SET_NULL,null=True,blank=True)
    address=models.CharField(validators=[MinLengthValidator(1)],max_length=var_char_length)
```

专业表包括5个属性：

- id专业代码为主键
- name为专业名称
- campus_id为外键引用Campus表，on_delete参数设置为PROTECT，即当Major表中引用了Campus表中的某个校区时，该校区不允许被删除
- person_in_charge专业负责人，为外键引用Teacher表，可以为空，on_delete参数设置为SET_NULL，即当引用的外键被删除时，Major表中的person_in_charge字段会被置空。
- address为专业地址

#### **3.班级表Class**

```python
class Class(clean_model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(validators=[MinLengthValidator(1)],max_length=var_char_length)
    begin_time=YMField()
    major_id=models.ForeignKey('Major', on_delete=models.CASCADE)
    grade=models.IntegerField()
    header_teacher=models.ForeignKey("Teacher",on_delete=models.CASCADE)
```

班级表包括6个属性：

- id班级代码为主键，类型为IntegerField
- name为班级名称
- begin_time为建班年月，类型为YMField，格式应为"YYYY-MM"
- major_id为外键引用Major表，on_delete设为CASCADE，采用级联删除
- grade为所属年级，类型为IntegerField
- header_teacher为班主任，外键引用Teacher表，采用级联删除

#### **4.个人信息表Student_teacher**

```python
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
```

个人信息表包含10个属性：

- id学号/工号为主键
- id_number为身份证件号，unique=TRUE代表身份证件号是唯一的
- id_number_type为身份证件类型，可选值为身份证或护照
- name_chinese为中文名
- gender为性别，可选值为男或女
- born_date为出生日期，类型为BirthField，格式为"YYYY-MM-DD"
- nationality为国籍
- email为邮箱，类型为EmailField
- student_or_teacher用来标识学生或教师，可选值为学生或教师
- entry_data为入校年月，类型为YMField，格式为"YYYY-MM"

#### **5.教师表Teacher**

```python
class Teacher(clean_model):
    id=models.AutoField(primary_key=True)
    sup=models.OneToOneField("Student_teacher",on_delete=models.PROTECT)
    major_id=models.ForeignKey("Major", on_delete=models.PROTECT,null=True,blank=True)
    professional_title=models.CharField(max_length=20,choices=(('professor','教授'),('associate professor','副教授')),null=True,blank=True)
```

教师表包含4个属性：

- id为主键，类型为AutoField，由数据库自动生成一个自增的变量
- sup为外键，引用个人信息表，类型为OneToOneField，代表一对一的关系，on_delete=PROTECT，有外键时不允许删除
- major_id所属专业为外键，引用Major表，有外键时不允许删除，可以为空
- professional_title为职称，可选值为教授或副教授，可以为空

#### **6.学生表Student**

```python
class Student(clean_model):
    id=models.AutoField(primary_key=True)
    sup=models.OneToOneField("Student_teacher",on_delete=models.PROTECT)
    class_id=models.ForeignKey("Class", on_delete=models.CASCADE,null=True,blank=True)
```

学生表包含3个属性：

- id为主键，类型为AutoField，由数据库自动生成一个自增的变量
- sup为外键，引用个人信息表，类型为OneToOneField，代表一对一的关系，on_delete=PROTECT，有外键时不允许删除
- class_id所属班级为外键，引用Class表，采用级联删除，可以为空

#### **7.家庭信息表Home_information**

```python
class Home_information(clean_model):
    id=models.AutoField(primary_key=True)
    sup=models.OneToOneField("Student_teacher",on_delete=models.CASCADE)
    home_address=models.CharField(validators=[MinLengthValidator(1)],max_length=var_char_length,null=True,blank=True)
    post_code=models.CharField(validators=[MinLengthValidator(1)],max_length=var_char_length,null=True,blank=True)
    home_telephone_number=models.CharField(validators=[MinLengthValidator(1)],max_length=var_char_length,null=True,blank=True)
```

家庭信息表包含5个属性：

- id为主键，类型为AutoField，由数据库自动生成一个自增的变量
- sup为外键，一对一引用个人信息表，采用级联删除
- home_address为家庭住址，可以为空
- post_code为家庭邮政编码，可以为空
- home_telephone_number为家庭电话，可以为空

#### **8.课程表Course**

```python
class Course(clean_model):
    id=models.CharField(validators=[MinLengthValidator(1)],max_length=var_char_length,primary_key=True)
    name=models.CharField(validators=[MinLengthValidator(1)],max_length=var_char_length)
    examination=models.CharField(max_length=10,choices=(('exam','考试'),('query','当堂答辩')))
    major_id=models.ForeignKey("Major",on_delete=models.CASCADE)
    teacher_id=models.ForeignKey("Teacher",on_delete=models.CASCADE)
    start_year=models.IntegerField()
    start_semester=models.CharField(max_length=10,choices=(('spring','春'),('fall','秋')))
    course_time=models.CharField(validators=[MinLengthValidator(1)],max_length=var_char_length)
```

课程表包含8个属性：

- id课程号为主键
- name为课程名称
- examination为考核方式，可选值为考试或当堂答辩
- major_id开课专业为外键，引用Major表，采用级联删除
- teacher_id为外键，引用教师表，采用级联删除
- start_year为开课年份，类型为IntegerField
- start_semester为开课学期，可选值为春或秋
- course_time为开课时间，每周一节课，记录方式为"Monday-1"，即星期几-第几节课。

#### **9.选课表Course_sign_up**

```python
class Course_sign_up(clean_model):
    id=models.AutoField(primary_key=True)
    course_id=models.ForeignKey("Course",on_delete=models.PROTECT)
    student_id=models.ForeignKey("Student",on_delete=models.CASCADE)
    score=models.IntegerField(null=True,blank=True)
```

选课表包含4个属性：

- id为主键，类型为AutoField，由数据库自动生成一个自增的变量
- course_id为外键，引用Course表，当外键存在时不允许删除
- student_id为外键，引用Student表，采用级联删除
- score为考试成绩，类型为IntegerField，可以为空

#### **10.学籍异动表Student_unnormal_change**

```python
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
```

学籍异动表包含6个属性：

- id异动编号为主键
- data为异动日期（年月），类型为YMField，格式为"YYYY-MM"
- class_before为原班级代码，外键引用Class表，采用级联删除
- class_after为现班级代码，外键引用Class表，采用级联删除
- change_type为异动类型，可选值为转专业或降级
- student_id为外键，引用Student表，采用级联删除

#### **11.转专业表Major_transfer**

```python
class Major_transfer(clean_model):
    id=models.AutoField(primary_key=True)
    sup=models.OneToOneField('Student_unnormal_change',on_delete=models.CASCADE)
    youth_league_changed=models.CharField(max_length=5,choices=(
        ('yes','是'),
        ('no','不是'),
        ('not a','不是团员')
    ),null=True,blank=True
    )
```

转专业表包含3个属性：

- id为主键，类型为AutoField，由数据库自动生成一个自增的变量
- sup为外键，一对一引用学籍异动表，采用级联删除
- youth_league_changed为是否已转出团员关系，可选值有"是"、"不是"、"不是团员"，可以为空

#### **12.降级表Grade_downward**

```python
class Grade_downward(clean_model):
    id=models.AutoField(primary_key=True)
    sup=models.OneToOneField('Student_unnormal_change',on_delete=models.CASCADE)
    cause=models.CharField(max_length=10,choices=(('suspend','休学'),('teacher','支教')),null=True,blank=True)
```

降级表包含3个属性：

- id为主键，类型为AutoField，由数据库自动生成一个自增的变量
- sup为外键，一对一引用学籍异动表，采用级联删除
- cause为降级原因，可选值为休学或支教，可以为空

### **13.账户表school_user**

```python
class school_user(AbstractUser):
    person=models.OneToOneField("Student_teacher",on_delete=models.CASCADE,null=True,blank=True,unique=True)
```

降级表包含3个属性：

- username为主键，为登录时的用户名
- password,加密后的密码
- person,这个账户对应的人，可以为老师或学生，若为空，该账户身份为管理员

---

### 数据库中添加的约束

- 外键on_delete=PROTECT的属性，有外键被引用时不允许删除
- 主键以及unique=True的属性唯一
- 学生选课表中，增加约束使得同一名学生不允许重复选课
- 学生表中，不允许删除未毕业的学生（通过入学年月和当前时间计算入学是否已满4年）
- 对所有日期或时间域，判断时间是否在在建校时间和当前时间之间

### Django中添加的触发信号

- 在添加一个teacher_student时，会根据teacher_or_student域判断是学生还是教师,在student表或teacher表中建立相应的项。teacher表或student表中某项删除，teacher_student表中的对应数据也相应删除，home_information表中对应的数据也相应删除。同样的，teacher_student表中某项删除，相应的其他两个表中的数据也会删除。
- 在添加一个unoraml_change时，会根据teacher_or_student域判断是学生还是教师,在student表或teacher表中建立相应的项。teacher表或student表中某项删除，teacher_student表中的对应数据也相应删除，home_information表中对应的数据也相应删除。同样的，teacher_student表中某项删除，相应的其他两个表中的数据也会删除。
- 在添加一个teacher_student时，会同步添加一个账户，用户名为学号/工号，密码为证件号，删除teacher_student时，会同步删除对应的账户

### 实现的一致性

- 子实体和父实体间的一致性

- 弱实体和弱实体关联的强实体间的一致性

- teacher_student和账户之间的一致性

  （这两者通过Django触发信号)

  



## Django web-API(后端提供个前端的接口)

### ###4种用户权限等级  

1. root     （root用户为django的超级用户，通过/admin登录，不在前端的设计范围内）
2. manager
3. teacher
4. student

在登录时，通过session-id保有登录信息，不同用户等级，对数据有不同权限的访问

### 1.用户登录接口(仅manager)

- 方法描述：用户登录
- URL地址：/login
- HTTP请求方式：POST
- 请求参数：
  1. username：用户名，类型为String，必填
  2. password：密码，类型为String，必填

- 返回结果：{"code":"success" ,"url":"/campus"} url中提示跳转的url
- 请求示例：

```json
"request": {
    "method": "POST",
    "body": {
        "mode": "formdata",
        "formdata": [
            {
                "key": "password",
                "value": "123",
            },
            {
                "key": "username",
                "value": "123",
            }
        ]
    }
}
```

- 备注：包含4种身份信息，root、manager、teacher、student，对应不同的权限。每个教师账号对应一个teacher实体，每个学生账号对应一个student实体，默认用户名为学号/工号，密码为身份证件号

### 2.用户登出接口(仅manager)

- 方法描述：用户登录
- URL地址：/logout
- HTTP请求方式：POST
- 请求参数：无
- 返回结果：HttpResponse，显示登出是否成功

### 3.校区管理接口(仅manager)

- 方法描述：对校区信息进行增删查改

- URL地址：/campus

- HTTP请求方式：POST

- 请求参数：method，类型为String，必填

  1. method=FORMAT： 代表返回数据表元信息（列信息）

     不需要其他参数

  2. method=ALL： 代表返回当前权限可见的所有数据

     不需要其他参数

  3. method=INSERT：代表插入数据

     - id：校区代码，类型为String，必填
     - name：校区名称，类型为String
     - address：校区地址，类型为String

  4. method=DELETE：代表删除数据

     - id：校区代码，类型为String，必填

  5. method=EDIT：代表修改数据

     - id：校区代码，类型为String，必填
     - 需要修改的字段以及修改后的值

- 返回格式：

  1. method=FORMAT：

  ```json
  {
      "code":"success",
      "message":"OK",
      "format":[{"name":"id", "type":auto", "readonly"="false"},​{"name"="student" ,"type"="link" ,"readonly"="false","alter":{"PB1703":"高岩"}}
      ]
  }
  ```

  2. method=ALL：

  ```json
  {
      "code":"success" ,
      "message":"OK",
      "data":[
          {"id":"123","student":"高岩"}
      ]
  }
  ```

  3. method=INSERT：

  ```json
  {"code":"success" ,"message":"OK"}
  ```

  4. method=DELETE：

  ```json
  {"code":"success" ,"message":"OK"}
  ```

  5. method=EDIT：

  ```json
  {"code":"success" ,"message":"OK"}
  ```

  6. 发生错误时返回：

  ```json
  {"code":"fail" ,"message":"错误信息"}
  或
  {"code":"fail" ,"message":{"错误字段":"错误原因"}}
  ```

- 权限信息：仅manager能访问

- 备注：下述所有接口的请求参数、返回格式与校区管理接口类似，不再赘述

### 4.专业管理接口(仅manager)

- 方法描述：对专业信息进行增删查改
- URL地址：/major
- HTTP请求方式：POST
- 权限信息：仅manager能访问

### 5.班级管理接口(仅manager)

- 方法描述：对班级信息进行增删查改
- URL地址：/class
- HTTP请求方式：POST
- 权限信息：仅manager能访问

### 6.学生信息管理接口(仅manager)

- 方法描述：对学生信息进行增删查改
- URL地址：/student
- HTTP请求方式：POST
- 权限信息：仅manager能访问

### 7.教师信息管理接口(仅manager)

- 方法描述：对教师信息进行增删查改
- URL地址：/teacher
- HTTP请求方式：POST
- 权限信息：仅manager能访问

### 8.学籍异动管理接口(仅manager)

- 方法描述：对学籍异动信息进行增删查改
- URL地址：/unnormal
- HTTP请求方式：POST
- 权限信息：仅manager能访问

### 9.课程管理接口(所有人)

- 方法描述：对课程信息进行增删查改
- URL地址：/course
- HTTP请求方式：POST
- 权限信息：
  - manager：拥有全部权限
  - teacher：拥有FORMAT和ALL权限，对自己开设的课程拥有全部权限
  - student：仅拥有FORMAT和ALL权限

### 10.选课管理接口(所有人)

- 方法描述：对选课信息进行增删查改
- URL地址：/course_sign_up
- HTTP请求方式：POST
- 权限信息：
  - manager：拥有全部权限
  - teacher：拥有FORMAT权限，对自己开设的课程拥有ALL权限(返回自己开设课程的选课信息)，有EDIT权限(给定分数)
  - student：拥有FORMAT权限，ALL返回自己选的课程，INSERT代表选课，对自己已选且未出分的课程拥有DELETE权限，没有EDIT权限

# **前端设计**

以以下两个component为主：

### DataTable.vue

*数据表：负责前端所有的数据交互，包括显示数据，增删改数据，搜索，按列搜索，排序，分类*

*主要继承了vuetify中的v-data-table，并在此基础上增加了按列搜索的功能，并将数据表和后端连通，使得在前端数据表上的操作能改变数据库中的数据*

##### DataTable.vue

```javascript
methods: {
      customFilter(value, search,item) {
        if (item.hasOwnProperty(this.filter_value)){
          if (item[this.filter_value].toLowerCase().indexOf(search.toLowerCase()) != -1)
            return true;
          else return false;
        }
        else {
          for (var i in item){
            if (item[i].toLowerCase().indexOf(search.toLowerCase()) == -1)
            return false;
          }
          return true;
        }
      },
      newItem(){
        this.formdata=[];
        for (var head of this.headers){
          if (head['value']!='actions' && this.datatype[head['value']]!='auto' )
          this.formdata.push({label:head['value'],data:''});
        }
        this.mode='insert';
        this.dialog = true;
      },
      editItem (item) {
        this.formdata=[];
        for (var str1 in this.editedItem){
          this.formdata.push({label:str1,data:item[str1]});
        }
        this.mode='edit';
        this.currentid=item['id'];
        this.dialog = true;
      },
      deleteItem (item) {
        if (confirm('你真的要删除这一项吗?')==true){
         			this.$http.post(this.$props.url,JSON.stringify({method:'DELETE',id:item['id']})).then(function(res){
                              var x= res.body;
                              this.hint=x['message'];
                            this.data_update();
                        },function(res){
                            alert(res.status)
                        });       
        }
      },
}
```

**函数说明：**

customFilter(value, search,item) 

过滤属性用于排序

newItem()

绑定创建的按钮，用formdata收集用户信息，调用save或close

editItem (item) 

绑定编辑的按钮，用formdata收集用户信息，调用save或close

deleteItem (item)

绑定删除按钮，调用post向后台删除数据

```javascript
close () {
        this.dialog = false
}, 
save () {
        if (this.mode=='edit' || this.mode=='insert'){

            var datadict={};
            ////window.console.log(JSON.stringify(alter));
            var alter=this.dataalter;
            for (var value of this.formdata){
              if (alter.hasOwnProperty(value['label'])){
                datadict[value['label']]=alter[value['label']][value['data']];
              }
              else{
                datadict[value['label']]=value['data'];
              }
            }
            ////window.console.log(JSON.stringify(datadict));

              if (this.mode=='edit') {
              datadict['id']=this.currentid;
              datadict['method']='EDIT';
              }
              if (this.mode=='insert') {
              datadict['method']='INSERT';
              }
              this.$http.post(this.$props.url,JSON.stringify(datadict)).then(function(res){
              var x = res.body;
              this.hint=x['message'];
              this.data_update();
            },function(res){
              alert(res.status)
            });
            need_update=true;
        }

        this.close()
      },
 data_update(){
 this.$http.post(this.$props.url,JSON.stringify({method:'FORMAT'})).then(function(res){
        var x= res.body;
        var code=x['code'];
        this.datatype={};
		this.dataalter={};
        this.filter_c=['All'];
        if (code=='fail'){  this.hint=x['message']
                            return;
		}
                            
                            if (code=='success'){
                              this.editedItem={};
                              this.headers=[];
                              for (var i of x['format']){
                                var item={};
                                var name =i['name']
                                  if (i['read_only']=='false'){
                                    this.editedItem[name]='';
                                  }
                                item['text']=name;
                                item['value']=name;
                                item['align']='center';
                                this.datatype[name]=i['type'];
                                this.headers.push(item);
                                this.filter_c.push(name);
                                if (i.hasOwnProperty('alter')){
                                  var tep={};
                                  for (var index in i['alter']){
                                    tep[i['alter'][index]]=index;
                                  }
                                  this.dataalter[name]=tep;
                                  var tlist=[];
                                  for (var index in i['alter']){
                                    tlist.push(i['alter'][index]);
                                  }
                                  this.alterkeys[name]=tlist;
                                }
                              }
                              if (this.$props.edit||this.$props.delete1)
                              this.headers.push({ text: 'Actions', value: 'actions', sortable: false,align:'center' });
                              }},function(res){
                            alert(res.status)
                        });
          this.$http.post(this.$props.url,JSON.stringify({method:'ALL'})).then(function(res){
                            var x= res.body;
                            var code=x['code'];
                            if (code=='fail'){
                              this.hint=x['message']
                              return;
                            } 
                            if (code=='success'){
                              this.tabledata=x['data'];
                              }
                        },function(res){
                            alert(res.status)
                        });
       window.vue=this;
    }
  }
```

close()   关闭dialog

save()     判断INSERT接口的类型，打包formdata，发给后台

update()    通过`$http.post()`调用后端api 接口FORMAT，并根据后台返回的code为success或者fail来更新组织数据用于tabledata或者打印出错信息

### NavBar.vue

功能：   创建导航栏，存放其他页面的跳转url，实现导航功能

代码实现：

通过`<v-list-item v-for="(item, i) in items" :key="i">  `展开item即所有pages的属性

在`data.item`存放item数组存放每个页面的名字和网址，用于展开，提供logout()方法用于注销

## 项目测试演示

*详细内容见录制视频*  

## :key:总结和讨论

这次实验完整地实现了前后端所有内容，做到了前后端完全分离，体会到了实现数据一致性的不易，不过也在django.model层实现了复杂的子实体-父实体等一致性的保障。

在web-API设计中，增加了不同等级权限用户的区分，做到了很好的权限控制。

在前端设计中，设计了界面友好的数据操作界面，并带有分组，排序，搜索，按列搜索的功能
