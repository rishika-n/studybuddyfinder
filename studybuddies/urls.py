from django.urls import path, include
from rest_framework import routers
from . import views


app_name = 'studybuddies'
urlpatterns = [
    path('', views.homePage, name='home'),
    path('chat', views.ChatView.as_view(), name='chat'),
    path('profile/edit/', views.EditProfileView.as_view(), name='edit'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('courses/', views.AllCoursesView.as_view(), name="allcourses"),
    path('friends/', views.myFriends, name="myfriends"),
    path('mycourses/<str:course>/', views.roster, name='roster'),
    path('chat/<str:room>/', views.room, name='room'),
    path('chat/checkview', views.checkview, name='checkview'),
    path('chat/send', views.send, name='send'),
    path('chat/getMessages/<str:room>/', views.getMessages, name='getMessages'),
    path('friendreq/<str:username>', views.friend_request, name='friendrequest'),
    path('friends/<str:operation>/<str:username>', views.add_or_remove_friend, name='myrequest'),
    path('remfriend/<str:username>', views.remove_friend, name='remfriend'),
    path('mycourses/<str:course>/createStudySession/', views.createStudySession, name='createsession'),
    path('mycourses/<str:course>/join/<int:pk>/', views.join_studySession, name='joinstudysession'),
    path('session/<int:pk>', views.viewStudySession, name='viewstudysession'),
    path('friends/<int:pk>', views.viewFriendProfile, name='viewfriendprofile')
]