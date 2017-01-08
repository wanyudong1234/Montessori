# modify the system coding ways
# coding=utf-8

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from managesystem.models import HoursStudent, HoursDailyClass, TryStudent, CourseStudent, CourseDailyClass
from managesystem.form import LoginForm

import datetime, calendar

# Create your views here.

# 常量
SEASON = u"季卡"
HALFYEAR = u"半年卡"
YEAR = u"年卡"


# 登陆
def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/homepage/')
    else:
        error = []
        username = ''
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                # get the form data
                data = form.cleaned_data
                # get the value of username
                username = data['username']
                # get the value of password
                password = data['password']
                # authenticate the user
                if login_validate(request, username, password):
                    # if succeed, jump to the welcome page
                    return HttpResponseRedirect('/homepage/')
                else:
                    # add the error message
                    error.append(u'请输入正确的密码')
            else:
                # add the error message
                error.append(u'请输入用户名和密码')
        else:
            # if request is not the POST, set the form to null
            form = LoginForm()
        # load the login page
        return render_to_response('login/login.html', {'error': error, 'form': form})


def login_validate(request, username, password):
    value = False
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            return True
    return value

# 退出登陆
#define the logout method
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')


###########################################
#                  课时                  #
###########################################

    # 注册
    # 课时学生
def HoursRegister(request):
    currentDate = str(datetime.datetime.now().date())
    if request.user.is_authenticated():
        error = ''
        if request.method == 'POST':
            hoursSudentInstance = HoursStudent()
            username = request.POST['username']
            if username != "" and username is not None :
                if not HoursStudent.objects.all().filter(username=username):
                    sex = request.POST['sex']
                    birth_date = request.POST['birth_date']
                    phone_num = request.POST['phone_num']
                    character = request.POST['character']
                    hobbies = request.POST['hobbies']
                    sum_hours = request.POST['sum_hours']
                    register_date = request.POST['register_date']

                    # 保存学生信息
                    hoursSudentInstance.username = username
                    hoursSudentInstance.sex = sex
                    hoursSudentInstance.birth_date = birth_date
                    hoursSudentInstance.phone_num = phone_num
                    hoursSudentInstance.character = character
                    hoursSudentInstance.hobbies = hobbies
                    hoursSudentInstance.sum_hours = sum_hours
                    hoursSudentInstance.hours_rest = sum_hours
                    hoursSudentInstance.register_date = register_date
                    hoursSudentInstance.save()

                    return  HttpResponseRedirect('/homepage/hoursList/')
                else:
                    error = "学生姓名已存在,请输入不同的名字"
            else:
                error = "请输入姓名"
        return render_to_response('register/hoursRegister.html',{'currentDate':currentDate,'errors':error})
    else:
        return HttpResponseRedirect('/')

# 主页
    #课时学生管理主页
def HoursHomepage(request):
    if request.user.is_authenticated():
        hoursStudentArr = HoursStudent.objects.all()
        tryStudentArr = TryStudent.objects.all()

        # 若果总条数大于七条只显示七条数据
        if len(hoursStudentArr) > 7:
            hoursStudentArr = hoursStudentArr[0:6]
        else:
            hoursStudentArr = hoursStudentArr

        # 若果总条数大于七条只显示七条数据
        if len(tryStudentArr) > 7:
            tryStudentArr = tryStudentArr[0:6]
        else:
            tryStudentArr = tryStudentArr

        return render_to_response("homepage/homepage.html",{"studentList":hoursStudentArr, "tryStudentList":tryStudentArr})
    else:
        return HttpResponseRedirect('/')


# 个人页面
    #课时个人页面
