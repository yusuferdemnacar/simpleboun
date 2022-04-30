from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import *
from .db_utils import run_statement

# Create your views here.

def index(req):
    
    #Logout the user if logged 
    if req.session:
        req.session.flush()
    
    return render(req,'index.html')
    
def managerLogin(req):

    isFailed=req.GET.get("fail",False) #Check the value of the GET parameter "fail"
    
    loginForm=UserLoginForm() #Use Django Form object to create a blank form for the HTML page

    return render(req,'managerLogin.html',{"login_form":loginForm,"action_fail":isFailed})
    
def studentLogin(req):
    
    isFailed=req.GET.get("fail",False) #Check the value of the GET parameter "fail"
    
    loginForm=UserLoginForm() #Use Django Form object to create a blank form for the HTML page

    return render(req,'studentLogin.html',{"login_form":loginForm,"action_fail":isFailed})

def instructorLogin(req):
    
    isFailed=req.GET.get("fail",False) #Check the value of the GET parameter "fail"
    
    loginForm=UserLoginForm() #Use Django Form object to create a blank form for the HTML page

    return render(req,'instructorLogin.html',{"login_form":loginForm,"action_fail":isFailed})