from django.views import View
from django.shortcuts import HttpResponse,render,redirect
import pymysql
import json
import math
from .view import getpages
db = pymysql.connect("localhost","root","root",database="db_minestu",cursorclass=pymysql.cursors.DictCursor)
class one(View):
    def get(self,request):
        page = request.GET.get("page") if request.GET.get("page") else 0
        page = int(page)
        num = 3
        cursor = db.cursor()
        # sql = "select * from grade"
        sql = "select *,GROUP_CONCAT(pname) as pnames,GROUP_CONCAT(gname) as gnames from grade LEFT JOIN part on FIND_IN_SET(part.pid,grade.pid) GROUP BY gname order by grade.id asc limit %s,%s"
        cursor.execute(sql,(num*page,num))
        result = cursor.fetchall()
        sqls = "select COUNT(*) as t from grade"
        cursor.execute(sqls)
        nums = cursor.fetchone()
        nums = nums["t"]
        nums = math.ceil(nums/num)
        return render(request, "gradeinfo.html", {"data": result,"page":getpages(nums,page,"/grade1")})
    def post(self,request):
        pass

class addgrade(View):
    def get(self,request):
        cursor = db.cursor()
        sql = "select * from grade"
        cursor.execute(sql)
        result = cursor.fetchall()
        return render(request,"addgrade.html",{"data": result})
    def post(self,request):
        gname = request.POST.get("gname")
        gid = request.POST.get("gid")
        pid = request.POST.getlist("pid") #变成字符串   #字符串类型
        pids =""    #因为最终需要的是find_in_set提取，所以必须是字符串
        for item in pid:
            pids+=item+','
        pids=pids[:-1]
        print(pids)
        cursor = db.cursor()
        sql = "insert into grade(gname,gid,pid) VALUES ('%s','%s','%s')" % (gname, gid,pids)
        cursor.execute(sql)
        db.commit()
        return redirect("/grade1/")

class gradeajax(View):
    def get(self,request):
        cursor = db.cursor()
        sql = "select * from grade"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
        return HttpResponse(json.dumps(result))

class delgrade(View):
    def get(self,request):
        id = request.GET.get("id")
        cursor = db.cursor()
        sql = "delete from grade WHERE id="+id
        cursor.execute(sql)
        db.commit()
        return redirect("/grade1/")

class editGrade(View):
    def get(self,request):
        id = request.GET.get("id")
        cursor = db.cursor()
        sql = "select * from grade WHERE id="+id
        cursor.execute(sql)
        result = cursor.fetchone()
        return render(request,"editGrade.html",{"data":result})
    def post(self,request):
        gname = request.POST.get("gname")
        pid = request.POST.getlist("pid")
        pass

