from django.views import View
from django.shortcuts import HttpResponse,render,redirect
import pymysql
import json
from django import forms
import xlrd
import math
from .view import getpages
db = pymysql.connect("localhost","root","root",database="db_minestu",cursorclass=pymysql.cursors.DictCursor)

# class headsearch(View):
#     def get(self,request):
#         print("get")
#     def post(self,request):
#         print("2313123")
#         cursor = db.cursor()
#         gid = request.POST.get("gid")
#         pid = request.POST.get("pid")
#         tid = request.POST.get("tid")
#         print("----------", gid, pid, tid)
#         condition=" where 1=1"
#         condition += " and tests.gid="+gid if gid else ""
#         condition += " and tests.pid="+pid if pid else ""
#         condition += " and tests.tid="+tid if tid else ""
#         sql = "select tests.id,types.tname as tnames,part.pname as pnames,grade.gname as gnames,title,tests.`opts`,result from tests LEFT JOIN types on types.tid = tests.tid LEFT JOIN part on part.pid=tests.pid LEFT JOIN grade on tests.gid=grade.gid "+condition
#         cursor.execute(sql)
#         result = cursor.fetchall()
#         sql1="select * from grade"
#         cursor.execute(sql1)
#         grades = cursor.fetchall()
#         sql2="select * from part"
#         cursor.execute(sql2)
#         parts = cursor.fetchall()
#         sql3 = "select * from types"
#         cursor.execute(sql3)
#         types = cursor.fetchall()
#
#         gid = "0" if not request.POST.get("gid") else request.POST.get("gid")
#         pid = "0" if not request.POST.get("pid") else request.POST.get("pid")
#         tid = "0" if not request.POST.get("tid") else request.POST.get("tid")
#
#         return render(request,"testsinfo.html",{"data":result,"grades":grades,"parts":parts,"types":types,"pid":int(pid),"gid":int(gid),"tid":int(tid)})

class testTable(View):
    def get(self,request):
        page = request.GET.get("page") if request.GET.get("page") else 0
        page = int(page)
        num = 3
        cursor = db.cursor()
        sql = "select tests.gid,tests.pid,tests.tid,tests.id,types.tname as tnames,part.pname as pnames,grade.gname as gnames,title,tests.`opts`,result from tests LEFT JOIN types on types.tid = tests.tid LEFT JOIN part on part.pid=tests.pid LEFT JOIN grade on tests.gid=grade.gid limit %s,%s"

        grades = "select * from grade"
        parts = "select * from part"
        types = "select * from types"
        cursor.execute(sql,(page*num,num))
        result = cursor.fetchall()
        cursor.execute(grades)
        grades = cursor.fetchall()
        cursor.execute(parts)
        parts = cursor.fetchall()
        cursor.execute(types)
        types = cursor.fetchall()
        sqls = "select COUNT(*) as t from tests"
        cursor.execute(sqls)
        nums = cursor.fetchone()
        nums = nums["t"]
        nums = math.ceil(nums / num)  # ??????????

        return render(request, "testsinfo.html",{"data":result,"page":getpages(nums,page,"/testtable/"),"grades":grades,"parts":parts,"types":types})
    def post(self,request):
        print("2313123")
        cursor = db.cursor()
        gid = request.POST.get("gid")
        pid = request.POST.get("pid")
        tid = request.POST.get("tid")
        print("----------", gid, pid, tid)
        condition=" where 1=1"
        condition += " and tests.gid="+gid if gid else ""
        condition += " and tests.pid="+pid if pid else ""
        condition += " and tests.tid="+tid if tid else ""
        sql = "select tests.id,types.tname as tnames,part.pname as pnames,grade.gname as gnames,title,tests.`opts`,result from tests LEFT JOIN types on types.tid = tests.tid LEFT JOIN part on part.pid=tests.pid LEFT JOIN grade on tests.gid=grade.gid "+condition
        cursor.execute(sql)
        result = cursor.fetchall()
        sql1="select * from grade"
        cursor.execute(sql1)
        grades = cursor.fetchall()
        sql2="select * from part"
        cursor.execute(sql2)
        parts = cursor.fetchall()
        sql3 = "select * from types"
        cursor.execute(sql3)
        types = cursor.fetchall()

        gid = "0" if not request.POST.get("gid") else request.POST.get("gid")
        pid = "0" if not request.POST.get("pid") else request.POST.get("pid")
        tid = "0" if not request.POST.get("tid") else request.POST.get("tid")

        return render(request,"testsinfo.html",{"data":result,"grades":grades,"parts":parts,"types":types,"pid":int(pid),"gid":int(gid),"tid":int(tid)})
