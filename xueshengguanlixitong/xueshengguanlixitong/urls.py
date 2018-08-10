"""xueshengguanlixitong URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import re_path

from .view import *
from .grade1 import *
from .part1 import *
from .test1 import *
from .testtable import *
from .zutibiao import *
from .scorebiao import *

#类型 题目 选项  答案
#解析上传文件
    #1.pip install xlrd
    #2.import xlrd

#数据库去重/防止重复插入数据库
    # 添加索引-------索引是唯一的
        #IGNORE   与字段的索引相结合使用，索引是唯一的键
        #insert IGNORE into demo(`name`) VALUES("zhangsan")
#<257  值与内存都是相等的
#>257  值相等，内存不等 is判断内存地址与值是否都相等
#{% if item.gid == gid %} style="color:red" {% endif %}





urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('login/',login),  #登录页     也可以使用正则re_path('^login/?$',login),
    path('sign/',sign),   #注册页
    path('header/',header),
    path('lefter/',lefter),
    path('main1/',main1),
    path('footer/',footer),
    path('exit/',exit),

#--------------学生-----------
    path('stuinfo/',stuinfo),
    path('edit/',edit),
    path('addstud/',addstud),
    path('ajaxstu/',ajaxstu),
    path('delstud/',delstud),
#--------------教师-----------
    path('teainfo/',teainfo),
    path('edittea/',edittea),
    path('addtea/', addtea),
    path('ajax/',ajax),
    path('deltea/', deltea),
#--------------班级-----------
    path('clainfo/',clainfo),
    path('addclas/',addclas),
    path('delcla/',delcla),
    path('editcla/',editcla),
    path('classajax/',classajax),
    path('classajax1/',classajax1),

    path('grade1/',one.as_view()),  #读取类  年级信息
    path('addgrade/',addgrade.as_view()),  #读取类  年级信息
    path('gradeajax/',gradeajax.as_view()),  #
    path('delgrade/',delgrade.as_view()),  #
    path('editGrade/',editGrade.as_view()),  #

    path('part1/',part.as_view()),    #所带课程
    path('addpart/',addpart.as_view()),
    path('delpart/',delpart.as_view()),
    path('partajax/',partajax.as_view()),
    path('editPart/',editPart.as_view()),
    # re_path('^delpart.html$',delpart.as_view()),   #seo、sem搜索引擎优化

    path('test1/',test.as_view()),   #试题类型
    path('testadd/',testadd.as_view()),
    path('testajax/',testajax.as_view()),
    path('deltype/',deltype.as_view()),
    path('edittype/',edittype.as_view()),

    path('testtable/',testTable.as_view()),   #试题表testtable
    path('testTableAdd/',testTableAdd.as_view()),
    path('headsearch/',headsearch.as_view()),
    path('searchname/',searchname.as_view()),
    path('testupfile/',testupfile.as_view()),
    path('deltests/',deltests.as_view()),
    path('edittests/',edittests.as_view()),
    # gid = request.POST.get("gid") if not request.POST.get("gid") else int(request.POST.get("gid"))
#vuex保存数据与状态
    path('zutibiao/',zutiTable.as_view()),
    path('zutiTableAdd/',zutiTableAdd.as_view()),

    path('scorebiao/',scoreTable.as_view()),
    path('scoreTableAdd/',scoreTableAdd.as_view()),


]
