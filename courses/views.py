from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.http import HttpResponse
import json

#Auth and messages
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
import json


from .models import Course,Video
from teacher.models import teacherProfile,Follower

from student.models import studentProfile


from home.models import Notification

# Create your views here.


def course_form(request):
    user=request.user
    if user.is_authenticated:
        if request.method=='POST':
            courname = request.POST.get('coursename',"")
            desc = request.POST.get('description',"")
            thumbnl = request.FILES.get('coursethumb',"")
            
            curr_teacher = teacherProfile.objects.get(email=user.email)
            if len(thumbnl)!=0:
                newCourse = Course(name=courname,teacher=curr_teacher,description=desc,thumbnail=thumbnl)
            else:
                newCourse = Course(name=courname,teacher=curr_teacher,description=desc)

            Course.save(newCourse)
            
            return redirect('login_page')

        return render(request , 'courses/form.html')
    
    messages.error(request,"Login First")
    return redirect('login_page')



def teacher_courses(request,teacher_id):
    user=request.user
    if user.is_authenticated:
        
        curr_teacher = teacherProfile.objects.filter(id=teacher_id)
        if len(curr_teacher)==0:
            return redirect('login_page')

        curr_teacher=curr_teacher[0]
        curr_teacher_courses = Course.objects.filter(teacher=curr_teacher)

    
        courses = []
        tot=len(curr_teacher_courses)
        tot_slide=int(tot/3)
        var=0
        curr=[]
        

        for i in curr_teacher_courses:
            # print("hi")
            var+=1
            curr.append(i)
            if var==3:
                courses.append(curr)
                curr=[]
                var=0

        if var<3 and var>0:
            # curr.append(-1)
            # curr.append(-1)
            courses.append(curr)
        # for i in courses:
        #     for j in i:
        #         print(j)

        # print(courses[0][0].name)

            
        return render(request, 'courses/courses.html',{'all_courses':courses,'tot_slide':tot_slide} )
        
            
    messages.error(request,"Login First")
    return redirect('home_view')


def seecourse(request,course_id):
    user=request.user
    if user.is_authenticated:
        
        curr_course = Course.objects.filter(id=course_id)
        
        tot=len(curr_course)
        if tot==0:
            return redirect('teacher_home')

        # print(course_id)

        curr_course=curr_course[0]
        teacher_id = curr_course.teacher.id

        vids = Video.objects.filter(course_id=curr_course)

        var=0
        curr=[]
        
        course_videos=[]

        for i in vids:
            # print("hi")
            var+=1
            curr.append(i)
            if var==2:
                course_videos.append(curr)
                curr=[]
                var=0

        if var:
            course_videos.append(curr)

        for i in course_videos:
            print(i)


        return render(request , 'courses/seecourse.html',{'tid':teacher_id,'id':course_id , 'videos':course_videos } )


    messages.error(request,"Login First")
    return redirect('login_page')



def addvideo(request,course_id):

    user=request.user
    if user.is_authenticated:

        curr_course = Course.objects.filter(id=course_id)
        if len(curr_course)==0:
            return redirect('login_page')

        curr_course=curr_course[0]
        if curr_course.teacher.email!=user.email:
            return redirect('login_page')

        if request.method=='POST':

            vid_title = request.POST.get('videotitle',"")
            desc = request.POST.get('description',"")
            video_thumbnail = request.FILES.get('videothumb',"")
            vid = request.FILES.get('video',"")

            if len(video_thumbnail)==0 or len(vid)==0:
                return redirect('login_page')

            newVideo = Video(course_id=curr_course,title=vid_title,description=desc,vid_thumbnail=video_thumbnail,video=vid)
            Video.save(newVideo)


            # Get followers list and send them new video notification
            curr_user = teacherProfile.objects.get(email=user.email)
            user_followers_obj=Follower.objects.filter(teacher=curr_user)
            user_followers=[]
            if user_followers_obj:
                user_followers=user_followers_obj[0].students.all()
            for i in user_followers:
                msg=curr_user.firstname+" added a new video to the course : "+str(curr_course.name)
                auth_i = User.objects.get(username=i.email)
                newNotify = Notification(user=auth_i,message=msg)
                print(i)
                Notification.save(newNotify)


            return HttpResponseRedirect(reverse('teacher_course',kwargs={'teacher_id':curr_course.teacher.id}) )

        return render(request , 'courses/addvideo.html',{'id':course_id})

    messages.error(request,"Login First")
    return redirect('login_page')



