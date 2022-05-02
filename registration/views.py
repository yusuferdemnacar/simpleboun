from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import *
from .db_utils import run_statement
import mysql.connector
import environ

env = environ.Env()
environ.Env.read_env()

connection = mysql.connector.connect(
  host=env("MYSQL_HOST"),
  user=env("MYSQL_USER"),
  password=env("MYSQL_PASSWORD"),
  database=env("MYSQL_DATABASE"),
  auth_plugin='mysql_native_password'
)

cursor=connection.cursor()

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

    cursor.execute(f"SELECT * FROM Database_manager WHERE username='{username}' and password='{password}';") #Run the query in DB

    result=cursor.fetchall()
    
    connection.commit()

    if result: #If a result is retrieved
        req.session["username"]=username #Record username into the current session
        return HttpResponseRedirect('../registration/managerHome') #Redirect user to home page
    else:
        return HttpResponseRedirect('../registration/managerIndex?fail=true')
    
def studentLogin(req):
    
    #Retrieve data from the request body
    username=req.POST["username"]
    password=req.POST["password"]

    cursor.execute(f"SELECT * FROM Student WHERE username='{username}' and password='{password}';") #Run the query in DB

    result=cursor.fetchall()

    connection.commit()

    if result: #If a result is retrieved
        req.session["username"]=username #Record username into the current session
        return HttpResponseRedirect('../registration/studentHome') #Redirect user to home page
    else:
        return HttpResponseRedirect('../registration/studentIndex?fail=true')

def instructorLogin(req):
    
    #Retrieve data from the request body
    username=req.POST["username"]
    password=req.POST["password"]
    
    cursor.execute(f"SELECT * FROM Instructor WHERE username='{username}' and password='{password}';") #Run the query in DB

    result=cursor.fetchall()

    connection.commit()

    if result: #If a result is retrieved
        req.session["username"]=username #Record username into the current session
        return HttpResponseRedirect('../registration/instructorHome') #Redirect user to home page
    else:
        return HttpResponseRedirect('../registration/instructorIndex?fail=true')
        
#Home pages
    
def managerHome(req):

    username=req.session["username"]

    return render(req,'managerHome.html', {"username":username})
    
def studentHome(req):
    
    username=req.session["username"]

    return render(req,'studentHome.html', {"username":username})

def instructorHome(req):
    
    username=req.session["username"]

    return render(req,'instructorHome.html', {"username":username})

# Manager operations

# Add student to the database

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
        cursor.execute(f"INSERT INTO Student VALUES('{username}', {student_id}, '{department_id}', '{password}', '{name}', '{surname}', '{email}')")
        result=cursor.fetchall()
        connection.commit()
        return HttpResponseRedirect("../managerHome/addStudentPage?state=success")
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect('../managerHome/addStudentPage?state=fail')
        
# Add instructor to the database
    
def addInstructorPage(req):

    state=req.GET.get("state", "begin")
    username=req.session["username"]

    return render(req, "addInstructor.html", {"state":state, "username":username})
    
def addInstructor(req):

    logged_user=req.session["username"]
    username=req.POST["username"]
    password=req.POST["password"]
    title=req.POST["title"]
    name=req.POST["name"]
    surname=req.POST["surname"]
    email=req.POST["email"]
    department_id=req.POST["department_id"]
    
    try:
        cursor.execute(f"insert into Instructor values('{username}','{department_id}','{title}','{password}','{name}','{surname}','{email}')")
        result=cursor.fetchall()
        connection.commit()

        cursor.execute(f"insert into Lecturer_at values('{username}','{department_id}')")
        result=cursor.fetchall()
        connection.commit()
        return HttpResponseRedirect("../managerHome/addInstructorPage?state=success")
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect('../managerHome/addInstructorPage?state=fail')
        
# Remove student from database

def deleteStudentPage(req):

    state=req.GET.get("state", "begin")
    username=req.session["username"]

    return render(req, "deleteStudent.html", {"state":state, "username":username})
    
