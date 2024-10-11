#from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
  
    # Departments
    path('departments/', views.getDepartments, name='get-departments'),
    path('departments/<int:pk>/', views.crudDepartment, name='crud-department'),
    path('departments/create/', views.createDepartment, name='create-department'),
    
    #students
    path('students/<int:pk>/', views.RUDStudent, name='crud-student'),
    path('students/create/', views.createStudent, name='create-student'),
    path('students/', views.getStudentsByCondition, name='filter-students'),
   
   # Courses
    path('courses/', views.getCourses, name='get-courses'),
    path('courses/<int:pk>/', views.crudCourse, name='crud-course'),
    path('courses/create/', views.createCourse, name='create-course'),
   

    # Timetables
    path('timetables/', views.getTimeTables, name='get-timetables'),
    path('timetables/<int:pk>/', views.crudTimetable, name='crud-timetable'),
    path('timetables/<int:pk>/leclabs/<int:lec_lab>/', views.getLecLabsPerCourseinTT, name='lec-labs-per-course-in-tt'),
    path('timetables/<int:pk>/leclabs/total/<int:lec_lab>/', views.getTotalLecLabsPerCourseinTT, name='count-lec-labs-per-course-in-tt'),
    path('timetables/create/', views.createTimeTable, name='create-timetable'),
    
    # Timetable Slots
    path('slots/', views.getTimeTableSlots, name='get-slots'),
    path('slots/<int:pk>/', views.crudTimeTableSlot, name='crud-slot'),
    path('slots/create/', views.createTimeTableSlot, name='create-slot'),
    
    # Profiles
    path('profiles/', views.getProfiles, name='get-profiles'),
    path('profiles/<int:pk>/', views.crudProfile, name='crud-profile'),
    path('profiles/create/', views.createProfile, name='create-profile'),
    path('user/create/', views.createUser, name='create-user'),
    path('profiles/create_user/', views.createUserProfile, name='create-user-profile'),


    # Faculties
    path('faculties/', views.getFaculties, name='get-faculties'),
    path('faculties/<int:pk>/', views.crudFaculty, name='crud-faculty'),
    path('faculties/create/', views.createFaculty, name='create-faculty'),

    # Classes
    path('classes/', views.getClasses, name='get-classes'),
    path('classes/<int:pk>/', views.crudClass, name='crud-class'),
    path('classes/create/', views.createClass, name='create-class'),

    # Batches
    path('batches/', views.getBatches, name='get-batches'),
    path('batches/<int:pk>/', views.crudBatch, name='crud-batch'),
    path('batches/create/', views.createBatch, name='create-batch'),

    # Lectures
    path('lectures/', views.getLectures, name='get-lectures'),
    path('lectures/<int:pk>/', views.crudlec, name='crud-lecture'),
    path('lectures/create/', views.createLecture, name='create-lecture'),
    path('lectures/cancel/', views.crudLecsConditional, name='cud-lecs-c'),


    # Labs
    path('labs/', views.getLabs, name='get-labs'),
    path('labs/<int:pk>/', views.crudExtraLab, name='crud-lab'),
    path('labs/create/', views.createLab, name='create-lab'),
    path('labs/cancel/', views.crudLabsConditional, name='cud-labs-c'),

   

    # Enrollments
    path('enrollments/', views.getEnrollments, name='get-enrollments'),
    path('enrollments/create/', views.createEnrollment, name='create-enrollment'),

    # Lab Attendances
    path('labattendances/', views.getLabAttendance, name='get-lab-attendances'),
    path('labattendances/markatt/', views.MarkLabAttendance, name='crud-lab-attendance'),
    path('labattendances/create/', views.createLabAttendance, name='create-lab-attendance'),
   
    path('attendances/getPercent/<int:pk>/<int:lec_lab>/', views.getPercentAttendanceofStudentinaCourseLecs, name='percent-attedance-lecs'),
   # LecAttendances
    path('lecattendances/', views.getLecAttendances, name='get-lec-attendances'),
    path('lecattendances/markatt/', views.crudLecAttendance, name='crud-lec-attendance'),
    path('lecattendances/create/', views.createLecAttendance, name='create-lec-attendance'),
    
    

]