def HoursPerson(request, username):
    if request.user.is_authenticated():
        hoursStudentInstance = HoursStudent.objects.get(username = username)
        hoursDailyArr = HoursDailyClass.objects.filter(owner=hoursStudentInstance)

        hours_already = hoursStudentInstance.hours_already;
        # 计算单科课程数
        num_mons = 0
        num_music = 0
        num_art = 0
        num_english = 0
        for item in hoursDailyArr:
            num_mons = num_mons + item.mons_hours
            num_music = num_music + item.music_hours
            num_art = num_art + item.art_hours
            num_english = num_english + item.english_hours
        if request.method == "POST":
            num_mons = 0
            num_music = 0
            num_art = 0
            num_english = 0
            if "day" in request.POST:
                keywords = request.POST["day"]
                searchList = HoursDailyClass.objects.filter(owner=hoursStudentInstance, consume_date=keywords)
                num = len(searchList)
                for item in searchList:
                    num_mons = num_mons + item.mons_hours
                    num_music = num_music + item.music_hours
                    num_art = num_art + item.art_hours
                    num_english = num_english + item.english_hours
            if "month" in request.POST:
                keywords = request.POST["month"]
                arr = keywords.split('-')
                year = arr[0]
                month = arr[1]
                searchList = HoursDailyClass.objects.filter(owner=hoursStudentInstance, consume_date__year=int(year), consume_date__month=int(month))
                for item in searchList:
                    num_mons = num_mons + item.mons_hours
                    num_music = num_music + item.music_hours
                    num_art = num_art + item.art_hours
                    num_english = num_english + item.english_hours
            if "year" in request.POST:
                keywords = request.POST["year"]
                searchList = HoursDailyClass.objects.filter(owner=hoursStudentInstance, consume_date__year=int(keywords))
                for item in searchList:
                    num_mons = num_mons + item.mons_hours
                    num_music = num_music + item.music_hours
                    num_art = num_art + item.art_hours
                    num_english = num_english + item.english_hours
            return render_to_response("personal/hoursperson.html",
                                          {"username": username, "recordList": searchList,
                                           "hoursAlready": hours_already, "num_mons":num_mons, "num_music":num_music, "num_art":num_art, "num_english":num_english})

        return render_to_response("personal/hoursperson.html",{"username":username,"recordList":hoursDailyArr,"hoursAlready":hours_already, "num_mons":num_mons, "num_music":num_music, "num_art":num_art, "num_english":num_english})
    else:
        return HttpResponseRedirect('/')

# 新增课时课程
def DailyClassAdd(request, username):
    hoursStudentInstance = HoursStudent.objects.get(username=username)
    currentDate = str(datetime.datetime.now().date())
    if request.user.is_authenticated():
        if request.method == "POST":
            hoursDailyInstance = HoursDailyClass()

            mons_hours = request.POST["mons_hours"]
            if mons_hours == "" or mons_hours is None:
                mons_hours = '0'
            music_hours = request.POST["music_hours"]
            if music_hours == "" or music_hours is None:
                music_hours = '0'
            art_hours = request.POST["art_hours"]
            if art_hours == "" or art_hours is None:
                art_hours = '0'
            english_hours = request.POST["english_hours"]
            if english_hours == "" or english_hours is None:
                english_hours = '0'
            consume_date = request.POST["consume_date"]

            # 保存
            hoursDailyInstance.owner = hoursStudentInstance
            hoursDailyInstance.mons_hours = int(mons_hours)
            hoursDailyInstance.music_hours = int(music_hours)
            hoursDailyInstance.art_hours = int(art_hours)
            hoursDailyInstance.english_hours = int(english_hours)
            hoursDailyInstance.consume_date = consume_date
            hoursDailyInstance.save()

            daily_sum_hours = int(mons_hours)+int(music_hours)+int(art_hours)+int(english_hours)
            hours_rest = int(hoursStudentInstance.hours_rest) - daily_sum_hours
            hours_already = int(hoursStudentInstance.sum_hours) - hours_rest

            # 更新
            hoursStudentInstance.hours_already = hours_already
            hoursStudentInstance.hours_rest = hours_rest
            hoursStudentInstance.save()

            return HttpResponseRedirect('/homepage/hoursList/'+username)
        return render_to_response("registerDaily/hoursdailyadd.html",{"currentDate":currentDate,"username":username})
    else:
        return HttpResponseRedirect('/')

# 课时学生删除
def delete_hours_student_homepage(request,username):
    del_hours_student = HoursStudent.objects.get(username=username)
    del_hours_classes = HoursDailyClass.objects.filter(owner=del_hours_student)
    del_hours_classes.delete()
    del_hours_student.delete()
    return HttpResponseRedirect('/homepage/hoursList/')


