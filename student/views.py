from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.http import HttpResponse

#Auth and messages
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import studentProfile
from  teacher.models import teacherProfile,Follower,Following

from courses.models import Course,Video
import json



def student_home_view(request):
    print("hello student")
    user = request.user
    if user.is_authenticated:
        print(user.email)
        curr_user=studentProfile.objects.get(email=user.email)
        # print(curr_user.id)

        all_following_obj = Following.objects.filter(student=curr_user)
        
        users_following=[]

        if all_following_obj:
            users_following = all_following_obj[0].teachers.all()

        all_courses=Course.objects.all()
        feed_vids=[]

        for i in all_courses:
            if i.teacher in users_following:
                courseid=i.id
                videos_obj = Video.objects.filter(course_id=courseid)

                for j in videos_obj:
                    feed_vids.append(j)

        for i in feed_vids:
            print(i)

        return render(request, 'student/dashboard.html',{'user':curr_user,'feed_vids':feed_vids})

    messages.error(request,"Login First")
    return redirect('login_page')


def isUserMatching(str1 , str2):
    #Filters user based on search
    m = len(str1) 
    n = len(str2) 
      
    j = 0   
    i = 0   
      
    while j<m and i<n: 
        if str1[j] == str2[i]:     
            j = j+1    
        i = i + 1
          
    # If all characters of str1 matched, then j is equal to m 
    return j==m



def student_result(request):
    print("hello")
    user = request.user
    if user.is_authenticated:
        curr_user=studentProfile.objects.get(email=user.email)
        # print(curr_user.id)
        name = request.POST.get('search')
        print(name)
        teachers = teacherProfile.objects.all()
        mylist = []
        for i in teachers:
            if isUserMatching(i.firstname,name) or isUserMatching(i.lastname,name) or isUserMatching(name, i.lastname) or isUserMatching(name, i.firstname):
                            mylist.append(i)           
        return render(request, 'student/result.html',{'teachers':mylist})

    messages.error(request,"Login First")
    return redirect('login_page')


def student_profile(request):
    user = request.user
    if user.is_authenticated:
        curr_user = studentProfile.objects.get(email=user.email)
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

        return render(request, 'student/profile.html', {'user':curr_user,'word_list':tag_list})

    messages.error(request,"Login First")
    return redirect('login_page')




def searched_teacher_view(request,teacher_id):
    user=request.user
    if user.is_authenticated:
        curr_teacher=teacherProfile.objects.filter(id=teacher_id)
        if not curr_teacher:
            return redirect('login_page')

        curr_teacher=curr_teacher[0]
        curr_student = studentProfile.objects.get(email=user.email)
        follower = Follower.objects.filter(teacher=curr_teacher,students=curr_student)       

        if  not follower:
            follower=0
        else:
            follower=1

        return render(request, 'student/searchedteacher.html',{'id':teacher_id,'curr_teacher':curr_teacher,'follower':follower})

    return redirect('login_page')



def handlefollow(request,*args):
    
    user=request.user
    if user.is_authenticated:
        teacher_id=request.GET.get('teacher_id')
        print(teacher_id)
        curr_teacher = teacherProfile.objects.filter(id=teacher_id)

        if len(curr_teacher)==0:
            return redirect('login_page')

        curr_teacher=curr_teacher[0]
        curr_user = studentProfile.objects.get(email=user.email)

        is_followed = Following.objects.filter(student=curr_user,teachers=curr_teacher)

        if is_followed:
            print("unfollow")
            Following.unfollow(curr_user, curr_teacher)
            Follower.unfollow(curr_teacher, curr_user)
        else:
            print("follow")
            Follower.follow(curr_teacher, curr_user)
            Following.follow(curr_user, curr_teacher)
        print("heelo")
        rep={

        }
        response=json.dumps(rep)

        return HttpResponse(response,content_type='application/json')

    return redirect('login_page')