def see_video(request,video_id):
    user = request.user
    print(video_id)
    if user.is_authenticated:
        curr_video = Video.objects.filter(id = video_id)

        if len(curr_video) == 0:
            return redirect('login_page')
        
        curr_video = curr_video[0]

        tot_like=curr_video.likes.count()
        print(tot_like)

        tot_dislike = curr_video.dislikes.count()
        print(tot_dislike)

        is_liked = curr_video.likes.filter(email=user.email)
        is_disliked = curr_video.dislikes.filter(email=user.email)


        is_viewed = curr_video.views.filter(email=user.email)

        if len(is_viewed)==0:
            curr_video.add_view(user,video_id)
        
        if is_disliked:
            is_disliked=1
        else:
            is_disliked=0

        if is_liked:
            is_liked=1
        else:
            is_liked=0

        return render(request , 'courses/seevideo.html',{'id':video_id , 'video':curr_video ,'is_liked':is_liked,'is_disliked':is_disliked,
                                'tot_like':tot_like,'tot_dislike':tot_dislike  })



def nextvideo_view(request,*args):
    user=request.user
    if user.is_authenticated:

        vid_id = request.GET.get('id',"")
        
        curr_video = Video.objects.get(id=vid_id)
        curr_video_url=curr_video.video.url

        course_id_for_video = curr_video.course_id 

        all_vids = Video.objects.filter(course_id=course_id_for_video)


        currid_video_urls=[]
        currvid_index=0
        var=0

        for i in all_vids:
            if i.video.url==curr_video_url:
                currvid_index=var
            currid_video_urls.append(i.video.url)
            var+=1

        for i in currid_video_urls:
            print(i)

        print(currvid_index)

        rep={
        'vids':currid_video_urls,
        'index':currvid_index
        }
        response=json.dumps(rep)

        return HttpResponse(response,content_type='application/json')

    return redirect('login_page')



def handle_like(request,*args):
    
    user=request.user
    if user.is_authenticated:
        vid_id = request.GET.get('vidid',"")
        curr_vid = Video.objects.filter(id=vid_id)
        btn = int(request.GET.get('which',""))
        print(btn)
        
        if not curr_vid:
            return HttpResponse("no such video")

        curr_user = studentProfile.objects.get(email=user.email)
        curr_vid=curr_vid[0]

        all_likers = curr_vid.likes.filter(email=user.email)
        
        all_dislikers = curr_vid.dislikes.filter(email=user.email)

        if btn==1:
            if all_likers:
                Video.rem_liked_p(curr_user, vid_id)
            else:
                Video.rem_disliked_p(curr_user,vid_id)
                Video.liked_p(curr_user, vid_id)

        else:
            if all_dislikers:
                Video.rem_disliked_p(curr_user, vid_id)
            else:
                Video.rem_liked_p(curr_user, vid_id)
                Video.disliked_p(curr_user, vid_id)
        likecnt = curr_vid.likes.count()
        dislikecnt = curr_vid.dislikes.count()
        rep={
            'likecnt':likecnt,
            'dislikecnt':dislikecnt
        }
        response=json.dumps(rep)

        return HttpResponse(response,content_type='application/json')

    return redirect('login_page')




def deleteCourse(request,courseId):
    user = request.user
    if user.is_authenticated:
        course = Course.objects.filter(id = courseId)
        course = course[0]
        teacherId = course.teacher.id
        course.delete()
        return HttpResponseRedirect(reverse('teacher_course',kwargs={'teacher_id':teacherId}) )
        # return redirect('teacher_home')

    else:
        return redirect('home_view')


def deleteVideo(request,videoId):
    user = request.user
    if user.is_authenticated:
        video = Video.objects.filter(id = videoId)
        video = video[0]
        courseId = video.course_id.id
        video.delete()
        return HttpResponseRedirect( reverse ('see_course' , kwargs={'course_id':courseId}))
    
    else:
        return redirect('home_view')


    
