from django.contrib.auth.models import User,Group
from django.db import transaction
from django.shortcuts import render

from oosc.attendance.views import AbsenteesFilter, AttendanceFilter
from oosc.students.models import Students,ImportError,ImportResults
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.views import APIView
from oosc.students.serializers import StudentsSerializer,ImportErrorSerializer,ImportResultsSerializer
from datetime import datetime,timedelta
from django_filters.rest_framework import FilterSet,DjangoFilterBackend
import django_filters
import csv
from oosc.students.permissions import IsTeacherOrAdmin, IsTeacherOrPartner
from rest_framework import serializers
import json
from oosc.stream.models import Stream
from oosc.schools.models import Schools
from oosc.teachers.models import Teachers
from datetime import datetime
from django.db.models import Count,Case,When,IntegerField,Q,Value,CharField,TextField,F
from django.db.models.functions import ExtractMonth,ExtractYear,ExtractDay,TruncDate
from django.db.models.functions import Concat,Cast
from rest_framework.response import Response
from rest_framework import status
from oosc.history.models import History
from oosc.attendance.models import Attendance
from rest_framework.pagination import PageNumberPagination
# Create your views here.
from oosc.partner.models import Partner
from sys import stdout


class StudentFilter(FilterSet):
    name = django_filters.CharFilter(name="student__name", method="filter_name")
    Class=django_filters.NumberFilter(name="class_id")
    school=django_filters.NumberFilter(name="class_id__school")
    school_emis_code=django_filters.NumberFilter(name="class_id__school__emis_code")
    partner=django_filters.NumberFilter(name="partner",method="filter_partner")
    county=django_filters.NumberFilter(name="class_id__school__zone__subcounty__county")


    class Meta:
        model=Students
        fields=('name','fstname','midname','lstname','admission_no','partner','gender','school','school_emis_code','county','is_oosc')
    def filter_name(self,queryset,name,value):
        return queryset.filter(Q(fstname__icontains=value) | Q(lstname__icontains=value)| Q(midname__icontains=value))

    def filter_partner(self, queryset, name, value):
        return queryset.filter(class_id__school__partners__id=value)


class StandardresultPagination(PageNumberPagination):
    page_size = 100
    max_page_size = 1000
    page_size_query_param = 'page_size'

class ListCreateStudent(generics.ListCreateAPIView):
    queryset=Students.objects.select_related("class_id","class_id__school")
    serializer_class=StudentsSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class=StudentFilter
    pagination_class = StandardresultPagination

    def perform_create(self, serializer):
        #obj=self.get_object()
        stud=serializer.save()
        hist=History()
        hist.student=stud
        hist._class=stud.class_id
        hist.joined=stud.date_enrolled
        if stud.not_in_school_before:
            hist.joined_description="Not in School Before"
        else:
            hist.joined_description="In school before"
        hist.save()


class DeleteSerializer(serializers.Serializer):
    reason=serializers.CharField(max_length=20,required=True)

class RetrieveUpdateStudent(generics.RetrieveUpdateDestroyAPIView):
    queryset=Students.objects.all()
    serializer_class=StudentsSerializer

    def get_serializer_class(self):
        if self.request.method=="DELETE":
            return DeleteSerializer
        return StudentsSerializer


    def perform_update(self, serializer):
        obj=self.get_object()
        if obj.class_id !=serializer.validated_data.get("class_id"):
            stud=obj
            hist = History()
            hist.student = stud
            hist._class = serializer.validated_data.get("class_id")
            hist.joined = stud.date_enrolled
            hist.joined_description="Class Change"
            hist.save()
            serializer.save(previous_class=obj.class_id_id)
        else:
            serializer.save()



    def delete(self, request, *args, **kwargs):
        params=self.request.query_params
        ser=DeleteSerializer(data=params)
        if not ser.is_valid():
            return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)
        object=self.get_object()
        if(ser.data["reason"].lower() == "error"):
            object.delete()
            return Response("",status=status.HTTP_204_NO_CONTENT);
        object.active=False
        object.save()
        hist=History.objects.filter(student=object,_class=object.class_id)
        if(hist.exists()):
            hist=hist[0]
            hist.left=datetime.now()
            hist.left_description=ser.data["reason"]

        else:
            stud=object
            hist=History()
            hist.student = stud
            hist._class = stud.class_id
            hist.left = datetime.now()
            hist.left_description=ser.data["reason"]
            hist.save()
        return Response("",status=status.HTTP_204_NO_CONTENT)


