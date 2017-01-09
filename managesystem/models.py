# modify the system coding ways
# coding=utf-8

from django.db import models

# Create your models here.

# 课时学生
class HoursStudent(models.Model):
    username = models.CharField(max_length=200)
    sex = models.CharField(max_length=200)
    birth_date = models.DateField()
    phone_num = models.CharField(max_length=200)
    character = models.CharField(max_length=200)
    hobbies = models.CharField(max_length=200)
    sum_hours = models.IntegerField(default=0)
    hours_already = models.IntegerField(default=0)
    hours_rest = models.IntegerField(default=0)
    register_date = models.DateField(default="2016-11-11")

    def __unicode__(self):
        return self.username

# 课时学生日常课程
class HoursDailyClass(models.Model):
    owner = models.ForeignKey(HoursStudent, null=False)
    mons_hours = models.IntegerField(default=0)
    music_hours = models.IntegerField(default=0)
    art_hours = models.IntegerField(default=0)
    english_hours = models.IntegerField(default=0)
    consume_date = models.DateField(default="2016-11-11")

    def __unicode__(self):
        return self.consume_date

# 试听学生
class TryStudent(models.Model):
    username = models.CharField(max_length=200)
    sex = models.CharField(max_length=200)
    phone_num = models.CharField(max_length=200)
    contact = models.CharField(max_length=200)
    try_class_one = models.CharField(max_length=200,null=False,default="蒙氏")
    try_class_one_state = models.CharField(max_length=200,null=False,default="未上")
    class_one_teacher = models.CharField(max_length=200)
    try_class_two = models.CharField(max_length=200, null=False, default="蒙氏")
    try_class_two_state = models.CharField(max_length=200, null=False, default="未上")
    class_two_teacher = models.CharField(max_length=200)

    register_date = models.DateField(default="2016-11-11")
    accompany_username = models.CharField(max_length=200, default="")
    try_class_one_time = models.CharField(max_length=200, default="")
    try_class_two_time = models.CharField(max_length=200, default="")
    source = models.CharField(max_length=200, default="")
    unRegister_reason = models.CharField(max_length=200, default="")
    birth_date = models.CharField(max_length=200, default="0个月")

    def __unicode__(self):
        return self.username

# 课程学生
class CourseStudent(models.Model):
    username = models.CharField(max_length=200)
    sex = models.CharField(max_length=200)
    birth_date = models.DateField()
    phone_num = models.CharField(max_length=200)
    character = models.CharField(max_length=200)
    hobbies = models.CharField(max_length=200)
    sum_hours = models.IntegerField(default=0)
    course_type = models.CharField(max_length=200)
    course_frequency = models.CharField(max_length=200)
    hours_already = models.IntegerField(default=0)
    register_date = models.DateField(default="2016-11-11")

    def __unicode__(self):
        return self.username

# 课程学生 每日课程
class CourseDailyClass(models.Model):
    owner = models.ForeignKey(CourseStudent, null=False)
    class_name = models.CharField(max_length=200,null=False,default="蒙氏")
    class_color = models.CharField(max_length=200,default="#f39c12")
    consume_date = models.DateField(default="2016-11-11")

    def __unicode__(self):
        return (self.owner.username +' '+str(self.consume_date) +' '+self.class_name)