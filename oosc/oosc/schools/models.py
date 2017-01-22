from django.db import models
#from oosc.teachers.models import Teachers
from oosc.zone.models import Zone
from django.contrib.auth.models import User
#from oosc.teachers.models import Teachers
# Create your models here.
class Schools(models.Model):
    LEVELS=(('PRIMARY','Primary'),('SECONDARY','Secondary'))
    STATUS=(('PUBLIC','Public'),('PRIVATE','Private'))
    school_code = models.IntegerField(default=0,null=True,blank=True)
    school_name = models.CharField(max_length = 200, default="schoolname")
    geo_cordinates  = models.CharField(max_length = 200,null=True,blank=True)
    emis_code   = models.IntegerField(default = 0,null=True,blank=True)
    zone = models.ForeignKey(Zone, on_delete = models.CASCADE)
    source_of_water = models.CharField(max_length = 200,null=True,blank=True)
    headteacher = models.OneToOneField(User,related_name="headteacher",null=True,blank=True)
    phone_no    = models.IntegerField(default=0,)
    level=models.CharField(choices=LEVELS,max_length=50,default='PRIMARY')
    status=models.CharField(choices=STATUS,max_length=50,default='PUBLIC')


    def __str__(self):
        return self.school_name
