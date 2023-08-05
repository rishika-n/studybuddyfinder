from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic.edit import FormView, CreateView, UpdateView
from .models import Profile, Course
from django.views import generic
from .forms import CreateProfile, CreateStudySession
from rest_framework import viewsets
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
import requests
import json
from .models import Room, Message, Friends, FriendRequest, StudySessions
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
# Create your views here.
# def home(request):
#     return render(request, 'home.html')

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'studybuddies/room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    
    username = request.POST['username']
    friend = request.POST['dropdown']
    chat = [username, friend]
    print(chat)
    chat.sort()
    room = "".join([chat[0], chat[1]])

    if Room.objects.filter(name=room).exists():
        return redirect(room+'/?username='+username)
        #+'/?username='+username
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect(room+'/?username='+username)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})

class ChatView(generic.ListView):
    template_name = 'studybuddies/chat.html'
    context_object_name = 'friends'
    
    def get_queryset(self):
        """Return the last five published questions."""
        #User = get_user_model()
        return Friends.objects.filter(users1=self.request.user)

# class HomePageView(generic.ListView):
#     template_name = 'studybuddies/home.html'
#     context_object_name = 'studysessions'
    
#     def get_queryset(self):
#         """Return the last five published questions."""
#         return StudySessions.objects.filter(members=self.request.user)

def homePage(request):
    time = timezone.now()
    studysessions = StudySessions.objects.filter(members=request.user, date__gte=time).order_by('date', 'time')
    current_user = Profile.objects.get(user=request.user)
    courses = current_user.courses.all()
    return render(request, 'studybuddies/home.html', {'studysessions':studysessions, 'course_list':courses})
# def editProfile(request):
#     profile_form = CreateProfile
#     return render(request=request, template_name="studybuddies/edit.html", context={"user":request.user, "profile_form":profile_form })    


class EditProfileView(LoginRequiredMixin, CreateView):
    
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

    form_class = CreateProfile      
    model = Profile
    template_name = 'studybuddies/edit.html'
 

class ProfileView(generic.ListView):
    model = Profile
    template_name = 'studybuddies/profile.html'
    context_object_name = 'my_profile'
    def get_queryset(self):
        """Return the last five published questions."""
        return Profile.objects.filter(user=self.request.user).last()




#Do not run: only needs to be run once to populate studybuddies_courses database    
def get_courses(request):
    dept_url = 'http://luthers-list.herokuapp.com/api/deptlist/'
    dept_response = requests.get(dept_url)
    dept_data = json.dumps(dept_response.json())
    depts = json.loads(dept_data)

    all_courses = {}
    for dept in depts:
        url = 'http://luthers-list.herokuapp.com/api/dept/' + dept['subject']
        response = requests.get(url)
        data = json.dumps(response.json())
        courses = json.loads(data)

        for i in courses:
            print(i)
            course_data = Course(
                course_name = i['description'],
                course_num = i['subject'] + " " + i["catalog_number"],
                professor = i['instructor']['name']
            )
            try:
                course_data.save()
            except IntegrityError as e:
                print("error")
            all_courses = Course.objects.order_by('course_num')

    return 

class AllCoursesView(generic.ListView):
    model = Course
    template_name = 'studybuddies/allcourses.html'
    context_object_name = 'master_course_list'
    def get_queryset(self):
        """Return the last five published questions."""
        return Course.objects.all()



def roster(request, course):
    current_course = course
    profiles = Profile.objects.all()
    studysessions = StudySessions.objects.filter(course_num=current_course, date__gte=timezone.now()).order_by('date', 'time')
    requests = FriendRequest.objects.filter(sender=request.user).values_list('receiver', flat=True)
    friends = Friends.objects.filter(users1=request.user).values_list('current_user', flat=True)
    members = studysessions.values_list('members', flat=True)
    return render(request, 'studybuddies/roster.html', {'roster':profiles, 'course': current_course, 'studysessions': studysessions, 'requests':requests, 'friends':friends, 'members':members})

def myFriends(request):
    friends_list = Friends.objects.filter(users1=request.user)
    request_list = FriendRequest.objects.filter(receiver=request.user)
    return render(request, 'studybuddies/friends.html', {'friends_list':friends_list, 'request_list':request_list})

def friend_request(request, username):
    sender = request.user
    recipient = User.objects.get(username=username)
    model = FriendRequest.objects.get_or_create(sender=request.user, receiver=recipient)
    return redirect('/studybuddies/friends')

def remove_friend(request, username):
    client1 = User.objects.get(username=username)
    Friends.lose_friend(request.user, client1)
    Friends.lose_friend(client1, request.user)

    return redirect('/studybuddies/friends')

def add_or_remove_friend(request, operation, username):
    new_friend = User.objects.get(username=username)
    if operation == 'add':
        fq = FriendRequest.objects.get(sender=new_friend, receiver=request.user)
        Friends.make_friend(request.user, new_friend)
        Friends.make_friend(new_friend, request.user)
        fq.delete()
    elif operation == 'remove':
        model2 = FriendRequest.objects.get(sender=new_friend, receiver=request.user)
        model2.delete()
    return redirect('/studybuddies/friends')
        
def createStudySession(request, course):
    if request.method == 'POST':
        form = CreateStudySession(request.POST)
        if form.is_valid():
            form.instance = form.save(commit=False)
            form.instance.save()
            form.instance.members.add(request.user)
            form.instance.course_num = course
            form.instance.save()
            return redirect('/studybuddies/mycourses/'+course)
    else:
        form = CreateStudySession()
    return render(request, 'studybuddies/createsession.html', {'form': form})
    # Rest of your view follows

def join_studySession(request, course, pk):
    studysession = StudySessions.objects.get(pk=pk)
    studysession.members.add(request.user)
    return redirect('/studybuddies/mycourses/'+course)

def viewStudySession(request, pk):
    studysession = StudySessions.objects.get(pk=pk)
    members = studysession.members.all()
    availability = studysession.capacity - len(studysession.members.all())
    return render(request, 'studybuddies/viewstudysession.html', {'studysession':studysession, 'members': members, 'availability':availability})

def viewFriendProfile(request, pk):
    friends_list = Friends.objects.filter(users1=request.user)
    friend = friends_list.get(pk=pk)
    profile = Profile.objects.filter(user=friend.current_user).last()
    return render(request, 'studybuddies/viewfriendprofile.html', {'profile':profile, 'friend':friend})