def deleteStudent(req):

    logged_user=req.session["username"]
    student_id=req.POST["student_id"]
    
    cursor.execute(f"DELETE FROM Student WHERE student_id = {student_id}")
    result=cursor.fetchall()
    connection.commit()

    if cursor.rowcount:
        return HttpResponseRedirect("../managerHome/deleteStudentPage?state=success")
    else:
        return HttpResponseRedirect('../managerHome/deleteStudentPage?state=fail')

# View all instructors

def viewInstructorsPage(req):

    cursor.execute("SELECT username, name, surname, email, department_id, title FROM Instructor")
    result=cursor.fetchall()
    connection.commit()
    
    return render(req, "viewInstructors.html", {"results":result})

# View all students in ascending order of completed credits

def viewStudentsPage(req):

    cursor.execute("SELECT username, S.name, S.surname, email, department_id, SUM(credits), SUM(credits*grade)/SUM(credits) FROM (Student S INNER JOIN Grade G ON S.student_id = G.student_id) INNER JOIN Course C ON G.course_id = C.course_id GROUP BY username ORDER BY SUM(credits) ASC;")
    result=cursor.fetchall()
    connection.commit()
    
    return render(req, "viewStudents.html", {"results":result})
    
# View all grades of a student

def viewGradesPage(req):

    student_id=req.GET.get("student_id", 0)
    
    result=[]

    if student_id:
        cursor.execute(f"SELECT G.course_id, name, grade FROM Grade G INNER JOIN Course C ON (G.course_id = C.course_id) WHERE student_id = '{student_id}'")
        result=cursor.fetchall()
        connection.commit()
    
    return render(req, "viewGrades.html", {"results":result, "student_id":student_id})

#View all courses of an instructor

def viewCoursesInsPage(req):
    
    username=req.GET.get("username", 0)
    
    result=[]

    if username:
        cursor.execute(f"SELECT C.course_id, C.name, R.classroom_id, campus, slot FROM ((Course C INNER JOIN Schedule S ON C.course_id = S.course_id) INNER JOIN Classroom R ON S.classroom_id = R.classroom_id) INNER JOIN Lectured_by L ON L.course_id = C.course_id WHERE L.username = '{username}'")
        result=cursor.fetchall()
        connection.commit()
    
    return render(req, "viewCoursesIns.html", {"results":result, "username":username})
    
#View average grade of a course

def viewAvgGradePage(req):
    
    course_id=req.GET.get("course_id", 0)
    
    result=[]

    if course_id:
        cursor.execute(f"SELECT C.course_id, C.name, AVG(grade) FROM Course C INNER JOIN Grade G ON C.course_id = G.course_id WHERE C.course_id = '{course_id}' GROUP BY C.course_id")
        result=cursor.fetchall()
        connection.commit()
    
    return render(req, "viewAvgGrades.html", {"results":result, "course_id":course_id})
    
#Update title of an instructor

def updateTitlePage(req):

    state=req.GET.get("state", "begin")
    username=req.session["username"]

    return render(req, "updateTitle.html", {"state":state, "username":username})

def updateTitle(req):

    logged_user=req.session["username"]
    username=req.POST["username"]
    new_title=req.POST["title"]
    
    try:
        cursor.execute(f"UPDATE Instructor SET title = '{new_title}' WHERE username = '{username}'")
        result=cursor.fetchall()
        connection.commit()
        
        if cursor.rowcount:
            return HttpResponseRedirect("../managerHome/updateTitlePage?state=success")
        else:
            return HttpResponseRedirect('../managerHome/updateTitlePage?state=fail')
            
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect('../managerHome/updateTitlePage?state=fail')
        
# Instructor Operations

def viewMyStudentsPage(req):
    
    course_id=req.GET.get("course_id", 0)
    username=req.session["username"]
    
    result=[]

    if course_id:
        cursor.execute(f"SELECT S.username, S.student_id, S.email, S.name, S.surname FROM (Enrolled E INNER JOIN Lectured_by L ON E.course_id = L.course_id) INNER JOIN Student S ON E.student_id = S.student_id WHERE E.course_id = '{course_id}' AND L.username = '{username}'")
        result=cursor.fetchall()
        connection.commit()
    
    return render(req, "viewMyStudents.html", {"results":result, "course_id":course_id})

def toy(req):
    return render(req, "toy.html")