class testTableAdd(View):
    def get(self,request):
        return render(request, "addtestsinfo.html")
    def post(self,request):
        cursor = db.cursor()
        gid = request.POST.get("gid")
        pid = request.POST.get("pid")
        tid = request.POST.get("tid")
        title = request.POST.get("title")
        opts = request.POST.get("opts")
        result = request.POST.get("result")
        sql = "insert into tests(gid,pid,tid,title,opts,result) VALUES(%s,%s,%s,'%s','%s','%s')"%(gid,pid,tid,title,opts,result)

        cursor.execute(sql)
        db.commit()
        return HttpResponse("ok")

class testtableajax(View):
    def get(self,request):
        cursor = db.cursor()
        sql = "select gname from grade"
        cursor.execute(sql)
        result = cursor.fetchall()
        return HttpResponse(json.dumps(result))

class searchname(View):
    def post(self,request):
        cursor = db.cursor()
        name = request.POST.get("searchname")
        sql = "select tests.id,types.tname as tnames,part.pname as pnames,grade.gname as gnames,title,tests.`opts`,result from tests LEFT JOIN types on types.tid = tests.tid LEFT JOIN part on part.pid=tests.pid LEFT JOIN grade on tests.gid=grade.gid where tests.title like '%%%s%%'"%(name)
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
        grades = "select * from grade"
        parts = "select * from part"
        types = "select * from types"
        cursor.execute(grades)
        grades = cursor.fetchall()
        cursor.execute(parts)
        parts = cursor.fetchall()
        cursor.execute(types)
        types = cursor.fetchall()
        return render(request, "testsinfo.html",{"data":result,"grades":grades,"parts":parts,"types":types})

class mycheck(forms.Form):
    gid = forms.CharField(required=True, error_messages={"required": "必须选择一个年级"})
    pid = forms.CharField(required=True, error_messages={"required": "必须选择一个阶段"})
    file = forms.FileField(required=True,error_messages={"required": "必须选择文件"})

class testupfile(View):
    def get(self,request):
        return render(request,"testupfile.html")
    def post(self,request):
        obj = mycheck(request.POST,request.FILES)
        if obj.is_valid():
            cursor = db.cursor()
            gid = request.POST.get("gid")
            pid = request.POST.get("pid")
            file = request.FILES["file"]
            sheet = xlrd.open_workbook(filename=None,file_contents=file.read()) #通过内存读成二进制的信息
            data = sheet.sheet_by_index(0)
            arrs = []
            type = "select tname,tid from types"
            cursor.execute(type)
            type = cursor.fetchall()
            typeDict = {}
            for i in type:
                typeDict[i["tname"]] = i["tid"]
            print(typeDict)
            for row in range(1,data.nrows):
                arr = data.row_values(row)
                arr[0] = typeDict[arr[0]]
                arr[2] = "|".join(arr[2].split("\n"))
                arr.append(gid)
                arr.append(pid)
                arrs.append(arr)

            sql = "insert IGNORE into tests(tid,title,opts,result,gid,pid) values(%s,%s,%s,%s,%s,%s)"
            cursor.executemany(sql,arrs)
            db.commit()
            # data = request.FILES["file"]
            # f = open("test.xlsx","wb")
            # for item in data.chunks():    #上传的文件分成块写入新的文件
            #     f.write(item)
            # f.close()
            return redirect("/testupfile/")
        else:
            print("------------------")
            fileerr = obj.errors["file"][0]
            # giderr = obj.errors["gid"][0]
            # piderr = obj.errors["pid"][0]
            # return render(request,"testupfile.html",{"fileerr":fileerr,"giderr":giderr,"piderr":piderr})
            return render(request,"testupfile.html",{"fileerr":fileerr})

class deltests(View):
    def get(self,request):
        id = request.GET.get("id")
        cursor = db.cursor()
        sql = "delete from tests where id="+id
        cursor.execute(sql)
        db.commit()
        return redirect("/testtable/")

class edittests(View):
    def get(self,request):
        id = request.GET.get("id")
        cursor = db.cursor()
        sql = "select * from tests WHERE id="+id
        cursor.execute(sql)
        result = cursor.fetchone()
        return render(request,"edittests.html",{"data":result})
    def post(self,request):
        id = request.POST.get("id")
        gid = request.POST.get("gid")
        pid = request.POST.get("pid")
        tid = request.POST.get("tid")
        title = request.POST.get("title")
        opts = request.POST.get("opts")
        result = request.POST.get("result")
        cursor = db.cursor()
        sql = "update tests set gid=%s,pid=%s,tid=%s,title=%s,opts=%s,result=%s where id=%s"
        cursor.execute(sql,[gid,pid,tid,title,opts,result,id])
        db.commit()
        return redirect("/testtable/")