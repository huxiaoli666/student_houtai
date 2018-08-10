from django.shortcuts import render,redirect,HttpResponse
import pymysql
import hashlib   #验证
import math
import re
db = pymysql.connect("localhost","root","root",database="db_minestu",cursorclass=pymysql.cursors.DictCursor)
'''
学科：语数英 class,teacher
年级管理
阶段管理
'''

def check(callback):
    def abc(request):
        if request.session.get("name") == "yes":
            return callback(request)
        else:
            return redirect(login)
    return abc
def md5(str):
    md5=hashlib.md5()
    md5.update(str.encode("utf8"))
    return md5.hexdigest()

#登录页
def login(request):
    if request.method == "GET":
        # if request.session.get("login") == "yes":
        #     return redirect(index)
        # else:
            return render(request, "login.html", {"message": ""})
    elif request.method == "POST":
        name = request.POST.get("name")
        pass1 = md5(request.POST.get("pass1"))
        save = request.POST.get("save")
        # 数据的验证：正则
        # try:
        #     rename = re.match('[\w]{1-11}',name)
        #     repass = re.match('[\w]{1-11}',pass1)
        #     if rename == name and repass == pass1:
        #         return render(request,"login.html")
        #     else:
        #         return render(request, "login.html", {"message":"用户名与密码不匹配"})
        # except:
        #     pass
        if name == "" and pass1 == "":
            return render(request, "login.html", {"message":"请输入用户名"})
        else:
            cursor = db.cursor()
            sql = "select * from t_user where name=%s and pass1=%s"
            cursor.execute(sql,[name,pass1])
            result = cursor.fetchall()
            if len(result) > 0:
                if save:
                    obj = redirect(index)
                    request.session["login"] = "yes"
                    request.session["name"] = name
                    request.session.set_expiry(60 * 60 * 24 * 7)
                    return obj
                else:
                    obj = redirect(index)
                    request.session["login"] = "yes"
                    request.session["name"] = name
                    request.session.set_expiry(0)
                    return obj
            else:
                return render(request, "login.html", {"message": "登录失败"})

#主页
def index(request):
    if request.session.get("login") == "yes":
        result = request.session.get("name")
        print(result)
        return render(request,"index.html",{"name":result})
    else:
        return render(request,"login.html")

#注册
def sign(request):
    return render(request,"sign.html")

#头部
def header(request):   #request接收一个传回来的参数
    name = request.GET.get("name")
    return render(request,"header.html",{"name":name})
def exit(request):
    # del request.session["login"]
    request.session.clear()
    return redirect(login)
#左侧栏
def lefter(request):
    return render(request,"lefter.html")

#main
def main1(request):
    return render(request,"main1.html")

def footer(request):
    return render(request,"footer.html")

'''
总页数，当前页
'''
def getpages(total,page,url):
    items=3
    str1='''
     <a href="%s?page=0">首页</a>
    '''%(url)

    up=page-1 if page-1>0 else 0
    str1 += '''
         <a href="%s?page=%s">上一页</a>
        '''%(url,up)
    next=page+1 if page+1<total else page

    before = page if page<math.floor(items/2) else math.floor(items/2)
    for item in range(before,0,-1):
         num=page-item
         if num==page:
             str1+='''
                  <a href="%s?page=%s" style="color:red">%s</a>
            '''%(url, num, num + 1)
         else:
            str1 += '''
              <a href="%s?page=%s">%s</a>
        ''' % (url, num, num + 1)
    after=items-before
    for item in range(after):
         num=page+item
         if (num<total):
             if num==page:
                 str1 += '''
                       <a href="%s?page=%s" style="color:red">%s</a>
                 ''' % (url, num, num + 1)
             else:
                 str1+='''
                      <a href="%s?page=%s">%s</a>
                '''%(url,num,num+1)
    str1 += '''
             <a href="%s?page=%s">下一页</a>
            '''%(url,next)
    str1 += '''
             <a href="%s?page=%s">尾页</a>
            '''%(url,total-1)
    return str1
#点击左侧栏学生信息跳转到相应的页面
#项目资源配置表
#项目变更
#项目阶段审查
#项目自我评价表（担任角色、任务）
#
@check
def stuinfo(request):
    page = request.GET.get("page") if request.GET.get("page") else 0
    page = int(page)
    num = 3
    cursor = db.cursor()
    sql = "select * from t_stu LEFT JOIN t_class on t_class.id = t_stu.classID limit %s,%s"
    cursor.execute(sql,(page*num,num))
    result = cursor.fetchall()
    sqls = "select count(*) as t from t_stu LEFT JOIN t_class on t_class.id = t_stu.id"
    cursor.execute(sqls)
    nums = cursor.fetchone()
    nums = nums["t"]
    nums = math.ceil(nums/num)
    # up = page-1 if page-1>0 else 0
    # next = page+1 if page+1<nums else page
    return render(request, "stuinfo.html", {"data": result,"page":getpages(nums,page,"/stuinfo")})
    # return render(request, "stuinfo.html", {"data": result,"up":up,"next":next})

