from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .serializers import *
from .models import *
from django.contrib.auth.models import User
from datetime import date,time


# Create your tests here.

class UserProfileTests(APITestCase):
    def test_create_user_profile(self):
        # Prepare data for the request
        user_data = {'username': 'testuser', 'password': 'testpassword', 'email':'test@example.com'}  # Adjust as needed
        profile_data = {'name': 'Test User', 'email': 'test@example.com', 'phone':'12345678','date_of_birth': date(1990,1,1)}  # Adjust as needed
        faculty_data = {'department':1}  # Adjust as needed
        student_data = {'joined_year': 2000,'class_field':None, 'batch':None}  # Adjust as needed

        # Make a request to create a user profile
        response = self.client.post('/api/profiles/create/', {
            'UserInfo': user_data,
            'ProfileInfo': profile_data,
            #'FacultyInfo': faculty_data,
            'StudentInfo': student_data,  # Uncomment if testing with student data
        }, format='json')

        # Verify the response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertIn('User created Successfully', response.data['message'])

        # Optionally, check the created objects in the database
        user = User.objects.get(username=user_data['username'])
        self.assertIsNotNone(user)

        # Adjust the checks based on your models and serializers
        profile = user.userprofile
        self.assertEqual(profile.name, profile_data['name'])

        # Adjust for testing Faculty and Student models if needed
        # faculty = profile.faculty
        # student = profile.student

'''

{
"UserInfo":{
"username":"arooshjoshi",
"email":"aroosh.joshi22@spit.ac.in",
"password": "aj19@Nav"
},
"ProfileInfo":{
"name":"Aroosh Joshi",
"email":"aroosh.joshi22@spit.ac.in",
"phone": 123456789,
"date_of_birth": "2004-03-28"
},

"StudentInfo":{
"joined_year":2022,
"class_field":1,
"batch":1
}
}


{
"UserInfo":{
"username":"ccnfaculty",
"email":"ccnfac@nav.in",
"password": "ccnfac@Nav"
},
"ProfileInfo":{
"name":"CCN Faculty",
"email":"ccnfac@nav.in",
"phone": 123456789,
"date_of_birth": "2024-03-21"
},

"FacultyInfo":{
  "department": 2
}

}


Dept
{
 "dname":"Computer Science and Engineering",
 "hod":None
}

Class 
{
  "department": 2,
  "year":2,
  "division":"D",
  "acad_year":"2023-24",
  "incharge":null,
  "cr" : null
}

Batch
{
"bname" : "Batch B",
"class_field":2,
"br":null

}

Course
{
"cname" : "Linear Algebra",
"semester":4,
"head" : null,
"department" : 3,
}

TimeTable
{
 "class_field":2,
 "semester":4,
 "valid_from": "2024-01-15",
 "valid_till": "2024-05-09",
}

TimeTableSlot
{
 "ttid" : 2,
 "day" : 1,
 "start_time": "09:00",
 "end_time":"10:00",
 "faculty": 6,
 "course":2,
 "lec_lab":1,
 "batch":null

}





'''