# 课时学生日常课程删除
def delete_hours_daily(request, class_id, username):
    del_hours_class = HoursDailyClass.objects.get(id=class_id)
    hours_student = HoursStudent.objects.get(username=username)

    current_mons_hours = int(del_hours_class.mons_hours)
    current_music_hours = int(del_hours_class.music_hours)
    current_art_hours = int(del_hours_class.art_hours)
    current_english_hours = int(del_hours_class.english_hours)

    hours_rest = int(hours_student.hours_rest) + current_art_hours + current_english_hours + current_mons_hours + current_music_hours
    del_hours_class.delete()
    hours_student.hours_rest=hours_rest
    hours_student.hours_already = int(hours_student.sum_hours) - hours_rest
    hours_student.save()

    return HttpResponseRedirect('/homepage/hoursList/'+username+'/')

# 课时学生列表
def HoursStudentList(request):
    if request.user.is_authenticated():
        hoursStudentArr = HoursStudent.objects.all()
        if request.method == "POST":
            keywords = request.POST["keywords"]
            searchList = HoursStudent.objects.filter(username__contains=keywords)
            return render_to_response("homepage/hoursStudentList.html", {"studentList": searchList})
        return render_to_response("homepage/hoursStudentList.html", {"studentList": hoursStudentArr})
    else:
        return HttpResponseRedirect('/')

# 课时修改
def HoursModification(request, username):
    if request.user.is_authenticated():
        currentStudent = HoursStudent.objects.get(username=username)
        if request.method == "POST":
            sex = request.POST['sex']
            birth_date = request.POST['birth_date']
            phone_num = request.POST['phone_num']
            character = request.POST['character']
            hobbies = request.POST['hobbies']
            register_date = request.POST['register_date']

            # 保存修改
            currentStudent.sex = sex
            currentStudent.birth_date = birth_date
            currentStudent.phone_num = phone_num
            currentStudent.character = character
            currentStudent.hobbies = hobbies
            currentStudent.register_date = register_date
            currentStudent.save()
            return HttpResponseRedirect('/homepage/hoursList/')
        return render_to_response("modification/hoursModification.html",{"currentStudent":currentStudent})
    else:
        return HttpResponseRedirect('/')


###########################################
#                  试听                  #
###########################################

# 注册
    # 试听学生注册
def TryRegister(request):
    currentDate = str(datetime.datetime.now().date())
    if request.user.is_authenticated():
        error = ''
        if request.method == 'POST':
            trySudentInstance = TryStudent()
            username = request.POST['username']
            if username != "" and username is not None :
                if not HoursStudent.objects.all().filter(username=username) and not TryStudent.objects.all().filter(username=username):
                    sex = request.POST['sex']
                    phone_num = request.POST['phone_num']
                    contact = request.POST['contact']
                    class_one = request.POST['class_one']
                    classOneTeacher = request.POST['classOneTeacher']
                    hasDoneOne = request.POST['hasDoneOne']
                    class_two = request.POST['class_two']
                    hasDoneTwo = request.POST['hasDoneTwo']
                    classTwoTeacher = request.POST['classTwoTeacher']

                    # 保存学生信息
                    trySudentInstance.username = username
                    trySudentInstance.sex = sex
                    trySudentInstance.phone_num = phone_num
                    trySudentInstance.contact = contact
                    trySudentInstance.try_class_one = class_one
                    trySudentInstance.try_class_one_state = hasDoneOne
                    trySudentInstance.class_one_teacher = classOneTeacher
                    trySudentInstance.try_class_two = class_two
                    trySudentInstance.try_class_two_state = hasDoneTwo
                    trySudentInstance.class_two_teacher = classTwoTeacher
                    trySudentInstance.save()

                    return  HttpResponseRedirect('/homepage/')
                else:
                    error = "学生姓名已存在,请输入不同的名字"
            else:
                error = "请输入姓名"
        return render_to_response('register/tryRegister.html',{'currentDate':currentDate,'errors':error})
    else:
        return HttpResponseRedirect('/')

