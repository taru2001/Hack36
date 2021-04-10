from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.http import HttpResponse

#Auth and messages
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import teacherProfile



def teacher_home_view(request):
    user = request.user
    if user.is_authenticated:
        curr_user=teacherProfile.objects.get(email=user.email)
        # print(curr_user.id)
        return render(request, 'teacher/dashboard.html',{'user':curr_user})

    messages.error(request,"Login First")
    return redirect('login_page')



def teacher_profile(request):
    user = request.user
    if user.is_authenticated:
        curr_user = teacherProfile.objects.get(email=user.email)
        user_tags = curr_user.tagline

        tag_list=[]
        currword=""
        spcount=0
        for ch in user_tags:
            if ch==' ':
                spcount+=1
        
            if spcount>4:
                tag_list.append(currword)
                spcount=0
                currword=""
            else:
                currword+=ch
        currword+='  "'
        tag_list.append(currword)

        return render(request, 'teacher/teacher_profile.html', {'user':curr_user,'word_list':tag_list})

    messages.error(request,"Login First")
    return redirect('login_page')



def editProfile(request):
    user=request.user
    if user.is_authenticated:
        # print("hello")
        if request.method=='POST':
            fname = request.POST.get('firstname',"")
            lname = request.POST.get('lastname',"")
            passw = request.POST.get('password',"")
            st = request.POST.get('state',"")
            coun = request.POST.get('country',"")
            profPic = request.FILES.get('profilePic',"")
            addr = request.POST.get('address',"")
            tagl  = request.POST.get('tagline',"")

            # if len(passw)==0:
            #     passw=otp_generator()
            # print(passw)
            curr_user = teacherProfile.objects.get(email=user.email)
            ori_password=curr_user.password

            curr_user.firstname=fname
            curr_user.lastname=lname
            curr_user.password=passw
            curr_user.state=st
            curr_user.country=coun
            curr_user.address=addr
            curr_user.tagline=tagl
            

            if len(profPic):
                curr_user.profileImage=profPic
            curr_user.save()

            if ori_password==passw:
                return redirect('login_page')

            user.first_name=fname
            user.last_name=lname
            user.set_password(passw)
            user.save()

        # messages.success(request, {'msg':"Details updated successfully" , })
        
            user=authenticate(username=user.email,password=passw)
            login(request,user)
            return redirect('login_page')

    messages.error(request,"Login in First")
    return redirect('login_page')
