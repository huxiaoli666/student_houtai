from django.views import View
from django.shortcuts import HttpResponse,render,redirect
import pymysql
import json
import math
from .view import getpages
db = pymysql.connect("localhost","root","root",database="db_minestu",cursorclass=pymysql.cursors.DictCursor)
class test(View):
    def get(self,request):
        page = request.GET.get("page") if request.GET.get("page") else 0
        page=int(page)
        num=3
        cursor = db.cursor()
        sql = "select * from types limit %s,%s"
        cursor.execute(sql,(page*num,num))
        result = cursor.fetchall()
        sqls = "select COUNT(*) as t from types"
        cursor.execute(sqls)
        nums = cursor.fetchone()
        nums = nums["t"]
        nums = math.ceil(nums / num)
        return render(request, "testinfo.html",{"data":result,"page":getpages(nums,page,"/test1")})
    def post(self,request):
        pass
class testadd(View):
    def get(self,request):
        return render(request, "addtest.html")
    def post(self,request):
        cursor = db.cursor()
        tname = request.POST.get("tname")
        tid = request.POST.get("tid")
        #form表单验证的类 django中存在
        sql ="insert into types(tname,tid) VALUES (%s,%s)"
        cursor.execute(sql,[tname,tid])
        db.commit()
        return redirect("/test1/")

class testajax(View):
    def get(self, request):
        cursor = db.cursor()
        sql = "select * from types"
        cursor.execute(sql)
        result = cursor.fetchall()
        return HttpResponse(json.dumps(result))

class deltype(View):
    def get(self,request):
        cursor = db.cursor()
        id = request.GET.get("id")
        sql = "delete from types where id="+id
        cursor.execute(sql)
        db.commit()
        return redirect("/test1/")

class edittype(View):
    def get(self,request):
        cursor = db.cursor()
        id = request.GET.get("id")
        sql = "select * from types WHERE id="+id
        cursor.execute(sql)
        result = cursor.fetchone()
        return render(request,"edittype.html",{"data":result})
    def post(self,request):
        cursor = db.cursor()
        id = request.POST.get("id")
        tname = request.POST.get("tname")
        tid = request.POST.get("tid")
        sql = "update types set tname=%s,tid=%s where id=%s"
        cursor.execute(sql,[tname,tid,id])
        db.commit()
        return redirect("/test1/")

