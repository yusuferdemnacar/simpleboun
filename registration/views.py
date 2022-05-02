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

    cursor.execute("SELECT username, name, surname, email, department_id, completed_credits, gpa FROM Student ORDER BY completed_credits ASC;")
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

#View my students

def viewMyStudentsPage(req):
    
    course_id=req.GET.get("course_id", 0)
    username=req.session["username"]
    
    result=[]

    if course_id:
        cursor.execute(f"SELECT S.username, S.student_id, S.email, S.name, S.surname FROM (Enrolled E INNER JOIN Lectured_by L ON E.course_id = L.course_id) INNER JOIN Student S ON E.student_id = S.student_id WHERE E.course_id = '{course_id}' AND L.username = '{username}'")
        result=cursor.fetchall()
        connection.commit()
    
    return render(req, "viewMyStudents.html", {"results":result, "course_id":course_id})

#View available classrooms

def viewClassroomsPage(req):
    
    slot=req.GET.get("slot", 0)
    
    result=[]

    if slot:
        cursor.execute(f"SELECT R.classroom_id, R.campus, R.capacity FROM Classroom R WHERE R.classroom_id NOT IN ( SELECT C.classroom_id FROM Classroom C INNER JOIN Plan P ON P.classroom_id = C.classroom_id WHERE P.slot = {slot})")
        result=cursor.fetchall()
        connection.commit()
    
    return render(req, "viewClassrooms.html", {"results":result, "slot":slot})
    
#Add course

def createCoursePage(req):

    state=req.GET.get("state", "begin")

    return render(req, "createCourse.html", {"state":state})
    
def createCourse(req):

    username=req.session["username"]
    name=req.POST["name"]
    course_id=req.POST["course_id"]
    classroom_id=req.POST["classroom_id"]
    slot=req.POST["slot"]
    credits=req.POST["credit"]
    quota=req.POST["quota"]
    
    try:
        cursor.execute(f"INSERT INTO Course VALUES('{course_id}','{name}',{credits},{quota});")
        cursor.execute(f"INSERT INTO Lectured_by VALUES('{course_id}','{username}');")
        cursor.execute(f"INSERT INTO Plan VALUES('{classroom_id}',{slot});")
        cursor.execute(f"INSERT INTO Schedule VALUES('{classroom_id}',{slot},'{course_id}');")
        result=cursor.fetchall()
        connection.commit()
        
        return HttpResponseRedirect("../instructorHome/createCoursePage?state=success")
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect('../instructorHome/createCoursePage?state=fail')

#Add prerequisite

def addPrerequisitePage(req):

    state=req.GET.get("state", "begin")

    return render(req, "addPrerequisite.html", {"state":state})
    
def addPrerequisite(req):

    course_id=req.POST["course_id"]
    prerequisite_id=req.POST["prerequisite_id"]
    username=req.session["username"]
    
    cursor.execute(f"SELECT username FROM Lectured_by L WHERE L.course_id = '{course_id}' AND L.username = '{username}';")
    result=cursor.fetchall()
    
    if len(result) == 0:
        print("no such course given by you")
        return HttpResponseRedirect('../instructorHome/addPrerequisitePage?state=fail')
    
    try:
        cursor.execute(f"INSERT INTO Prerequisite VALUES('{course_id}','{prerequisite_id}');")
        result=cursor.fetchall()
        connection.commit()
        
        return HttpResponseRedirect("../instructorHome/addPrerequisitePage?state=success")
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect('../instructorHome/addPrerequisitePage?state=fail')
        
#Update course name

def updateCourseNamePage(req):

    state=req.GET.get("state", "begin")

    return render(req, "updateCourseName.html", {"state":state})
    
def updateCourseName(req):

    course_id=req.POST["course_id"]
    course_name=req.POST["course_name"]
    username=req.session["username"]
    
    cursor.execute(f"SELECT username FROM Lectured_by L WHERE L.course_id = '{course_id}' AND L.username = '{username}';")
    result=cursor.fetchall()
    
    if len(result) == 0:
        print("no such course given by you")
        return HttpResponseRedirect('../instructorHome/updateCourseNamePage?state=fail')
    
    try:
        cursor.execute(f"UPDATE Course SET name = '{course_name}' WHERE course_id = '{course_id}';")
        result=cursor.fetchall()
        connection.commit()
        
        return HttpResponseRedirect("../instructorHome/updateCourseNamePage?state=success")
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect('../instructorHome/updateCourseNamePage?state=fail')

#View my courses

def viewMyCoursesPage(req):

    username=req.session["username"]

    cursor.execute(f"SELECT C.course_id, C.name, S.classroom_id, S.slot, C.quota, GROUP_CONCAT(P.prerequisite_id) FROM ((Course C INNER JOIN Schedule S ON C.course_id = S.course_id) INNER JOIN Lectured_by L ON L.course_id = C.course_id) LEFT OUTER JOIN Prerequisite P ON P.course_id = C.course_id WHERE L.username = '{username}' GROUP BY C.course_id ORDER BY C.course_id ASC;")
    result=cursor.fetchall()
    connection.commit()
    
    return render(req, "viewMyCourses.html", {"results":result})
    
#Grade a student

def gradeStudentPage(req):

    state=req.GET.get("state", "begin")

    return render(req, "gradeStudent.html", {"state":state})

def gradeStudent(req):

    course_id=req.POST["course_id"]
    student_id=req.POST["student_id"]
    grade=req.POST["grade"]
    username=req.session["username"]
    
    cursor.execute(f"SELECT student_id FROM Enrolled E INNER JOIN Lectured_by L ON E.course_id = L.course_id WHERE E.student_id = {student_id} AND L.username = '{username}' AND E.course_id = '{course_id}';")
    result=cursor.fetchall()
    
    if len(result) == 0:
        print("no such course given by you or no such student taking this course")
        return HttpResponseRedirect('../instructorHome/gradeStudentPage?state=fail')
    
    try:
        cursor.execute(f"INSERT INTO Grade VALUES({grade},{student_id},'{course_id}');")
        cursor.execute(f"DELETE FROM Enrolled E WHERE E.student_id = {student_id} AND E.course_id = '{course_id}';")
        result=cursor.fetchall()
        connection.commit()
        
        return HttpResponseRedirect("../instructorHome/gradeStudentPage?state=success")
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect('../instructorHome/gradeStudentPage?state=fail')

# Student Operations

#View my courses

def viewCoursesStuPage(req):

    username=req.session["username"]
    
    cursor.execute(f"SELECT S.student_id FROM Student S WHERE S.username='{username}'")
    stu_id=cursor.fetchall()
    student_id=stu_id[0][0]
    connection.commit()

    cursor.execute(f"SELECT C.course_id, C.name, G.grade FROM (Enrolled E INNER JOIN Course C ON E.course_id = C.course_id) LEFT OUTER JOIN Grade G ON G.course_id = E.course_id WHERE E.student_id = {student_id};")
    present_courses=cursor.fetchall()
    connection.commit()
    
    cursor.execute(f"SELECT C.course_id, C.name, G.grade FROM Grade G INNER JOIN Course C ON G.course_id = C.course_id WHERE G.student_id = {student_id};")
    taken_courses=cursor.fetchall()
    connection.commit()
    
    return render(req, "viewCoursesStu.html", {"results":present_courses+taken_courses})

def toy(req):
    return render(req, "toy.html")