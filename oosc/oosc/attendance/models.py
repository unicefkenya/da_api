from django.db import models
from oosc.stream.models import Stream
from oosc.students.models import Students
from datetime import datetime
# Create your models here.
class Attendance(models.Model):
    ATTENDANCE=((1,'Present'),(0,'Absent'))
    id=models.CharField(primary_key=True,max_length=50)
    student  = models.ForeignKey(Students, on_delete = models.CASCADE)
    date    = models.DateTimeField()
    created=models.DateTimeField(default=datetime.now)
    modified=models.DateTimeField(default=datetime.now)
    status  = models.IntegerField(choices=ATTENDANCE,default = 0) #assuming 1 is present 0 is absent
    cause_of_absence = models.CharField(max_length = 200,null=True,blank=True)
    _class = models.ForeignKey(Stream, on_delete= models.CASCADE)
    def __str__(self):
        return str(self.student)
    class Meta:
        get_latest_by="date"