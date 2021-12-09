from django.contrib import admin

# Register your models here.
from ePaperLineBot.models import *

class User_Info_Admin(admin.ModelAdmin):
    list_display = ('uid','lineName','userTrueName','pic_url','mdt')
admin.site.register(User_Info,User_Info_Admin)

"""
Username (leave blank to use 'h5222'): epapersuperuser
Email address: h5222436@gmail.com
Password: jj881013
"""