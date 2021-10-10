from django.db import reset_queries
from django.shortcuts import render, HttpResponse,redirect
from datetime import datetime
from WebApp.models import TODO, Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate,login
from django.contrib.auth.forms import UserCreationForm
from .forms import Registrationform, TODOForm


# Create your views here.
def index(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")

def contact(request):
    if request.method == "POST":
        name =request.POST.get('name')
        email =request.POST.get('email')
        phone =request.POST.get('phone')
        desc =request.POST.get('desc')
        contact = Contact(name=name, email=email, phone=phone, desc=desc, date=datetime.now())
        contact.save()
        messages.success(request, 'Message has been sent.')
    
    return render(request, "contact.html")

def signin(request):
    if request.method == "POST":
         username =request.POST.get('username')
         password = request.POST.get('password')
         user = authenticate(username= username , password=password)
         if user is not None:
             login(request,user)
             return redirect("/loggedin")
         else:
             messages.success(request, 'Wrong Credentials.')
             return render(request, "signin.html")  
    return render(request, "signin.html")

def signup(request):
    if request.method == "POST":
        form = Registrationform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created please signin.')
        else:
            messages.success(request, 'Something went wrong.')
            return redirect("/signup")
    else:
        form=Registrationform()
    return render(request, "signup.html",{"form":form})

def signout(request):
    logout(request)
    return redirect("/")

def loggedin(request):
    if request.user.is_anonymous:
        return redirect("/signin")
    
    if request.user.is_authenticated:
        user=request.user
        form =TODOForm()
        todos=TODO.objects.filter(user=user).order_by('-priority')
    return render(request, "loggedin.html",{'form':form, 'todos':todos})
 
def add_todo(request):
    if request.user.is_authenticated:
        user=request.user
        form = TODOForm(request.POST)
        if form.is_valid():
            todo=form.save(commit=False)
            todo.user=user
            todo.save()
            return redirect("/loggedin")
        else:
            return render(request, 'loggedin.html',{'form':form})

def delete_todo(request , id):
    TODO.objects.get(pk=id).delete()
    return redirect('/loggedin')

def change_status(request , id, status):
    todo=TODO.objects.get(pk=id)
    todo.status = status
    todo.save()
    return redirect('/loggedin')