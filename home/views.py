from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.http import HttpResponse

#Auth and messages
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages

#import models of user profiles
from teacher.models import teacherProfile
from student.models import studentProfile

from django.conf import settings 
from django.core.mail import send_mail
import os
from django.views.decorators.csrf import csrf_exempt

# import string,random


# s1=string.ascii_lowercase
# s2=string.digits
# s3=string.ascii_uppercase
# s=[]
# s.extend(list(s1))
# s.extend(list(s2))
# s.extend(list(s3))


# def otp_generator():
#     random.shuffle(s)
#     return str("".join(s[0:6]))



def home_view(request):
    user=request.user
    if user.is_authenticated:
        return redirect('teacher_home')
    return render(request,'home/index.html',{})


def login_user(request):

    user=request.user
    if user.is_authenticated:
        if "catgory" in request.session:
            catg = request.session["category"]
            if catg=="student":
                return redirect('student_home')
        return redirect('teacher_home')

    if request.method == 'POST':
        femail = request.POST.get('email',"")
        fpassword = request.POST.get('password',"")
        
        all_users = User.objects.all()

        conf_user = authenticate(username=femail,password=fpassword)

        if conf_user:
            login(request,conf_user)

            is_teacher = teacherProfile.objects.filter(email=femail)
            if len(is_teacher)==0:
                is_teacher=0
            else:
                is_teacher=1

            if is_teacher:
                request.session["category"]="teacher"
                return redirect('teacher_home')

            else :
                request.session["category"]="student"
                return redirect('student_home')

        messages.error(request,"Invalid Credentials")
        return redirect(request.path)

    return render(request, 'home/login.html')



def signup_user(request):

    user=request.user
    if user.is_authenticated:
        return redirect('teacher_home')

    if request.method=='POST':
        fname = request.POST.get('firstname',"")
        lname=request.POST.get('lastname',"")
        femail = request.POST.get('emailid',"")
        passw = request.POST.get('password',"")
        confpass = request.POST.get('confirmpassword',"")
        categ = int(request.POST.get('category',""))

        print(categ)
        
        #password didn't match
        if passw!=confpass:
            messages.error(request, "Password did not match.")
            return redirect(request.path)

        #already taken email
        all_users=User.objects.all()

        for user in all_users:
            if user.email==femail:
                messages.error(request, "Email Already taken")
                return redirect(request.path)
        
        curr_user=User.objects.create_user(femail,femail,passw)
        curr_user.first_name=fname
        curr_user.last_name=lname
        curr_user.save()

        if categ==1:
            print("1")
            newTeacher = teacherProfile(firstname=fname,lastname=lname,email=femail,password=passw)
            teacherProfile.save(newTeacher)
        else:
            print("2")
            newStudent = studentProfile(firstname=fname,lastname=lname,email=femail,password=passw)
            studentProfile.save(newStudent)

        user=authenticate(username=femail,password=passw)
        if user:
            login(request,user)
            # email_from = settings.EMAIL_HOST_USER
            # recipient_list = [femail]
            # send_mail(subject,message,email_from,recipient_list)

            # login(request, femail)
            # request.session
            # messages.success(request, "Sign Up successful! Verify Your Email to Continue!")
            if categ==1:
                return redirect('teacher_home')
            return redirect('student_home')
            
    return render(request, 'home/signup.html')



def logout_user(request):
    logout(request)
    if "category" in request.session:
        del request.session["category"]
    return redirect('home_view')
    

def validate_user(request):
    if(request.user.is_authenticated):
        print("user is authenticated")
        try:
            teacher = teacherProfile.objects.get(email=request.user.email)
        except teacherProfile.DoesNotExist:
            teacher = None

        try:
            student = studentProfile.objects.get(email=request.user.email)
        except studentProfile.DoesNotExist:
            student = None

        

        if teacher is not None:
            print('user is a teacher')
            return redirect('teacher_home') #for real purpose redirect to teacher dashboard
        if student is not None:
            print('user is a student')
            print(student.email)
            return redirect('home_view') #for real purpose redirect to student dashboard

        user=request.user
        user.username=user.email
        user.save()

        print("User has not selected its occupation")
        return render(request,'home/occupation.html')
    print("user is not authenticated")
    return redirect('home_view')


    
def student_confirm(request):
    if(request.user.is_authenticated):
        print("user is authenticated")
        try:
            teacher = teacherProfile.objects.get(email=request.user.email)
        except teacherProfile.DoesNotExist:
            teacher = None
        try:
            student = studentProfile.objects.get(email=request.user.email)
        except studentProfile.DoesNotExist:
            student = None
        if teacher is not None:
            print('user is a teacher')
            return redirect('teacher_home') #for real purpose redirect to teacher dashboard
        if student is not None:
            print('user is a student')
            return redirect('logout') #for real purpose redirect to student dashboard
        newStudent = studentProfile(email=request.user.email)
        studentProfile.save(newStudent)
        return redirect('home_view') #for real purpose redirect to student dashboard        
    print("user is not authenticated")
    return redirect('home_view')



def teacher_confirm(request):
    if(request.user.is_authenticated):
        print("user is authenticated")
        try:
            teacher = teacherProfile.objects.get(email=request.user.email)
        except teacherProfile.DoesNotExist:
            teacher = None
        
        if teacher is not None:
            print('user is a teacher')
            return redirect('teacher_home') #for real purpose redirect to teacher dashboard
        
        newTeacher = teacherProfile(email=request.user.email)
        teacherProfile.save(newTeacher)
        
        return redirect('home_view') #for real purpose redirect to student dashboard   
             
    print("user is not authenticated")
    return redirect('home_view')
