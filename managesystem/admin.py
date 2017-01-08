from django.contrib import admin

from managesystem.models import HoursStudent, HoursDailyClass, TryStudent, CourseDailyClass

# Register your models here.
admin.site.register(HoursStudent)
admin.site.register(HoursDailyClass)
admin.site.register(TryStudent)
admin.site.register(CourseDailyClass)
