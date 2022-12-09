from django.shortcuts import render,HttpResponse
from .models import Employee, Role,Department
from datetime import datetime
from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers
from emp_app.serializers import  UserSerializer

# Create your views here.
def index(request):
    return render(request, 'index.html')


def all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps':emps
    }

    # for a in emps:
    #    print(a.salary)
 
    # print(emps)
    return render(request, 'view_all_emp.html' , context)

def add_emp(request):
    if request.method == 'POST':
      first_name = request.POST.get('first_name')
      last_name = request.POST.get('last_name')
      salary = int(request.POST.get('salary')) 
      dept =   request.POST.get('dept')
      role = int(request.POST.get('role')) 
      bonus = int(request.POST.get('bonus'))
      phone = int(request.POST.get('phone')) 
      
      new_emp = Employee(first_name=first_name, last_name=last_name, salary=salary,dept_id=dept, role_id = role, hire_date = datetime.now())
      new_emp.save()
      return HttpResponse("Employee added")
    elif request.method == 'GET':
        return render(request, 'add_emp.html')
    else:
        return HttpResponse("An Exception Occur")

    return render(request, 'add_emp.html')

def remove_emp(request, emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id= emp_id)
            emp_to_be_removed.delete()
        except:
            return HttpResponse("Please Enter a valid Emp Id")
    emps = Employee.objects.all()
    context = {
        'emps':emps
    }
    return render(request, 'remove_emp.html',context)

def filter_emp(request):
    if request.method == 'POST':
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']
        emps = Employee.objects.all()
        if name:
            emps = emps.filter(Q(first_name__icontains = name) | Q(last_name__icontains = name))
        if dept:
            emps = emps.filter(dept__name__icontains = dept)
        if role:
            emps = emps.filter(role__name__icontains = role)
        context = {
            'emps':emps
        }
        return render(request, 'view_all_emp.html', context)
    elif request.method == 'GET':
        return render(request, 'filter_emp.html')
    else:
        return HttpResponse("An Exception Occured")


    return render(request, 'filter_emp.html')

class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data = request.data)

        if not serializer.is_valid():
            return Response({'status' : 403 , 'errors' : serializer.errors , 'message' : 'Something wents wrong'})

        serializer.save()

        user = User.objects.get(username = serializer.data['username'])
        token_obj , _ = Token.objects.get_or_create(user=user)


        return Response({'status' : 200 , 'payload' : serializer.data , 'token' : str(token_obj),  'message' : 'your data is saved'})






