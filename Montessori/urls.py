# modify the system coding ways
# coding=utf-8

"""Montessori URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from managesystem.views import login, logout, HoursHomepage, HoursRegister, HoursStudentList, HoursPerson, \
    DailyClassAdd, delete_hours_student_homepage, delete_hours_daily, HoursModification, TryRegister, TryStudentList, \
    delete_try_student_homepage, TryModification, CourseRegister, CourseHomepage, CourseStudentCalender, DailyCourseAdd, CourseStudentList, \
    delete_course_daily, CourseModification, delete_course_student_homepage

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    # 登录页面
    url(r'^$', login),

    # 主页
    url(r'^homepage/$', HoursHomepage),

    # 退出登录页面
    url(r'^logout/', logout),

    # 注册
    url(r'^hoursRegister/', HoursRegister),
    url(r'^tryRegister/', TryRegister),
    # 注册 课程
    url(r'^CourseRegister/(?P<flag>\w+)',CourseRegister),

    # 课时 学生列表
    url(r'^homepage/hoursList/$',HoursStudentList),
    # 课时 个人页面
    url(r'^homepage/hoursList/(?P<username>\w+)/$', HoursPerson),
    # 课时 个人页面 新增
    url(r'^homepage/hoursList/(?P<username>\w+)/dailyclassadd$', DailyClassAdd),
    # 课时 个人信息修改
    url(r'^hoursModification/(?P<username>\w+)$', HoursModification),
    # 删除 课时 学生
    url(r'^deleteHoursStudentHomepage/(?P<username>\w+)$',delete_hours_student_homepage),
    # 删除 课时 学生 日常课程
    url(r'^homepage/hoursList/(?P<username>\w+)/(?P<class_id>\d+)$',delete_hours_daily),

    # 试听 学生列表
    url(r'^homepage/tryList/$',TryStudentList),
    # 删除 试听 学生
    url(r'^deleteTryStudentHomepage/(?P<username>\w+)$',delete_try_student_homepage),
    # 试听 修改
    url(r'^tryModification/(?P<username>\w+)$', TryModification),

    # 课程 学生列表
    url(r'^homepage/courseList/(?P<flag>\w+)/$', CourseHomepage),
    # 课程 学生 课程日历
    url(r'^homepage/courseList/(?P<flag>\w+)/(?P<username>\w+)$', CourseStudentCalender),
    # 课程 学生 课程列表
    url(r'^homepage/courseList/(?P<flag>\w+)/(?P<username>\w+)/recordlist$', CourseStudentList),
    # 课程 学生 日常课程 新增
    url(r'^homepage/courseList/(?P<flag>\w+)/(?P<username>\w+)/dailycourseadd$', DailyCourseAdd),
    # 删除 课时 学生 日常课程
    url(r'^homepage/courseList/(?P<flag>\w+)/(?P<username>\w+)/recordlist/(?P<class_id>\d+)$', delete_course_daily),
    # 课程 个人信息修改
    url(r'^courseModification/(?P<flag>\w+)/(?P<username>\w+)$', CourseModification),
    # 删除 课时 学生
    url(r'^deleteCourseStudentHomepage/(?P<flag>\w+)/(?P<username>\w+)$',delete_course_student_homepage),

]