def edit(request):
    if request.method == "GET":
        cursor = db.cursor()
        id = request.GET.get("id")
        sql = "select * from t_stu LEFT JOIN t_class on t_class.id = t_stu.classID where t_stu.id=%s"
        cursor.execute(sql,[id])
        result = cursor.fetchone()
        sql1 = "select * from t_class"
        cursor.execute(sql1)
        stuInfo = cursor.fetchall()
        return render(request,"editstu.html",{"data":result,"stuInfo":stuInfo})
    elif request.method == "POST":
        cursor = db.cursor()
        id = request.POST.get("id")
        name = request.POST.get("name")
        age = request.POST.get("age")
        snumber = request.POST.get("snumber")
        class1 = request.POST.get("classID")
        print(class1)
        sql = "update t_stu set name='%s',age='%s',snumber='%s',classID='%s' where id='%s'"%(name,age,snumber,class1,id)
        cursor.execute(sql)
        db.commit()
        return redirect(stuinfo)

def addstud(request):
    if request.method == "GET":
        cursor = db.cursor()
        sql = "select * from t_class"
        cursor.execute(sql)
        result = cursor.fetchall()
        return render(request,"addstu.html",{"data":result})
    elif request.method == "POST":
        cursor = db.cursor()
        name = request.POST.get("name")
        age = request.POST.get("age")
        snumber1 = request.POST.get("snumber")
        class1 = request.POST.get("classID")
        cpass = md5("123456")
        try:
            sql = "insert into t_stu(name,age,snumber,classID,spass) VALUES ('%s','%s','%s','%s','%s')"%(name,age,snumber1,class1,cpass)
            cursor.execute(sql)
            # cursor.executemany()  #一次性可以执行多条语句
            db.commit()

        except:
            db.rollback()
        return redirect(stuinfo)

def ajaxstu(request):
    cursor = db.cursor()
    snumber1 = request.GET.get("snumber")
    sql = "select * from t_stu where snumber='%s'"%(snumber1)
    cursor.execute(sql)
    result = cursor.fetchone()
    if result:
        return HttpResponse("false")
    else:
        return HttpResponse("true")

def delstud(request):
    id = request.GET.get("id")
    cursor = db.cursor()
    sql = "delete from t_stu where id="+id
    cursor.execute(sql)
    db.commit()
    return redirect(stuinfo)
#----------------------教师-------------------
@check
def teainfo(request):
    page = request.GET.get("page") if request.GET.get("page") else 0
    page = int(page)
    num = 3
    cursor = db.cursor()
    # sql = "SELECT t_tea.id teid,name,t_tea.tnumber,t_class.id clsid,class_name from t_tea LEFT JOIN t_tea_class on t_tea.id = t_tea_class.tea_id LEFT JOIN t_class on class_id=t_class.id limit %s,%s"
    # sql = "SELECT t_tea.id teid,name,t_tea.tnumber,t_class.id clsid,class_name,group_concat(class_id) as class_id,GROUP_CONCAT(class_name) as class_name1 from t_tea LEFT JOIN t_tea_class on t_tea.id = t_tea_class.tea_id LEFT JOIN t_class on class_id=t_class.id GROUP BY(t_tea.id) limit %s,%s"
    sql = "SELECT t_tea.id as id,`name`,tnumber,GROUP_CONCAT(pname) as pnames from t_tea LEFT JOIN part ON FIND_IN_SET(part.pid,t_tea.pid) GROUP BY tnumber limit %s,%s"
    cursor.execute(sql,(num*page,num))
    result = cursor.fetchall()
    print(result)
    # sqls = "SELECT count(*) as t from t_tea LEFT JOIN t_tea_class on t_tea.id = t_tea_class.tea_id LEFT JOIN t_class on class_id=t_class.id group by (t_tea.name)"
    sqls = "select count(*) as t from t_tea"
    cursor.execute(sqls)
    nums = cursor.fetchone()
    nums = nums["t"]
    nums = math.ceil(nums / num)
    arr={}
    # for item in result:
    #     if item["teid"] not in arr:
    #         arr[item["teid"]] = item
    #         tea = item['class_name']
    #         arr[item["teid"]]["class_name"] = []
    #         arr[item["teid"]]["class_name"].append(tea)
    #     else:
    #         arr[item["teid"]]["class_name"].append(item['class_name'])
    # arr=arr.values()
    return render(request, "teainfo.html",{"data":result,"page":getpages(nums,page,"/teainfo")})

def addtea(request):
    if request.method == "GET":
        cursor = db.cursor()
        sql = "select * from part"
        cursor.execute(sql)
        result = cursor.fetchall()
        return render(request,"addteac.html", {"classInfo": result})
    elif request.method == "POST":
        cursor = db.cursor()
        name = request.POST.get("name")
        tnumber = request.POST.get("tnumber")
        pid = request.POST.getlist("pid")
        pids = ""
        for item in pid:
            pids+=item+","
        pids+=pids[:-1]
        sql = "select * from t_tea where tnumber='%s'"%(tnumber)
        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            return redirect(addtea)
        else:
            try:
                sql1 = "insert into t_tea(name,tnumber,pid) VALUES ('%s','%s','%s')" % (name,tnumber,pids)
                cursor.execute(sql1)
                db.commit()
                # teaId = db.insert_id()
                # for i in ids:
                #     sql = "insert into t_tea_class(tea_id,class_id) VALUES ('%s','%s')"%(teaId,i)
                #     cursor.execute(sql)

            except:
                db.rollback()
            return redirect(teainfo)

def ajax(request):
    cursor = db.cursor()
    tnumber1 = request.GET.get("tnumber")
    sql = "select * from t_tea where tnumber='%s'"%(tnumber1)
    cursor.execute(sql)
    result = cursor.fetchone()
    if result:
        return HttpResponse("false")
    else:
        return HttpResponse("true")

def edittea(request):
    if request.method == "GET":
        cursor = db.cursor()
        id = request.GET.get("id")
        sql = "select *,GROUP_CONCAT(part.pname) as pname from t_tea LEFT JOIN part on part.pid=t_tea.pid where t_tea.id="+id
        cursor.execute(sql)
        result = cursor.fetchone()
        sql = "select * from part"
        cursor.execute(sql)
        classInfo = cursor.fetchall()
        print("-----classinfo,",classInfo)
        return render(request,"editteac.html",{"data":result,"classInfo":classInfo})
    elif request.method == "POST":
        cursor = db.cursor()
        id = request.POST.get("id")
        name = request.POST.get("name")
        tnumber = request.POST.get("tnumber")
        pid = request.POST.getlist("pid")
        pids=','.join(pid)
        print("----------------",id,pid,type(pids))
        # pids = ""
        # for item in pid:
        #     pids+=item+","
        # pids+=pids[:-1]
        sql = "update t_tea set name='%s',tnumber='%s',pid='%s' where id='%s'"%(name,tnumber,pids,id)
        print(sql)
        cursor.execute(sql)
        db.commit()
        # try:
        #     sql1 = "update part set pname='%s' where part.pid='%s'"
        #     cursor.execute(sql1,())
        #     db.commit()
        #     # ids = request.POST.getlist("class_id")
        #     # print(id,ids)
        #     # sql = "delete from t_tea_class where tea_id="+id
        #     # cursor.execute(sql)
        #     # for i in ids:
        #     #     sql = "insert into t_tea_class(tea_id,class_id) VALUES ('%s','%s')"%(id,i)
        #     #     cursor.execute(sql)
        # except:
        #     db.rollback()
        return redirect(teainfo)

def deltea(request):
    id = request.GET.get("id")
    cursor = db.cursor()
    sql = "delete from t_tea where id="+id
    cursor.execute(sql)
    db.commit()
    return redirect(teainfo)
#----------------------班级-------------------
import json
@check
def clainfo(request):
    page = request.GET.get("page") if request.GET.get("page") else 0
    page = int(page)
    num = 3
    cursor = db.cursor()
    # sql = "select t_class.id,class_name,gid,t_tea.id,GROUP_CONCAT(name) as name from t_class LEFT JOIN t_tea_class on t_class.id = t_tea_class.class_id LEFT JOIN t_tea on tea_id = t_tea.id GROUP BY(class_name) limit %s,%s"
    sql = "select t_class.class_name,grade.gname,GROUP_CONCAT(part.pname) as pnames,GROUP_CONCAT(t_tea.`name`) as tname from t_class LEFT JOIN grade on grade.gid=t_class.gid LEFT JOIN t_tea_class on t_tea_class.class_id=t_class.id LEFT JOIN t_tea on t_tea_class.tea_id=t_tea.id LEFT JOIN part on t_tea.pid=part.pid GROUP BY class_name limit %s,%s"
    cursor.execute(sql,(page*num,num))   #page*num??????
    data = cursor.fetchall()
    sql1 = "select GROUP_CONCAT(gname) as gname,pid from t_class left join grade on t_class.gid=grade.gid GROUP BY(class_name)"
    cursor.execute(sql1)
    result = cursor.fetchall()
    # sqls = "select COUNT(*) as t from t_class LEFT JOIN t_tea_class on t_class.id = t_tea_class.class_id LEFT JOIN t_tea on tea_id = t_tea.id group by (t_class.class_name)"
    sqls = "select count(*) as t from t_class"
    cursor.execute(sqls)
    nums = cursor.fetchone()
    nums = nums["t"]
    nums = math.ceil(nums / num)   #??????????
    # sql2 = "select *,GROUP_CONCAT(class_name) as class_names from grade LEFT JOIN t_class on grade.gid=t_class.gid"
    # cursor.execute(sql2)
    # gradeinfo = cursor.fetchall()
    # for i in gradeinfo:
    #     gradeinfo = i
    #     print("-----gradeinfo",gradeinfo)
    # arr = {}
    # for item in result:
    #     if item["id"] not in arr:
    #         arr[item["id"]] = item
    #         tea = item['name']
    #         arr[item["id"]]["name"] = []
    #         # print(item)
    #         arr[item["id"]]["name"].append(tea)
    #     else:
    #         arr[item["id"]]["name"].append(item['name'])
    # data = arr.values()
    return render(request,"clainfo.html",{"data":data,"result":result,"page":getpages(nums,page,"/clainfo")})

