
"""oosc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from oosc.attendance.views import ListCreateAttendance,TakeAttendance,WeeklyAttendanceReport,ListAbsentees
from oosc.schools.views import ListCreateSchool,ImportSchools,GetAllReport,SearchEmiscode
from oosc.constituencies.views import ListCreateCounstituency
from oosc.counties.views import ListCreateCounty
from oosc.stream.views import ListCreateClass
from oosc.teachers.views import RetrieveUpdateTeacher,ListCreateTeachers,ListTeachers,ChangePassword,ForgotPasssword, \
    GetUserType, PingServer
from oosc.students.views import ListCreateStudent,GetEnrolled,ImportStudents,RetrieveUpdateStudent, ListAbsentStudents, \
    ListDropouts
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from oosc.absence.views import GetEditAbsence
from oosc.reason.views import ListCreatereason
from oosc.partner.views import ListCreatePartner

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/attendance/weekly',WeeklyAttendanceReport.as_view(),name="weekly_attendance_report"),
    url(r'^api/attendances/(?P<type>.+)',ListCreateAttendance.as_view(),name="attendance-list-create"),
    url(r'^api/attendance',TakeAttendance.as_view(),name="take_attendance"),
    url(r'^api/absentees',ListAbsentees.as_view(),name="list_absentees_for_the_pastweek"),
    url(r'^api/absent/(?P<pk>[0-9]+)',GetEditAbsence.as_view(),name="Update_absent"),
    url(r'^api/reasons',ListCreatereason.as_view(),name="list_create_reason"),
    url(r'^api/change-password',ChangePassword.as_view(),name="change_password"),
    url(r'^api/forgot-password',ForgotPasssword.as_view(),name="Forgot-password"),
    url(r'^api/schools/import',ImportSchools.as_view(),name="import_schools"),
    url(r'^api/schools/(?P<emiscode>.+)',SearchEmiscode.as_view(),name="import_schools"),
    url(r'^api/school',ListCreateSchool.as_view(),name="school-list-create"),
    url(r'^api/counties',ListCreateCounty.as_view(),name="county-list-create"),
    url(r'^api/zones',ListCreateCounstituency.as_view(),name="zones-list-create"),
    url(r'^api/streams',ListCreateClass.as_view(),name="class-list-create"),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^api/students/enrolls/(?P<type>.+)',GetEnrolled.as_view(),name="list-create-student"),
    url(r'^api/students/import',ImportStudents.as_view(),name="import-student"),
    url(r'^api/students/absent',ListAbsentStudents.as_view(),name="import-student"),
    url(r'^api/students/dropouts',ListDropouts.as_view(),name="import-student"),
    url(r'^api/students/(?P<pk>[0-9]+)',RetrieveUpdateStudent.as_view(),name="list-create-student"),
    url(r'^api/students',ListCreateStudent.as_view(),name="list-create-student"),
    url(r'^api/teacher$',ListCreateTeachers.as_view(),name="List-create-teachers"),
    url(r'^api/teachers/(?P<pk>[0-9]+)',RetrieveUpdateTeacher.as_view(),name="Retrieve_update_delete_Teachers"),
    url(r'^api/teachers',ListTeachers.as_view(),name="List_Teachers"),
    url(r'^api/partners',ListCreatePartner.as_view(),name="List_create_partner"),
    url(r'^api/user-type',GetUserType.as_view(),name="get_singed_in_user_type"),
    url(r'^api/ping$',PingServer.as_view(),name="ping_test_for_server"),
    url('^api/statistics',GetAllReport.as_view(),name="all_students_teacgers-schools_number"),

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