# 试听学生列表
def TryStudentList(request):
    if request.user.is_authenticated():
        tryStudentArr = TryStudent.objects.all()
        if request.method == "POST":
            keywords = request.POST["keywords"]
            searchList = TryStudent.objects.filter(username__contains=keywords)
            return render_to_response("homepage/tryStudentList.html", {"studentList": searchList})
        return render_to_response("homepage/tryStudentList.html", {"studentList": tryStudentArr})
    else:
        return HttpResponseRedirect('/')

# 试听学生删除
def delete_try_student_homepage(request,username):
    del_try_student = TryStudent.objects.get(username=username)
    del_try_student.delete()
    return HttpResponseRedirect('/homepage/tryList/')


# 试听学生修改
def TryModification(request, username):
    if request.user.is_authenticated():
        currentStudent = TryStudent.objects.get(username=username)
        if request.method == "POST":
            sex = request.POST['sex']
            phone_num = request.POST['phone_num']
            contact = request.POST['contact']
            class_one = request.POST['class_one']
            classOneTeacher = request.POST['classOneTeacher']
            hasDoneOne = request.POST['hasDoneOne']
            class_two = request.POST['class_two']
            hasDoneTwo = request.POST['hasDoneTwo']
            classTwoTeacher = request.POST['classTwoTeacher']

            # 保存修改
            currentStudent.sex = sex
            currentStudent.phone_num = phone_num
            currentStudent.contact = contact
            currentStudent.try_class_one = class_one
            currentStudent.try_class_one_state = hasDoneOne
            currentStudent.class_one_teacher = classOneTeacher
            currentStudent.try_class_two = class_two
            currentStudent.try_class_two_state = hasDoneTwo
            currentStudent.class_two_teacher = classTwoTeacher
            currentStudent.save()
            return HttpResponseRedirect('/homepage/tryList/')
        return render_to_response("modification/tryModification.html", {"currentStudent": currentStudent})
    else:
        return HttpResponseRedirect('/')


###########################################
#                  课程                  #
###########################################

# 注册
    # 课时学生
def CourseRegister(request, flag):
    currentDate = str(datetime.datetime.now().date())
    if request.user.is_authenticated():
        error = ''
        if request.method == 'POST':
            courseSudentInstance = CourseStudent()
            username = request.POST['username']
            if username != "" and username is not None :
                if not HoursStudent.objects.all().filter(username=username) and not TryStudent.objects.all().filter(username=username) \
                        and not CourseStudent.objects.filter(username=username):
                    sex = request.POST['sex']
                    birth_date = request.POST['birth_date']
                    phone_num = request.POST['phone_num']
                    character = request.POST['character']
                    hobbies = request.POST['hobbies']
                    sum_hours = request.POST['sum_hours']
                    course_type = request.POST['course_type']
                    course_frequency = request.POST['course_frequency']
                    register_date = request.POST['register_date']

                    # 保存学生信息
                    courseSudentInstance.username = username
                    courseSudentInstance.sex = sex
                    courseSudentInstance.birth_date = birth_date
                    courseSudentInstance.phone_num = phone_num
                    courseSudentInstance.character = character
                    courseSudentInstance.hobbies = hobbies
                    courseSudentInstance.sum_hours = sum_hours
                    courseSudentInstance.course_type = course_type
                    courseSudentInstance.course_frequency = course_frequency
                    courseSudentInstance.register_date = register_date
                    courseSudentInstance.save()

                    return  HttpResponseRedirect('/homepage/courseList/'+flag)
                else:
                    error = "学生姓名已存在,请输入不同的名字"
            else:
                error = "请输入姓名"
        return render_to_response('register/seasonRegister.html',{'currentDate':currentDate,'errors':error,'flag':flag})
    else:
        return HttpResponseRedirect('/')

