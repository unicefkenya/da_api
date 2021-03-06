from django.contrib import admin
from  oosc.attendance.models import Attendance, AttendanceHistory


class AttendaceAdmin(admin.ModelAdmin):
    list_display=['student','date','created','modified','cause_of_absence','status','_class']

admin.site.register(Attendance,AttendaceAdmin)
# Register your models here.


class AttendanceHistoryAdmin(admin.ModelAdmin):
    list_display = ["id",'present','absent','date',"_class"]

admin.site.register(AttendanceHistory,AttendanceHistoryAdmin)