from django.urls import path

from ePaperLineBot import admin
from . import views  #引用這個資料夾中的views檔案

urlpatterns = [
    #path('overview', views.index, name = "Index"),
    path('callback', views.callback),
    path('admin', admin.User_Info_Admin)
]