def CourseHomepage(request, flag):
    if request.user.is_authenticated():
        courseStudentArr = CourseStudent.objects.filter(course_type=flag)

        if request.method == "POST":
            keywords = request.POST["keywords"]
            searchList = CourseStudent.objects.filter(username__contains=keywords, course_type=flag)
            return render_to_response("homepage/courseStudentList.html",
                                      {'studentList': searchList, 'flag': flag})
        return render_to_response("homepage/courseStudentList.html",{'studentList':courseStudentArr, 'flag':flag})
    else:
        return HttpResponseRedirect('/')


# 课程 学生上课日历表
def CourseStudentCalender(request, flag, username):
    if request.user.is_authenticated():
        courseStudentInstance = CourseStudent.objects.get(username=username)
        courseDailyList = CourseDailyClass.objects.filter(owner=courseStudentInstance)
        hours_already = len(courseDailyList)
        return render_to_response("personal/courseperson.html",{"courseList":courseDailyList,"flag":flag,"username":username,"student":courseStudentInstance,"already":hours_already})
    else:
        return HttpResponseRedirect('/')

# 课程 学生上课列表
def CourseStudentList(request, flag, username):
    if request.user.is_authenticated():
        courseStudentInstance = CourseStudent.objects.get(username=username)
        courseDailyList = CourseDailyClass.objects.filter(owner=courseStudentInstance)
        # 计算蒙氏课程数
        num_mons =len(CourseDailyClass.objects.filter(owner=courseStudentInstance, class_name="蒙氏"))
        num_music = len(CourseDailyClass.objects.filter(owner=courseStudentInstance, class_name="音乐"))
        num_art = len(CourseDailyClass.objects.filter(owner=courseStudentInstance, class_name="艺术"))
        num_english = len(CourseDailyClass.objects.filter(owner=courseStudentInstance, class_name="英语"))
        if request.method == "POST":
            couse_name = ""
            if "day" in request.POST:
                keywords = request.POST["day"]
                searchList = CourseDailyClass.objects.filter(owner=courseStudentInstance, consume_date=keywords)
                num_mons = len(CourseDailyClass.objects.filter(owner=courseStudentInstance, consume_date=keywords, class_name="蒙氏"))
                num_music = len(CourseDailyClass.objects.filter(owner=courseStudentInstance, consume_date=keywords, class_name="音乐"))
                num_art = len(CourseDailyClass.objects.filter(owner=courseStudentInstance, consume_date=keywords, class_name="艺术"))
                num_english = len(CourseDailyClass.objects.filter(owner=courseStudentInstance, consume_date=keywords, class_name="英语"))
            if "month" in request.POST:
                keywords = request.POST["month"]
                arr = keywords.split('-')
                year = arr[0]
                month = arr[1]
                searchList = CourseDailyClass.objects.filter(owner=courseStudentInstance, consume_date__year=int(year), consume_date__month=int(month))
                num_mons = len(CourseDailyClass.objects.filter(owner=courseStudentInstance, consume_date__year=int(year), consume_date__month=int(month),
                                                               class_name="蒙氏"))
                num_music = len(CourseDailyClass.objects.filter(owner=courseStudentInstance, consume_date__year=int(year), consume_date__month=int(month),
                                                                class_name="音乐"))
                num_art = len(CourseDailyClass.objects.filter(owner=courseStudentInstance, consume_date__year=int(year), consume_date__month=int(month),
                                                              class_name="艺术"))
                num_english = len(CourseDailyClass.objects.filter(owner=courseStudentInstance, consume_date__year=int(year), consume_date__month=int(month),
                                                                  class_name="英语"))
            if "year" in request.POST:
                keywords = request.POST["year"]
                searchList = CourseDailyClass.objects.filter(owner=courseStudentInstance, consume_date__year=int(keywords))
                num_mons = len(CourseDailyClass.objects.filter(owner=courseStudentInstance, consume_date__year=int(keywords),
                                                               class_name="蒙氏"))
                num_music = len(CourseDailyClass.objects.filter(owner=courseStudentInstance, consume_date__year=int(keywords),
                                                                class_name="音乐"))
                num_art = len(CourseDailyClass.objects.filter(owner=courseStudentInstance, consume_date__year=int(keywords),
                                                              class_name="艺术"))
                num_english = len(CourseDailyClass.objects.filter(owner=courseStudentInstance, consume_date__year=int(keywords),
                                                                  class_name="英语"))

            return render_to_response("homepage/courseRecordList.html",
                                      {"courseList": searchList, "flag": flag, "username": username, "num_mons":num_mons, "num_music":num_music, "num_art":num_art, "num_english":num_english})
        return render_to_response("homepage/courseRecordList.html",
                                      {"courseList": courseDailyList, "flag": flag, "username": username, "num_mons":num_mons, "num_music":num_music, "num_art":num_art, "num_english":num_english})
    else:
        return HttpResponseRedirect('/')


