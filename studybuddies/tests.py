import datetime
from urllib import request
from django.test import TestCase, Client
import requests
from django.urls import reverse
from django.test.utils import setup_test_environment
from django.utils import timezone

from studybuddies.models import Room, Message, Course, Profile, Friends, FriendRequest, StudySessions


class TrialTest(TestCase):

    def test_simple_addition(self):
        """
        simple test 1 + 2 = 3
        """
        first = 1
        second = 2
        sum = first + second
        self.assertIs(sum, 3)

class RoomTest(TestCase):
    def test_Room_field(self):
        """

        test to ensure the Room name field is filled in correctly
        """
        room1 = Room(name="user1user2")
        self.assertIs(room1.name, "user1user2")

class MessageTest(TestCase):
    def test_Message_default_field(self):
        """

        test to ensure the Message date field fills in its default case properly
        """
        message1 = Message(value="hello", user="me", room="209")
        self.assertIsNotNone(message1.date, msg=None)

class CourseTests(TestCase):
    def test_Course_coursename_default(self):
        """

        test to ensure the Course course_name field fills in its default case properly
        """
        course1 = Course()
        self.assertIsNotNone(course1.course_name, msg=None)

    def test_Course_coursenum_default(self):
        """

        test to ensure the Course course_num field fills in its default case properly
        """
        course1 = Course()
        self.assertIsNotNone(course1.course_num, msg=None)

    def test_Course_professor_default(self):
        """

        test to ensure the Course professor field fills in its default case properly
        """
        course1= Course()
        self.assertIsNotNone(course1.professor, msg=None)
    def test_Course_course_name(self):
        '''

        test to ensure that Course name is filled in correctly.
        '''
        course2 = Course(course_name = "ASD", course_num="3240", professor="Sherriff")
        self.assertEqual(course2.course_name, "ASD")

    def test_Course_num(self):
        '''

        test to ensure that Course number is filled in correctly.
        '''
        course2 = Course(course_name = "ASD", course_num="3240", professor="Sherriff")
        self.assertEqual(course2.course_num, "3240")

    def test_Course_professor(self):
        '''

        test to ensure that Course professor is filled in correctly.
        '''
        course2 = Course(course_name = "ASD", course_num="3240", professor="Sherriff")
        self.assertEqual(course2.professor, "Sherriff")

class ProfileTests(TestCase):
    def test_Profile_first_name(self):
        """

        test to ensure Profile first name field fills in correctly
        """
        profile1 = Profile(first_name="John", last_name="Smith", computing_id="jrs444", year = "third",
                           time_availability = "Mondays")
        self.assertIs(profile1.first_name, "John")

    def test_Profile_last_name(self):
        """

        test to ensure Profile last name field fills in correctly
        """
        profile1 = Profile(first_name="John", last_name="Smith", computing_id="jrs444", year = "third",
                           time_availability = "Mondays")
        self.assertIs(profile1.last_name, "Smith")

    def test_Profile_computing_id(self):
        """

        test to ensure Profile comp id field fills in correctly
        """
        profile1 = Profile(first_name="John", last_name="Smith", computing_id="jrs444", year = "third",
                           time_availability = "Mondays")
        self.assertIs(profile1.computing_id, "jrs444")

    def test_Profile_year(self):
        """

        test to ensure Profile year field fills in correctly
        """
        profile1 = Profile(first_name="John", last_name="Smith", computing_id="jrs444", year = "third",
                           time_availability = "Mondays")
        self.assertIs(profile1.year, "third")

    def test_Profile_time_availability(self):
        """


        test to ensure Profile time availability field fills in correctly
        """
        profile1 = Profile(first_name="John", last_name="Smith", computing_id="jrs444", year = "third",
                           time_availability = "Mondays")
        self.assertIs(profile1.time_availability, "Mondays")

    def test_Profile_empty_field(self):
        '''

        test ensures that an empty field in the Profile is not equal to 'None'
        '''
        profile1 = Profile(last_name="Smith", computing_id="jrs444", year="third",
                           time_availability="Mondays")
        self.assertIsNotNone(profile1.first_name, msg=None)

class StudySessionTests(TestCase):
    def test_Study_Session_capacity_default_filled(self):
        """

        test to ensure that the Study Session capacity default field is not empty.
        """
        studysession1 = StudySessions(date=timezone.now(), time="12:00", course_num="3240")
        self.assertIsNotNone(studysession1.capacity,msg="None")

    def test_Study_Session_capacity_default_value(self):
        """

        test to ensure Study Session capacity field fills in its default case correctly.
        """
        studysession1 = StudySessions(date=timezone.now(), time="12:00", course_num="3240")
        self.assertIs(studysession1.capacity, 20)

    def test_Study_Session_time(self):
        """

        test to ensure Study Session time field fills in correctly.
        """
        studysession1 = StudySessions(date=timezone.now(), time="12:00", course_num="3240")
        self.assertIs(studysession1.time, "12:00")

    def test_Study_Session_course_num(self):
        """

        test to ensure Study Session course_num field fills in correctly.
        """
        studysession1 = StudySessions(date=timezone.now(), time="12:00", course_num="3240")
        self.assertIs(studysession1.course_num, "3240")

    def test_matching_course_num(self):
        """

        test to ensure Study Session course_num field matches that of a Course with the same course_num.
        """
        studysession1 = StudySessions(date=timezone.now(), time="12:00", course_num="3240")
        course1 = Course(course_num="3240")
        self.assertEqual(studysession1.course_num, course1.course_num)

    def test_Study_Session_date_past(self):
        '''

        test to ensure that an inputted past date is calculated as less than today's date
        '''
        studysession1 = StudySessions(date=datetime.date(2020, 10, 10), time="12:00", course_num="3240")
        self.assertGreater(datetime.date.today(), studysession1.date)

    def test_Study_Session_date_future(self):
        '''

        test to ensure that an inputted future date is calculated as greater than today's date
        '''
        studysession1 = StudySessions(date=datetime.date(2023, 10,10), time="12:00", course_num="3240")
        self.assertLess(datetime.date.today(), studysession1.date)


    #def Course_View(self):
        #thisCourse = Course.objects.create(course_name = "CS")
        #response = self.client.get(reverse('studybuddies:mycourses'))
        #self.assertQuerysetEqual(
           # response.context['master_course_list'],
           # [thisCourse],
       # )
    # def test_Profile_major(self):
    #     """

    #     test to ensure Profile major field fills in correctly
    #     """
    #     profile1 = Profile(first_name="John", last_name="Smith", computing_id="jrs444", year = "third", major = "Computer Science",
    #                        time_availability = "Mondays")
    #     self.assertIs(profile1.major, "Computer Science")
    
    # def test_Message_default_date_not_past(self):
    #     message1 = Message(value="hello", user="me", room="209")
    #     dateBool = message1.date().timestamp() < (timezone.now() - datetime.timedelta(days=1)).timestamp()
    #     self.assertTrue(dateBool)

