from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #login urls
    
    ##instructor login
    path('instructorIndex', views.instructorIndex, name="instructorIndex"),
    path('instructorLogin', views.instructorLogin, name="instructorLogin"),
    
    ##student login
    path('studentIndex', views.studentIndex, name="studentIndex"),
    path('studentLogin', views.studentLogin, name="studentLogin"),
    
    ##manager login
    path('managerIndex', views.managerIndex, name="managerIndex"),
    path('managerLogin', views.managerLogin, name="managerLogin"),
    
    #home page urls
    path('studentHome', views.studentHome, name="studentHome"),
    path('managerHome', views.managerHome, name="managerHome"),
    path('instructorHome', views.instructorHome, name="instructorHome"),
    
    #manager urls
    
    ##add student
    path('managerHome/addStudentPage', views.addStudentPage, name="managerHome/addStudentPage"),
    path('managerHome/addStudent', views.addStudent, name="managerHome/addStudent"),
    
    ##add instructor
    path('managerHome/addInstructorPage', views.addInstructorPage, name="managerHome/addInstructorPage"),
    path('managerHome/addInstructor', views.addInstructor, name="managerHome/addInstructor"),
    
    ##delete student
    path('managerHome/deleteStudentPage', views.deleteStudentPage, name="managerHome/deleteStudentPage"),
    path('managerHome/deleteStudent', views.deleteStudent, name="managerHome/deleteStudent"),
    
    ##view instructors
    path('managerHome/viewInstructorsPage', views.viewInstructorsPage, name="managerHome/viewInstructorsPage"),
    
    ##view students
    path('managerHome/viewStudentsPage', views.viewStudentsPage, name="managerHome/viewStudentsPage"),
    
    ##view grades
    path('managerHome/viewGradesPage', views.viewGradesPage, name="managerHome/viewGradesPage"),
    
    ##view courses of instructor
    path('managerHome/viewCoursesInsPage', views.viewCoursesInsPage, name="managerHome/viewCoursesInsPage"),
    
    ##view avg grade of a course
    path('managerHome/viewAvgGradePage', views.viewAvgGradePage, name="managerHome/viewAvgGradePage"),
    
    ##update the title of an instructor
    path('managerHome/updateTitlePage', views.updateTitlePage, name="managerHome/updateTitlePage"),
    path('managerHome/updateTitle', views.updateTitle, name="managerHome/updateTitle"),
    
    #instructor urls
    
    ##view my students
    path('instructorHome/viewMyStudentsPage', views.viewMyStudentsPage, name="instructorHome/viewMyStudentsPage"),
    
    ##view available classrooms
    path('instructorHome/viewClassroomsPage', views.viewClassroomsPage, name="instructorHome/viewClassroomsPage"),
    
    ##add course
    path('instructorHome/createCoursePage', views.createCoursePage, name="instructorHome/createCoursePage"),
    path('instructorHome/createCourse', views.createCourse, name="instructorHome/createCourse"),
    
    ##add prerequisite
    path('instructorHome/addPrerequisitePage', views.addPrerequisitePage, name="instructorHome/addPrerequisitePage"),
    path('instructorHome/addPrerequisite', views.addPrerequisite, name="instructorHome/addPrerequisite"),
    
    ##update name of a course
    path('instructorHome/updateCourseNamePage', views.updateCourseNamePage, name="instructorHome/updateCourseNamePage"),
    path('instructorHome/updateCourseName', views.updateCourseName, name="instructorHome/updateCourseName"),
    
    ##view my courses
    path('instructorHome/viewMyCoursesPage', views.viewMyCoursesPage, name="instructorHome/viewMyCoursesPage"),
    
    ##update name of a course
    path('instructorHome/gradeStudentPage', views.gradeStudentPage, name="instructorHome/gradeStudentPage"),
    path('instructorHome/gradeStudent', views.gradeStudent, name="instructorHome/gradeStudent"),
    
    ##view available classrooms
    path('studentHome/viewCoursesStuPage', views.viewCoursesStuPage, name="studentHome/viewCoursesStuPage"),
    
    ##view all courses
    path('studentHome/viewAllCoursesPage', views.viewAllCoursesPage, name="studentHome/viewAllCoursesPage"),
    
    ##add student
    path('studentHome/addCoursePage', views.addCoursePage, name="studentHome/addCoursePage"),
    path('studentHome/addCourse', views.addCourse, name="studentHome/addCourse"),
    
    path('toy', views.toy, name="toy")
]
