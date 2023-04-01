from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreateUserForm, addTaskForm
import cx_Oracle
import pandas as pd
from user import user
from tasks import task
from user_list import userList


cx_Oracle.init_oracle_client(lib_dir=r"D:/Oracle_libraries/instantclient_21_8")

def connection():
    conn = cx_Oracle.connect(user='TIMI', password='BananaBanana', dsn="localhost/xepdb1")
    return conn


def index(request):
    return render(request,'index.html')

def register(request):
    return render(request,'register.html')

def my_login(request):
    return render(request,'my-login.html')

def dashboard(request):
    return render(request,'dashboard.html')

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('User registered successfully!')
    context = {'form':form}
    return render(request,'register.html',context=context) 

def addtask(request):
    if request.method == 'GET':
        return render(request, 'addtask.html', {'task':{}})
    if(request.method == 'POST'):
        form = addTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            difficulty = form.cleaned_data['difficulty']
            deadline = form.cleaned_data['deadline']
            visibility = form.cleaned_data['visibility']
            task_type = form.cleaned_data['task_type']
            username = form.cleaned_data['username']
            new_task = task(title, description, visibility, difficulty, deadline, task_type)

            for person in userList.users:
                if person.username == username:
                    person.addTask(new_task)
            # addTasks(title, description, difficulty, deadline, duration, task_type, username)
    
    return redirect('listtasks')


def listtasks(request):
    conn=connection()
    cursor = conn.cursor()
    sqlTxt = 'SELECT * FROM Tasks'
    tasks=[]
    cursor.execute(sqlTxt)
    for row in cursor.fetchall():
        tasks.append({"title": row[0], "description": row[1], "difficulty": row[2], "deadline": row[3], "duration": row[4], "task_type": row[5], "username": row[6]})
    conn.close()
    return render(request, 'listtasks.html', {'tasks': tasks})


