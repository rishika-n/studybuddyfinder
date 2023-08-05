from django.db import models
from django.urls import reverse
from datetime import datetime
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=1000)
    
class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=timezone.now, blank=True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)

class Course(models.Model):
    def __str__(self):
        return self.course_num + ", " + self.professor
    class Meta:
        unique_together = ["course_name","course_num", "professor"]
    course_name = models.CharField(max_length=200, default="")
    course_num = models.CharField(max_length=200, default="")
    professor = models.CharField(max_length=200, default="")

class Profile(models.Model):
    def __str__(self):
        return self.first_name
    
    def get_absolute_url(self):
        return reverse('studybuddies:profile', kwargs={})
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    computing_id = models.CharField(max_length=200)
    year = models.CharField(max_length=4)
    #major = models.CharField(max_length=20)
    time_availability = models.CharField(max_length=200)
    courses = models.ManyToManyField(Course)


class Friends(models.Model):
    users1=models.ManyToManyField(User,null=True)
    current_user=models.ForeignKey(User,related_name='owner',on_delete=models.CASCADE,null=True)



    @classmethod
    def make_friend(cls,current_user,new_friend):
        friend,create=cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users1.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, create = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users1.remove(new_friend)


class FriendRequest(models.Model):
    sender=models.ForeignKey(User,null=True,related_name='sender1',on_delete=models.CASCADE)
    receiver=models.ForeignKey(User,null=True,on_delete=models.CASCADE)

class StudySessions(models.Model):
    members = models.ManyToManyField(User,null=True)
    capacity = models.IntegerField(blank=True, null=True, default=20)
    date = models.DateField()
    time = models.TimeField()
    course_num = models.CharField(max_length=200, default="")
    class Meta:
        unique_together = ["date","time", "course_num"]
    def get_absolute_url(self):
        return reverse('studybuddies', kwargs={})