class EnrollmentFilter(FilterSet):
    school = django_filters.NumberFilter(name="class_id__school", )
    start_date = django_filters.DateFilter(name='date_enrolled', lookup_expr=('gte'))
    end_date = django_filters.DateFilter(name='date_enrolled', lookup_expr=('lte'))
    year=django_filters.NumberFilter(name="date_enrolled",lookup_expr=('year'))

    class Meta:
        model=Students
        fields=['class_id','gender','school','start_date','end_date','year']


class EnrollmentSerializer(serializers.Serializer):
    enrolled_males=serializers.IntegerField()
    enrolled_females=serializers.IntegerField()
    old_males=serializers.IntegerField()
    old_females=serializers.IntegerField()
    value=serializers.CharField()
    total=serializers.SerializerMethodField()
    def get_total(self,obj):
        return obj["enrolled_males"]+obj["enrolled_females"]+obj["old_males"]+obj["old_females"]
    def to_representation(self, instance):
        data = super(EnrollmentSerializer, self).to_representation(instance)
        return data

class GetEnrolled(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    queryset = Students.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = EnrollmentFilter

    def get_queryset(self):
        studs=self.filter_queryset(Students.objects.filter(active=True))
        format = self.kwargs['type']
        at=self.get_formated_data(studs,format=format)
        return at

    def resp_fields(self):
        #lst = str(datetime.now().date() - timedelta(days=365))
        #enrolledm = Count(Case(When(Q(date_enrolled__gte=lst) & Q(gender="M"), then=1), output_field=IntegerField(), ))
        enrolledm = Count(Case(When(Q(is_oosc=True) & Q(gender="M"), then=1), output_field=IntegerField(), ))
        oldf = Count(Case(When(Q(gender="F") & Q(is_oosc=False), then=1), output_field=IntegerField(), ))
        enrolledf = Count(Case(When(Q(gender="F") & Q(is_oosc=True), then=1), output_field=IntegerField(), ))
        oldm = Count(Case(When(Q(gender="M") & Q(is_oosc=False), then=1), output_field=IntegerField(), ))
        return enrolledm,oldf,enrolledf,oldm
    # def get(self,request,format=None):
    #     now=str(datetime.now().date()+timedelta(days=1))
    #     lst=str(datetime.now().date()-timedelta(days=365))
    #     studs=Students.objects.filter(date_enrolled__range=[lst,now])
    #
    #     females=studs.filter(gender='F')
    #     males=studs.filter(gender='M')
    #     return Response({"total":len(studs),"males":len(males),
    #                      "females":len(females)},status=status.HTTP_200_OK)
    def get_formated_data(self, data, format):
        enrolledm, oldf, enrolledf, oldm = self.resp_fields()
        outp = Concat("month", Value(''), output_field=CharField())
        at = data.annotate(month=self.get_format(format=format)).values("month").annotate(enrolled_males=enrolledm,
                                                                                          enrolled_females=enrolledf,
                                                                                          old_males=oldm,
                                                                                          old_females=oldf, value=outp).order_by('value')
        return at

    def get_format(self,format):
        daily=Concat(TruncDate("date_enrolled"),Value(''),output_field=CharField(),)
        monthly= Concat(Value('1/'), ExtractMonth('date_enrolled'), Value('/'), ExtractYear("date_enrolled"),
                      output_field=CharField(), )

        if(format=="monthly"):
            return monthly
        elif format=="daily":
            return daily
        elif format== "yearly":
            return ExtractYear('date_enrolled')
        elif format=="gender":
            return Concat(Value("gender"),Value(""),output_field=CharField())
        elif format=="school":
            id=Cast("class_id__school_id",output_field=TextField())
            return Concat("class_id__school__school_name",Value(','),id,output_field=CharField())
        elif format=="stream":
            return Concat("class_id__class_name",Value(''),output_field=CharField())
        elif format=="county":
            return Concat("class_id__school__zone__subcounty__county__county_name",Value(''),output_field=CharField())
        elif format=="class":
            id=Cast("class_id", output_field=TextField())
            return Concat("class_id___class",Value(''),output_field=CharField())
        else:
            return monthly

def get_class(s):
    s=list(s)
    theclass=""
    for d in s:
        if d.isdigit():
            theclass=d
            break
    return str(theclass)

class ImportStudentSerializer(serializers.Serializer):
    fstname=serializers.CharField(max_length=50)
    midname=serializers.CharField(max_length=50,required=False,allow_null=True,allow_blank=True)
    lstname=serializers.CharField(max_length=50,required=False,allow_null=True,allow_blank=True)
    school=serializers.IntegerField()
    clas=serializers.CharField(max_length=50)
    gender=serializers.CharField(max_length=20)
    #date_enrolled=serializers.DateField(required=False,allow_null=True)
    # emis_code=serializers.IntegerField(required=False,allow_null=True)
    def validate_gender(self,value):
        allowed_gender_values=['m','f','female','male']
        if value.lower() not in allowed_gender_values:
            raise serializers.ValidationError("Wrong gender format")
        return value

    def validate_clas(self,value):
        cl=get_class(value)
        if cl=="":
            raise serializers.ValidationError("Only students between class 1 and 8")
        return value








def next_class(s):
    s=s.split(' ')[1]
    if s=="ECD":
        return "Std 1"
    return "Std "+str(int(s)+1)

def get_stream(s):
    d=list(s)
    theclass=get_class(s)
    d.pop(d.index(theclass))
    return ''.join(d)

def get_gender(s):
    if s.lower() =="male" or s.lower() == 'm':
        return "M"
    elif s.lower()=='female' or s.lower() == 'f':
        return "F"

def valid_date(date_text):
    try:
        datetime.strptime(date_text,'%Y-%m-%d')
        return True
    except ValueError:
        return False

def create_user(username):
    users=User.objects.filter(username=username)
    if not users.exists():
        user = User.objects.create_user(username=username, password="admin")
        g,created = Group.objects.get_or_create(name="teachers")
        #print (g,created)
        g.user_set.add(user)
        return user
    return users[0]

class ImportStudents(APIView):
    permission_classes = (IsTeacherOrPartner,)
    def post(self,request,format=None):
        #File with students details
        file=request.FILES["file"]
        #Convert each row into array
        data = [row for row in csv.reader(file.read().splitlines())]
        d=""
        s=0
        rowindex=[]
        err=""
        the_data=data[1:]
        with transaction.atomic():
            thelen=len(the_data)
            for i,dat in enumerate(the_data):
                print (i)
                #print (str((float(i)/float(thelen))*100)+" %")
                dt={"fstname":dat[6],"midname":dat[7],"lstname":dat[8], "school":dat[5],
                    "clas":dat[13],"gender":dat[11]}
                ser=ImportStudentSerializer(data=dt)
                is_partner = Group.objects.get(name="partners").user_set.filter(id=request.user.id).exists()
                partner = None
                if is_partner:
                    partner = Partner.objects.filter(user=request.user)[0]
                school_name=dat[4]
                if ser.is_valid():
                    sch=Schools.objects.filter(emis_code=ser.data.get("school"))
                    teach=Teachers()
                    if(sch.exists()):
                        sch=sch[0]
                        if partner:
                            if not partner in sch.partners.all():
                                sch.partners.add(partner)
                        teach = Teachers.objects.filter(school=sch)
                        if(not teach.exists()):
                            #print ("No teacher")
                            user=create_user(sch.emis_code)
                            teacher=Teachers()
                            teacher.user=user
                            teacher.headteacher=True
                            teacher.active=True
                            teacher.fstname="Admin"
                            teacher.lstname=sch.school_name.split(' ')[0]
                            teacher.teacher_type="TSC"
                            teacher.gender="M"
                            teacher.school=sch
                            teacher.phone_no="99999999999"
                            teach =teacher.save()
                            #print (teach)
                            #return Response("Create atleast one Teacher for the school")
                        else:
                            teachs=teach.filter(headteacher=True)
                            if not teachs.exists():
                                teach=teach[0]
                            else:
                                teach=teachs[0]
                    else:
                        print ("Create "+school_name +" First")
                        continue
                        #return Response("Create School First")
                    nxt_class=ser.data.get("clas")
                    theclass=get_class(nxt_class)
                    ##Confirm a class has been entered
                    #print ("Class "+theclass)
                    if theclass is None:
                        continue
                    if not nxt_class == "Std 9":
                        cls=Stream.objects.filter(class_name=nxt_class,school=sch)
                        cl = Stream()
                        if not (cls.exists()):
                            cl.class_name=nxt_class
                            cl._class_id=theclass
                            cl.school=sch
                            cl.teacher=teach
                            cl=cl.save()
                        else:
                            cl = cls[0]
                        if(cl is None):
                            continue
                        std=Students.objects.filter(fstname=ser.data.get("fstname"),lstname=ser.data.get("lstname"),midname=ser.data.get("midname"),
                                                    class_id=cl)

                        #check if student Exists
                        if(std.exists()):
                            #print "Found"
                            pass
                        else:
                            std=Students()
                            std.fstname=ser.data.get("fstname")
                            std.midname=ser.data.get("midname")
                            std.lstname=ser.data.get("lstname")
                            std.gender=get_gender(ser.data.get("gender"))
                            std.class_id=cl
                            if(valid_date(dat[2])):
                                std.date_enrolled=dat[2]
                                lst = str(datetime.now().date() - timedelta(days=35))
                                if(std.date_enrolled>lst):
                                    std.is_oosc=True
                                else:
                                    std.is_oosc=False
                            else:
                                std.date_enrolled=datetime.now()
                                std.is_oosc=True
                            print(std.class_id)
                            std.save()
                            s += 1

                    else:
                        print("Done Kcpe")
                else:

                    err=ser.errors
                    print(err)
                # schl=dat[5]
                # clas=dat[6]
                # if  clas and schl:
                #     pass
                # else:
                #     print dat
                #     return Response("Make Sure The Data is correct "+str(i)+" "+dat[6])
                # s=i
                # d=dat[4]
            f=s
            s=int((float(s)/float(len(the_data)))*100)
            rowindex.append({"name":"Import Summary","index":str(s)+"%, "+str(f)+" of  "+str(len(the_data))})
            rowindex.append({"name":"Errors","index":err})
            for i,dat in enumerate(data[0]):
                rw={'name':dat,'index':i}
                rowindex.append(rw)
            return Response(data=json.loads(json.dumps(rowindex)))

class AbsentStudentSerializer(serializers.Serializer):
    student_id=serializers.IntegerField(required=False)
    absent_count=serializers.IntegerField(required=False)
    name=serializers.CharField(required=False)
    school_name=serializers.CharField(required=False)
    class_name=serializers.CharField(required=False)
    class_id=serializers.IntegerField(required=False)
    guardian_phone=serializers.CharField(required=False)
    guardian_name=serializers.CharField(required=False)
    gender=serializers.CharField(required=False)
    present_count=serializers.IntegerField(required=False)


class ImportStudentsV2(APIView):
    total_success = 0
    total_fails = 0
    def post(self,request,format=None):
        file=""
        results=""
        verify=request.query_params.get('verify',None)
        try:
            file = request.FILES["file"]
        except:
            Response("No .csv file sent", status=status.HTTP_400_BAD_REQUEST)
        data=""
        # Convert each row into array and ignore the header row
        if file:
            data = [row for row in csv.reader(file.read().splitlines())][1:]

        if (verify):
            if verify=="update_oosc":
                results=self.update_oosc_status(data)
            else:
                results=self.verify_data(data)
        else:
            results=self.import_data(data,request)

        return Response(results)

    def update_oosc_status(self,data):
        total_success = 0
        total_fails = 0
        errors = []
        students=[]
        print(len(data))
        for i ,dat in enumerate(data):
            stdout.write("\rImporting  %d" % i)
            dt = {"fstname": dat[6], "midname": dat[7], "lstname": dat[8], "school": dat[5],
                  "clas": dat[13], "gender": dat[11]}
            ser = ImportStudentSerializer(data=dt)
            if ser.is_valid():
                school = Schools.objects.filter(emis_code=ser.validated_data.get("school"))[0]
                if not school:
                    print ("No school")
                    continue
                cl = self.get_class(school, ser.validated_data.get("clas"))
                if not cl:
                    print ("No sclass")
                    continue
                std = Students.objects.filter(fstname=ser.data.get("fstname"), lstname=ser.data.get("lstname"),
                                              midname=ser.data.get("midname"),
                                              class_id=cl)[0]
                if(std):
                    students.append(std.id)
                    total_success+=1
                else:
                    stdout.write("\rNo student  ")
                    total_fails+=1

            else:
                total_fails+=1
            stdout.flush()
        print ""
        total_success=Students.objects.filter(id__in=students).update(is_oosc=True)
        res = ImportResults(ImportErrorSerializer(errors, many=True).data, total_success, total_fails)
        return ImportResultsSerializer(res).data





    def verify_data(self,data):
        results="verified results"
        total_success=0
        total_fails=0
        errors=[]
        schools_not_created=[]
        total = len(data)
        with transaction.atomic():
            for i, dat in enumerate(data):
                if (total is not 0):
                    percentage=str(int(i / float(total) * 100))+"%"
                    stdout.write("\rVerifying %s " % percentage)
                    stdout.flush()
                dt = {"fstname": dat[6], "midname": dat[7], "lstname": dat[8], "school": dat[5],
                      "clas": dat[13], "gender": dat[11]}
                ser = ImportStudentSerializer(data=dt)
                if(ser.is_valid()):
                    ##Confirm the school in the db
                    school=Schools.objects.filter(emis_code=ser.validated_data.get("school"))
                    if(school):
                        total_success = total_success + 1
                    else:
                        total_fails += 1
                        error = ImportError(i + 2, "Create school first", json.dumps(dt))
                        # errors.append(error)
                        # continue
                        if ser.validated_data.get("school") not in schools_not_created:
                            errors.append(error)
                            schools_not_created.append(ser.validated_data.get("school"))
                        # if ser.validated_data.get("school") not in schools_not_created:
                        #     errors.append(error)
                        #     schools_not_created.append(ser.validated_data.get("school"))
                else:
                    total_fails=total_fails+1
                    #Adding 2 to row error due to header plus header is removed
                    error=ImportError(i+2,ser.errors,json.dumps(dt))
                    errors.append(error)
            #Print a new line
            print("")
        res=ImportResults(ImportErrorSerializer(errors,many=True).data,total_success,total_fails)
        return ImportResultsSerializer(res).data
    def import_data(self,data,request):
        results="Imported results"
        errors = []
        school=""
        schools_not_created = []
        students=[]
        total=len(data)
        is_partner = Group.objects.get(name="partners").user_set.filter(id=request.user.id).exists()
        partner = None
        if is_partner:
            partner = Partner.objects.filter(user=request.user)[0]
        print ("%d" %total)
        for i, dat in enumerate(data):
            if (total is not 0):
                percentage = str(int(i+1 / float(total) * 100)) + "%"
                stdout.write("\rImporting %s " % percentage)
                stdout.flush()
            dt = {"fstname": dat[6], "midname": dat[7], "lstname": dat[8], "school": dat[5],
                  "clas": dat[13], "gender": dat[11]}
            ser = ImportStudentSerializer(data=dt)
            if (ser.is_valid()):
                ##Confirm the school in the db

                school = Schools.objects.filter(emis_code=ser.validated_data.get("school"))
                if (school.exists()):
                    try:
                        school=school[0]
                        if partner:
                            if not partner in school.partners.all():
                                school.partners.add(partner)
                        ##Confirm a teacher is present for login
                        teach =self.get_school_teacher(school)
                        clas=self.get_class(school,ser.validated_data.get("clas"))
                        student=self.create_student(clas,ser,dat[2])
                        if student is not None:
                            students.append(student)

                    except Exception as e:
                        self.total_fails += 1
                        error=ImportError(i + 2, e.message, json.dumps(dt))
                        errors.append(error)
                else:
                    self.total_fails += 1
                    error = ImportError(i + 2, "Create school first", json.dumps(dt))
                    #errors.append(error)
                    #continue
                    if ser.validated_data.get("school") not in schools_not_created:
                        errors.append(error)
                        schools_not_created.append(ser.validated_data.get("school"))
            else:
                self.total_fails += 1
                # Adding 2 to row error due to header plus header is removed
                error = ImportError(i + 2, ser.errors, json.dumps(dt))
                errors.append(error)
        try:
            resa = Students.objects.bulk_create(students)
            self.total_success=len(resa)
        except Exception as e:
            print (e.message)
        res = ImportResults(ImportErrorSerializer(errors, many=True).data, self.total_success , self.total_fails)
        return ImportResultsSerializer(res).data

    def get_school_teacher(self,sch):
        teach=Teachers.objects.filter(school=sch)
        if (not teach.exists()):
            # print ("No teacher")
            user = create_user(sch.emis_code)
            teacher = Teachers()
            teacher.user = user
            teacher.headteacher = True
            teacher.active = True
            teacher.fstname = "Admin"
            teacher.lstname = sch.school_name.split(' ')[0]
            teacher.teacher_type = "TSC"
            teacher.gender = "M"
            teacher.school = sch
            teacher.phone_no = "99999999999"
            teach = teacher.save()
            # print (teach)
            # return Response("Create atleast one Teacher for the school")
        else:
            teachs = teach.filter(headteacher=True)
            if not teachs.exists():
                teach = teach[0]
            else:
                teach = teachs[0]
        return teach


    def get_class(self, school,clas):
        cls = Stream.objects.filter(class_name__icontains=clas.upper(), school=school)
        cl = Stream()
        if not (cls.exists()):
            cl.class_name = clas.upper()
            cl._class_id =get_class(clas)
            cl.school = school
            cl.save()
        else:
            cl = cls[0]
        return cl

    def create_student(self, cl, ser,date_enrolled):
        std = Students.objects.filter(fstname=ser.data.get("fstname"), lstname=ser.data.get("lstname"),
                                      midname=ser.data.get("midname"),
                                      class_id=cl)
        # check if student Exists
        if (std.exists()):
            # print "Found"
            std=None
            self.total_fails += 1
        else:
            std = Students()
            std.fstname = ser.data.get("fstname")
            std.midname = ser.data.get("midname")
            std.lstname = ser.data.get("lstname")
            std.gender = get_gender(ser.data.get("gender"))
            std.class_id = cl
            if (valid_date(date_enrolled)):
                std.date_enrolled = date_enrolled
                lst = str(datetime.now().date() - timedelta(days=35))
                if (std.date_enrolled > lst):
                    std.is_oosc = True
                else:
                    std.is_oosc = False
            else:
                std.date_enrolled = datetime.now()
                std.is_oosc = True
            #std.save()
            self.total_success += 1
        return std

class ListAbsentStudents(generics.ListAPIView):
    queryset=Attendance.objects.all()
    serializer_class = StudentsSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = AttendanceFilter

    def get_queryset(self):
        atts=Attendance.objects.all()
        atts=self.filter_queryset(atts)

        atts=atts.order_by('student').values("student_id")\
            .annotate(present_count=Count(Case(When(status=1,then=1),
            output_field=IntegerField())),
            name=Concat(F("student__fstname"),Value(' '),F("student__lstname")),
            school_name=F("student__class_id__school__school_name"),
            class_name=F("student__class_id__class_name"),
            class_id=F('student__class_id'),
            guardian_phone=F("student__guardian_phone"),
            guardian_name=F("student__guardian_name"),
            gender=F("student__gender"),
            absent_count=Count(Case(When(status=0,then=1),
            student_id='student',
            output_field=IntegerField())))
        atts = atts.exclude(absent_count=0)
        return atts

    def get_serializer_class(self):
        return AbsentStudentSerializer


class ListDropouts(generics.ListAPIView):
    queryset = Students.objects.filter(active=False)
    serializer_class = StudentsSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = EnrollmentFilter
