from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import *
from .db_utils import run_statement

#First page

def index(req):
    
    #Logout the user if logged 
    if req.session:
        req.session.flush()
    
    return render(req,'index.html')
    
#Login views
    
def managerIndex(req):

    isFailed=req.GET.get("fail",False) #Check the value of the GET parameter "fail"
    
    loginForm=UserLoginForm() #Use Django Form object to create a blank form for the HTML page

    return render(req,'managerLogin.html',{"login_form":loginForm,"action_fail":isFailed})
    
def studentIndex(req):
    
    isFailed=req.GET.get("fail",False) #Check the value of the GET parameter "fail"
    
    loginForm=UserLoginForm() #Use Django Form object to create a blank form for the HTML page

    return render(req,'studentLogin.html',{"login_form":loginForm,"action_fail":isFailed})

def instructorIndex(req):
    
    isFailed=req.GET.get("fail",False) #Check the value of the GET parameter "fail"
    
    loginForm=UserLoginForm() #Use Django Form object to create a blank form for the HTML page

    return render(req,'instructorLogin.html',{"login_form":loginForm,"action_fail":isFailed})
    
def managerLogin(req):

    #Retrieve data from the request body
    username=req.POST["username"]
    password=req.POST["password"]

    result=run_statement(f"SELECT * FROM Database_manager WHERE username='{username}' and password='{password}';") #Run the query in DB

    if result: #If a result is retrieved
        req.session["username"]=username #Record username into the current session
        return HttpResponseRedirect('../registration/managerHome') #Redirect user to home page
    else:
        return HttpResponseRedirect('../registration/managerIndex?fail=true')
    
def studentLogin(req):
    
    #Retrieve data from the request body
    username=req.POST["username"]
    password=req.POST["password"]

    result=run_statement(f"SELECT * FROM Student WHERE username='{username}' and password='{password}';") #Run the query in DB

    if result: #If a result is retrieved
        req.session["username"]=username #Record username into the current session
        return HttpResponseRedirect('../registration/studentHome') #Redirect user to home page
    else:
        return HttpResponseRedirect('../registration/studentIndex?fail=true')

def instructorLogin(req):
    
    #Retrieve data from the request body
    username=req.POST["username"]
    password=req.POST["password"]

    result=run_statement(f"SELECT * FROM Instructor WHERE username='{username}' and password='{password}';") #Run the query in DB

    if result: #If a result is retrieved
        req.session["username"]=username #Record username into the current session
        return HttpResponseRedirect('../registration/toy') #Redirect user to home page
    else:
        return HttpResponseRedirect('../registration/instructorIndex?fail=true')
        
#Home pages
    
def managerHome(req):

    username=req.session["username"]

    return render(req,'managerHome.html', {"username":username})
    
def studentHome(req):
    
    #Retrieve data from the request body
    username=req.POST["username"]
    password=req.POST["password"]

    result=run_statement(f"SELECT * FROM Instructor WHERE username='{username}' and password='{password}';") #Run the query in DB

    if result: #If a result is retrieved
        req.session["username"]=username #Record username into the current session
        return HttpResponseRedirect('../registration/toy') #Redirect user to home page
    else:
        return HttpResponseRedirect('../registration/instructorIndex?fail=true')

def instructorHome(req):
    
    #Retrieve data from the request body
    username=req.POST["username"]
    password=req.POST["password"]

    result=run_statement(f"SELECT * FROM Instructor WHERE username='{username}' and password='{password}';") #Run the query in DB

    if result: #If a result is retrieved
        req.session["username"]=username #Record username into the current session
        return HttpResponseRedirect('../registration/toy') #Redirect user to home page
    else:
        return HttpResponseRedirect('../registration/instructorIndex?fail=true')

#Manager operations

def addStudentPage(req):

    state=req.GET.get("state", "begin")
    username=req.session["username"]

    return render(req, "addStudent.html", {"state":state, "username":username})
    
def addStudent(req):

    logged_user=req.session["username"]
    username=req.POST["username"]
    password=req.POST["password"]
    student_id=req.POST["student_id"]
    name=req.POST["name"]
    surname=req.POST["surname"]
    email=req.POST["email"]
    department_id=req.POST["department_id"]
    
    try:
        run_statement(f"INSERT INTO Student VALUES('{username}', {student_id}, '{department_id}', '{password}', '{name}', '{surname}', '{email}')")
        return HttpResponseRedirect("../managerHome/addStudentPage?state=success")
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect('../managerHome/addStudentPage?state=fail')

    pass
    
def addInstructorPage(req):

    return render(req, "toy.html")
    
def addInstructor(req):

    pass

def deleteStudentPage(req):

    return render(req, "toy.html")
    
def deleteStudent(req):

    pass

def toy(req):
    return render(req, "toy.html")