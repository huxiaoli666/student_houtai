from django.views import View   #继承
from django.shortcuts import HttpResponse,render,redirect   #响应
import pymysql

db = pymysql.connect("localhost","root","root",database="db_minestu",cursorclass=pymysql.cursors.DictCursor)
class scoreTable(View):
    def get(self,request):
        cursor = db.cursor()
        sql = "select * from scores"
        cursor.execute(sql)
        result = cursor.fetchall()
        return render(request, "scoreinfo.html", {"data": result})
    def post(self,request):
        pass

class scoreTableAdd(View):
    def get(self,request):
        return render(request,"addscore.html")
    def post(self,request):
        cursor = db.cursor()
        zuid = request.POST.get("zuid")
        errors = request.POST.get("errors")
        score = request.POST.get("score")
        sql = "insert into scores(zuid, score, errors) VALUES (%s,%s,%s)"
        cursor.execute(sql,[zuid,errors,score])
        db.commit()
        return redirect("/scorebiao/")

