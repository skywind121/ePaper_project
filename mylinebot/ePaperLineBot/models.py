from django.db import models
from django.utils import timezone
import pytz

def get_localtime(utctime):
    utc = utctime.replace(tzinfo=pytz.UTC)
    localtz = utc.astimezone(timezone.get_current_timezone())
    return localtz

# Create your models here.
class User_Info(models.Model):
    uid = models.CharField(max_length=50,null=False,default='')             # user_id
    lineName = models.CharField(max_length=255,blank=True,null=False)       # LINE名字
    userTrueName = models.CharField(max_length=255,blank=True,null=False)   # 使用者真實姓名
    pic_url = models.CharField(max_length=255,null=False)                   # 大頭貼網址
    mdt = models.DateTimeField(auto_now=True)                               # 物件儲存的日期時間

    def __str__(self):
        return self.uid



# 景點位置
class Location(models.Model):
    name = models.CharField(max_length=255)  #位置名稱
    
#景點貼文
class Post(models.Model):
    subject = models.CharField(max_length=255)  #標題
    content = models.CharField(max_length=255)  #內容
    author = models.CharField(max_length=20)  #貼文者
    create_date = models.DateField(default=timezone.now)  #貼文時間
    location = models.ForeignKey(Location, on_delete=models.CASCADE) #景點位置