def addclas(request):
    if request.method == "GET":
        cursor = db.cursor()
        sql = "select * from grade"
        cursor.execute(sql)
        teacherInfo = cursor.fetchall()
        return render(request,"addclass.html",{"teacherInfo":teacherInfo})
    elif request.method == "POST":
        cursor = db.cursor()
        name = request.POST.get("class_name")
        gid = request.POST.get("gid")
        infos = request.POST.get("infos")
        ids = request.POST.getlist("id")
        infos = json.loads(infos).values()
        arr = []
        try:
            sql = "insert into t_class(class_name,gid) VALUES ('%s','%s')"%(name,gid)
            cursor.execute(sql)
            classID = db.insert_id()
            for item in infos:
                yz=(item["tid"],classID,item["pid"])
                arr.append(yz)
            sqls = "insert into t_tea_class(tea_id, class_id,pid) VALUES (%s,%s,%s)"
            cursor.executemany(sqls,(arr))
            db.commit()
            print("------aa",arr)
        except:
            db.rollback()
        return redirect(clainfo)

def delcla(request):
    cursor = db.cursor()
    id = request.GET.get("id")
    try:
        sql = "delete from t_class where id="+id
        cursor.execute(sql)
        db.commit()
        sql = "delete from t_tea_class where class_id=%s "%(id)
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    return redirect(clainfo)

def editcla(request):
    if request.method == "GET":
        cursor = db.cursor()
        id = request.GET.get("id")
        print(id)
        print(type(id))
        sql = "select t_class.id tcid,t_class.class_name,t_tea.pid,t_tea.id,t_tea.`name` from t_class LEFT JOIN t_tea_class on t_class.id = class_id LEFT JOIN t_tea on tea_id = t_tea.id WHERE t_class.id='%s'"%(id)
        cursor.execute(sql)
        result = cursor.fetchone()
        sql = "select * from t_tea"
        cursor.execute(sql)
        teacherInfo = cursor.fetchall()
        return render(request,"editcla.html",{"data":result,"teacherInfo":teacherInfo})
    elif request.method == "POST":
        cursor = db.cursor()
        id = request.POST.get("id")
        class_name = request.POST.get("class_name")
        ids = request.POST.getlist("tea_id")
        print("----------")
        print(id,class_name,ids)
        try:
            sql = "update t_class set class_name='%s' WHERE id='%s'" % (class_name, id)
            cursor.execute(sql)
            sql = "delete from t_tea_class where tea_id=" + id
            cursor.execute(sql)
            for i in ids:
                sql = "insert into t_tea_class(tea_id,class_id) VALUES ('%s','%s')" % (i, id)
                cursor.execute(sql)
                db.commit()
        except:
            db.rollback()
        return redirect(clainfo)

def classajax(request):
    gid = request.GET.get("gid")
    cursor = db.cursor()
    sql = "select *,GROUP_CONCAT(part.pid) as pids ,GROUP_CONCAT(part.pname) as pnames from grade left join part on find_in_set(part.pid,grade.pid) where gid=" + gid
    cursor.execute(sql)
    result = cursor.fetchone()
    return HttpResponse(json.dumps(result))

def classajax1(request):
    pid = request.GET.get("pid")
    cursor = db.cursor()
    sql = "select t_tea.name,t_tea.id from t_tea left join part on find_in_set(%s,part.pid)"
    cursor.execute(sql,[pid])
    result = cursor.fetchall()
    print("------------result------",result)
    return HttpResponse(json.dumps(result))
'''
1.如何使用递归写树形结构
2.如何点击头像的时候更换
'''