# 课程 新增日常课程
def DailyCourseAdd(request, flag, username):
    courseStudentInstance = CourseStudent.objects.get(username=username)
    currentDate = str(datetime.datetime.now().date())
    if request.user.is_authenticated():
        if request.method == "POST":
            consume_date = request.POST["consume_date"]
            if "mons" in request.POST:
                isMons = request.POST["mons"]
                saveCourseDaily(courseStudentInstance, "蒙氏", "#f39c12", consume_date) # 黄色
            if "music" in request.POST:
                isMusic = request.POST["music"]
                saveCourseDaily(courseStudentInstance, "音乐", "#f56954", consume_date) # 红色
            if "art" in request.POST:
                isArt = request.POST["art"]
                saveCourseDaily(courseStudentInstance, "艺术", "#00a65a", consume_date) # 绿色
            if "english" in request.POST:
                isEnglish = request.POST["english"]
                saveCourseDaily(courseStudentInstance, "英语", "#3c8dbc", consume_date) # 蓝色

            return HttpResponseRedirect('/homepage/courseList/'+flag+'/'+username)

        return render_to_response("registerDaily/coursedailyadd.html",{"currentDate":currentDate,"username":username,"flag":flag})
    else:
        return HttpResponseRedirect('/')

def saveCourseDaily(owner, courseName, color, consume_date):
    courseDailyInstance = CourseDailyClass()

    # 保存课程
    courseDailyInstance.owner = owner
    courseDailyInstance.class_name = courseName
    courseDailyInstance.class_color = color
    courseDailyInstance.consume_date = consume_date
    courseDailyInstance.save()

# 课程 日常课程删除
def delete_course_daily(request, class_id, username, flag):
    del_course_daily = CourseDailyClass.objects.get(id=class_id)
    del_course_daily.delete()

    return HttpResponseRedirect('/homepage/courseList/'+flag+'/'+username+'/recordlist')

# 课程 学生信息修改
def CourseModification(request, flag, username):
    if request.user.is_authenticated():
        courseSudentInstance = CourseStudent.objects.get(username=username)
        if request.method == 'POST':
            sex = request.POST['sex']
            birth_date = request.POST['birth_date']
            phone_num = request.POST['phone_num']
            character = request.POST['character']
            hobbies = request.POST['hobbies']
            sum_hours = request.POST['sum_hours']
            course_type = request.POST['course_type']
            course_frequency = request.POST['course_frequency']
            register_date = request.POST['register_date']

            # 保存学生信息
            courseSudentInstance.sex = sex
            courseSudentInstance.birth_date = birth_date
            courseSudentInstance.phone_num = phone_num
            courseSudentInstance.character = character
            courseSudentInstance.hobbies = hobbies
            courseSudentInstance.sum_hours = sum_hours
            courseSudentInstance.course_type = course_type
            courseSudentInstance.course_frequency = course_frequency
            courseSudentInstance.register_date = register_date
            courseSudentInstance.save()
            return HttpResponseRedirect("/homepage/courseList/"+course_type)
        return render_to_response("modification/courseModification.html", {"currentStudent":courseSudentInstance, "flag":flag})
    else:
        return HttpResponseRedirect('/')

# 课程 学生删除
def delete_course_student_homepage(request, flag, username):
    del_course_student = CourseStudent.objects.get(username=username)
    del_course_daily = CourseDailyClass.objects.filter(owner=del_course_student)

    del_course_student.delete()
    del_course_daily.delete()
    return HttpResponseRedirect("/homepage/courseList/"+flag)