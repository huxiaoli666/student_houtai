from django.views import View
from django.shortcuts import HttpResponse,render,redirect
import pymysql
import json
import math
from .view import getpages
db = pymysql.connect("localhost","root","root",database="db_minestu",cursorclass=pymysql.cursors.DictCursor)
class part(View):
    def get(self,request):
        page = request.GET.get("page") if request.GET.get("page") else 0
        page = int(page)
        num=3
        cursor = db.cursor()
        sql = "select * from part limit %s,%s"
        cursor.execute(sql,(page*num,num))
        result = cursor.fetchall()
        sqls = "select count(*) as t from part"
        cursor.execute(sqls)
        nums = cursor.fetchone()
        nums = nums["t"]
        nums = math.ceil(nums/num)
        return render(request, "partinfo.html", {"data": result,"page":getpages(nums,page,"/part1")})
    def post(self,request):
        pass

class addpart(View):
    def get(self,request):
        return render(request,"addpart.html")
    def post(self,request):
        pname = request.POST.get("pname")
        pid = request.POST.get("pid")
        cursor = db.cursor()
        sql = "insert into part(pname,pid) VALUES ('%s','%s')" % (pname, pid)
        cursor.execute(sql)
        db.commit()
        return redirect("/part1/")

class delpart(View):
    def get(self,request):
        cursor = db.cursor()
        id = request.GET.get("id")
        sql = "delete from part where id="+id
        cursor.execute(sql)
        db.commit()
        return redirect("/part1/")

class partajax(View):
    def get(self,request):
        cursor = db.cursor()
        sql = "select * from part"
        cursor.execute(sql)
        result = cursor.fetchall()
        return HttpResponse(json.dumps(result))
    def post(self,request):
        pass

class editPart(View):
    def get(self,request):
        cursor = db.cursor()
        id = request.GET.get("id")
        sql = "select * from part WHERE id="+id
        cursor.execute(sql)
        result = cursor.fetchone()
        return render(request,"editPart.html",{"data":result})
    def post(self,request):
        id = request.POST.get("id")
        pname = request.POST.get("pname")
        pid = request.POST.get("pid")
        cursor = db.cursor()
        sql = "update part set pname='%s',pid=%s WHERE id=%s"%(pname,pid,id)
        cursor.execute(sql)
        db.commit()
        return redirect("/part1/")
