from django.shortcuts import render
from rest_framework.response import Response # for rest framework api views
from rest_framework.decorators import api_view,permission_classes,parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .permissions import CanMarkAttendance
from .models import Department, Faculty, Class, Batch, Student, Course,Enrollment, Lecture, Lab, Timetable, TimeTableSlot, LecAttendance, LabAttendance,UserProfile
from .serializers import DepartmentSerializer,FacultySerializer,ClassSerializer,BatchSerializer,StudentSerializer,EnrollmentSerializer,CourseSerializer,LectureSerializer,LecAttendanceSerializer,LabSerializer,LabAttendanceSerializer,TimeTableSlotSerializer,TimetableSerializer,UserProfileSerializer
# Create your views here.

@api_view(['GET'])
def getProfiles(request):
   UserProfileFilters = {}
   UserProfiles = UserProfile.objects.filter(**UserProfileFilters)
   serializer = UserProfileSerializer(UserProfiles,many=True)
   return Response(serializer.data)
   pass # get all profiles

@api_view(['GET','PATCH','DELETE'])
def crudProfile(request,pk):
   try:
      profile = UserProfile.objects.get(pk = pk)
      if request.method == 'GET':
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)
      if request.method == 'DELETE':
         if request.user != profile.user:
            return Response({'error': 'You are not allowed to perform this action on this profile'}, status=status.HTTP_403_FORBIDDEN)
         profile.delete()
         return Response({'message': 'profile deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
      if request.method in ['PUT','PATCH']:
         if request.user != profile.user:
            return Response({'error': 'You are not allowed to perform this action on this profile'}, status=status.HTTP_403_FORBIDDEN)
         allowed_fields = ['name', 'email', 'phone']  # Replace with your actual field names
         data = {k: v for k, v in request.data.items() if k in allowed_fields}
         serializer = UserProfileSerializer(profile,data = data,partial = request.method =='PATCH')
         if serializer.is_valid:
           serializer.save()
           return Response(serializer.data)
     

   except UserProfile.DoesNotExist:
      return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
   except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST']) 
def createUserProfile(request):
   UserProfile = UserProfileSerializer(request.data)
   if UserProfile.is_valid:
       UserProfile.save()
       return Response({'message':'UserProfile created Successfully'},status=status.HTTP_201_CREATED)

@api_view(['GET'])
def getDepartments(request):
   DepartmentFilters = {}
   Departments = Department.objects.filter(**DepartmentFilters)
   serializer = DepartmentSerializer(Departments,many=True)
   return Response(serializer.data)
   pass # get a department list

@api_view(['GET','PUT','PATCH','DELETE'])
def crudDepartment(request,pk):
    if not(request.user.userprofile.is_hod):
      return Response({'error': 'You are not allowed to perform this action'}, status=status.HTTP_403_FORBIDDEN)
        
    try:
      department = Department.objects.get(pk = pk)
      if request.method == 'GET':
        serializer = DepartmentSerializer(department)
        return Response(serializer.data)
      if request.method == 'DELETE':
         department.delete()
         return Response({'message': 'department deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
      if request.method in ['PUT','PATCH']:
         serializer = DepartmentSerializer(department,request.data,partial = request.method =='PATCH')
         if serializer.is_valid:
           serializer.save()
           return Response(serializer.data)
     

    except Department.DoesNotExist:
      return Response({'error': 'Department not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST']) 
def createDepartment(request):
   Department = DepartmentSerializer(request.data)
   if Department.is_valid:
       Department.save()
       return Response({'message':'Department created Successfully'},status=status.HTTP_201_CREATED)


@api_view(['GET'])
def getFaculties(request):
   FacultyFilters = {}
   Facultys = Faculty.objects.filter(**FacultyFilters)
   serializer = FacultySerializer(Facultys,many=True)
   return Response(serializer.data)
   pass # get all Faculties list

@api_view(['GET','PATCH','DELETE'])
def crudFaculty(request,pk):
   try:
      faculty = Faculty.objects.get(pk = pk)
      if request.method == 'GET':
        serializer = FacultySerializer(faculty)
        return Response(serializer.data)
      if request.method == 'DELETE':
         faculty.delete()
         return Response({'message': 'faculty deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
      if request.method in ['PUT','PATCH']:
         serializer = FacultySerializer(faculty,request.data,partial = request.method =='PATCH')
         if serializer.is_valid:
           serializer.save()
           return Response(serializer.data)
   

   except Faculty.DoesNotExist:
      return Response({'error': 'Faculty not found'}, status=status.HTTP_404_NOT_FOUND)
   except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
def crudClassIncharges():
   pass

@api_view(['POST']) 
def createFaculty(request):
   Faculty = FacultySerializer(request.data)
   if Faculty.is_valid:
       Faculty.save()
       return Response({'message':'Faculty created Successfully'},status=status.HTTP_201_CREATED)

@api_view(['GET'])
def getClasses(request):
   ClassFilters = {}
   Classs = Class.objects.filter(**ClassFilters)
   serializer = ClassSerializer(Classs,many=True)
   return Response(serializer.data)

   pass # Get all classes

@api_view(['GET','PATCH','DELETE'])
def crudClass(request,pk):
   if not(request.user.userprofile.faculty.exists() or request.user.userprofile.is_hod or request.user.userprofile.is_classIncharge):
      return Response({'error': 'You are not allowed to perform this action'}, status=status.HTTP_403_FORBIDDEN)
   try:
      cLass = Class.objects.get(pk = pk)
      if request.method == 'GET':
        serializer = ClassSerializer(cLass)
        return Response(serializer.data)
      if request.method == 'DELETE':
         cLass.delete()
         return Response({'message': 'cLass deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
      if request.method in ['PUT','PATCH']:
         serializer = ClassSerializer(cLass,request.data,partial = request.method =='PATCH')
         if serializer.is_valid:
           serializer.save()
           return Response(serializer.data)
     

   except Class.DoesNotExist:
      return Response({'error': 'Class not found'}, status=status.HTTP_404_NOT_FOUND)
   except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST']) 
def createClass(request):
   Class = ClassSerializer(request.data)
   if Class.is_valid:
       Class.save()
       return Response({'message':'Class created Successfully'},status=status.HTTP_201_CREATED) 

def crudClassesbyYear():
   pass
def crudClassesbyDept():
   pass


def crudAllBatches():
   pass

@api_view(['POST']) 
def createBatch(request):
   Batch = BatchSerializer(request.data)
   if Batch.is_valid:
       Batch.save()
       return Response({'message':'Batch created Successfully'},status=status.HTTP_201_CREATED)

@api_view(['GET'])
def getBatches(request):
   BatchFilters = {}
   Batchs = Batch.objects.filter(**BatchFilters)
   serializer = BatchSerializer(Batchs,many=True)
   return Response(serializer.data)

@api_view(['GET','PATCH','DELETE'])
def crudBatch(request,pk):
   if not(request.user.userprofile.is_hod or request.user.userprofile.is_classIncharge):
      return Response({'error': 'You are not allowed to perform this action'}, status=status.HTTP_403_FORBIDDEN)
   
   try:
      batch = Batch.objects.get(pk = pk)
      if request.method == 'GET':
        serializer = BatchSerializer(batch)
        return Response(serializer.data)
      if request.method == 'DELETE':
         batch.delete()
         return Response({'message': 'batch deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
      if request.method in ['PUT','PATCH']:
         serializer = BatchSerializer(batch,request.data,partial = request.method =='PATCH')
         if serializer.is_valid:
           serializer.save()
           return Response(serializer.data)
     

   except Batch.DoesNotExist:
      return Response({'error': 'Batch not found'}, status=status.HTTP_404_NOT_FOUND)
   except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
def crudBatchByClass():
   pass

@api_view(['GET','PUT','PATCH','DELETE'])
def RUDStudent(request,pk):
   try:
      student = Student.objects.get(pk = pk)
      if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data)
      if request.method == 'DELETE':
         student.delete()
         return Response({'message': 'Student deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
      if request.method in ['PUT','PATCH']:
         serializer = StudentSerializer(student,request.data,partial = request.method =='PATCH')
         if serializer.is_valid:
           serializer.save()
           return Response(serializer.data)
      if request.method == 'DELETE':
         student.delete()
         return Response({'message': 'Post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

   except Student.DoesNotExist:
      return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
   except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  


#pass #  RUD pzrticular student
# @api_view(['GET','PUT','PATCH','DELETE'])
# def RUDStudentsConditionBased(request):

#    pass

@api_view(['POST'])
def createStudent(request):
   Student = StudentSerializer(request.data)
   if Student.is_valid:
       Student.save()
       return Response({'message':'Student created Successfully'},status=status.HTTP_201_CREATED)
   pass # also returns timetable of the class of that student, total lecs of the class of that student in the sem(as of valid tt), total he has attended, total not attended
  
# def getStudentList():
#    pass # get List pf students


@api_view(['GET','PATCH'])
def getStudentsByCondition(request,**kwargs):
   studentFilters = {}
   if 'batch_id' in request.query_params:
     try:
       batchid = int(request.query_params['batch_id'])
       studentFilters['batch'] = batchid
     except ValueError:
            return Response("Invalid batch_id. It should be an integer.", status=400)
       
   if 'joined_yr' in request.query_params:
     try:
       jid = int(request.query_params['joined_yr'])
       studentFilters['joined_year'] = jid
     except ValueError:
       return Response("Invalid joined yr It should be an integer.", status=400)
   if 'class' in request.query_params:
      try:
       jid = int(request.query_params['class'])
       studentFilters['class_field'] = jid
      except ValueError:
       return Response("Invalid class It should be an integer.", status=400)
       
   

   try:
     students = Student.objects.filter(**studentFilters)
   except Student.DoesNotExist:
      return Response({'error': 'Students with given conditions not found'}, status=status.HTTP_404_NOT_FOUND)

   if(request.method == 'GET'):
     serializer = StudentSerializer(students,many=True)
   if(request.method == 'PATCH'):
      fields = request.data
      students.update(**fields)
      serializer = StudentSerializer(students,many=True)
 
      
   return Response(serializer.data)

     # get students by class  



@api_view(['GET'])
def getCourses(request):
   CourseFilters = {}
   courses = Course.objects.filter(**CourseFilters)
   serializer = CourseSerializer(courses,many=True)
   return Response(serializer.data)


@api_view(['GET','PATCH','DELETE'])
def crudCourse(request,pk):
   try:
      course = Course.objects.get(pk = pk)
      if request.method == 'GET':
        serializer = CourseSerializer(course)
        return Response(serializer.data)
      if request.method == 'DELETE':
         course.delete()
         return Response({'message': 'Course deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
      if request.method in ['PUT','PATCH']:
         serializer = CourseSerializer(course,request.data,partial = request.method =='PATCH')
         if serializer.is_valid:
           serializer.save()
           return Response(serializer.data)
   

   except Course.DoesNotExist:
      return Response({'error': 'Faculty not found'}, status=status.HTTP_404_NOT_FOUND)
   except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
@api_view(['POST']) 
def createCourse(request):
   Course = CourseSerializer(request.data)
   if Course.is_valid:
       Course.save()
       return Response({'message':'Course created Successfully'},status=status.HTTP_201_CREATED)

@api_view(['GET'])
def getEnrollments(request):
   EnrollmentFilters = {}
   enrollments = Enrollment.objects.filter(**EnrollmentFilters)
   serializer = EnrollmentSerializer(enrollments,many = True)
   return Response(serializer.data)

@api_view(['POST']) 
def createEnrollment(request):
   Enrollment = EnrollmentSerializer(request.data)
   if Enrollment.is_valid:
       Enrollment.save()
       return Response({'message':'Enrollment created Successfully'},status=status.HTTP_201_CREATED)
   pass

def crudEnrollment():
   pass

@api_view(['GET'])
def getLectures(request): 
   LectureFilters = {}
   Lectures = Lecture.objects.filter(**LectureFilters)
   serializer = LectureSerializer(Lectures,many=True)
   return Response(serializer.data)
   pass # get all Lecs, with conditions

@api_view(['GET','PATCH','DELETE'])
def crudlec(request,pk):
   
    try:
      lecture = Lecture.objects.get(pk = pk)
      if not(request.user.userprofile.faculty == lecture.faculty or request.user.userprofile.is_hod or request.user.userprofile.is_coursehead or request.user.userprofile.is_classIncharge):
          return Response({'error': 'You are not allowed to perform this action'}, status=status.HTTP_403_FORBIDDEN)
         
      if request.method == 'GET':
        serializer = LectureSerializer(lecture)
        return Response(serializer.data)
      if request.method == 'DELETE':
         lecture.delete()
         return Response({'message': 'Lecture deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
      if request.method in ['PUT','PATCH']:
         serializer = LectureSerializer(lecture,request.data,partial = request.method =='PATCH')
         if serializer.is_valid:
           serializer.save()
           return Response(serializer.data)
     

    except Lecture.DoesNotExist:
      return Response({'error': 'Lecture not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
@api_view(['POST']) 
def createLecture(request):
   Lecture = LectureSerializer(request.data)
   if Lecture.is_valid:
       Lecture.save()
       return Response({'message':'Lecture created Successfully'},status=status.HTTP_201_CREATED)
# def crudLecbyRoom():
#    pass
# def crudLecbyCourse():
#    pass

def CountLecsperCourseofaClass():
   pass

@api_view(['GET'])
def getLabs(request):
   LabFilters = {}
   Labs = Lab.objects.filter(**LabFilters)
   serializer = LabSerializer(Labs,many=True)
   return Response(serializer.data)
   pass # get all Labs

@api_view(['GET','PATCH','DELETE'])
def crudExtraLab(request,pk):
   try:
      lab = Lab.objects.get(pk = pk)
      if request.method == 'GET':
        serializer = LabSerializer(lab)
        return Response(serializer.data)
      if request.method == 'DELETE':
         lab.delete()
         return Response({'message': 'lab deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
      if request.method in ['PUT','PATCH']:
         serializer = LabSerializer(lab,request.data,partial = request.method =='PATCH')
         if serializer.is_valid:
           serializer.save()
           return Response(serializer.data)
   except Lab.DoesNotExist:
      return Response({'error': 'Lab not found'}, status=status.HTTP_404_NOT_FOUND)
   except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
# def crudLabsbyClass():
#    pass
# def crudLabsbyFaculty():
#    pass
# def crudLabsbyRoom():
#    pass
# def crudLabsbyCourse():
#    pass
@api_view(['POST']) 
def createLab(request):
   Lab = LabSerializer(request.data)
   if Lab.is_valid:
       Lab.save()
       return Response({'message':'Lab created Successfully'},status=status.HTTP_201_CREATED)
def CountLabsperCourseofaClass():
   pass

@api_view(['GET'])
def getLecAttendances(request):
   LecAttendanceFilters = {}
   LecAttendances = LecAttendance.objects.filter(**LecAttendanceFilters)
   serializer = LecAttendanceSerializer(LecAttendances,many=True)
   return Response(serializer.data)

@api_view(['PATCH','PUT'])
@permission_classes([CanMarkAttendance])
def crudLecAttendance(request):
   lec = request.data.get("Lecture")
   Attendance = request.data.get("Attendance",{})
   serializer = LecAttendanceSerializer(Attendance, many = True,partial = request.method == 'PATCH')
   if serializer.is_valid():
      serializer.save()
      return Response({"message": "Attendance updated successfully"}, status=200)

    # If validation fails, return an error response
   return Response(serializer.errors, status=400)

   pass # mark attendance of a particular student in a particuar lec
# def crudLecAttendancebyStudent():
#    pass
@api_view(['POST']) 
def createLecAttendance(request):
   LecAttendance = LecAttendanceSerializer(request.data)
   if LecAttendance.is_valid:
       LecAttendance.save()
       return Response({'message':'LecAttendance created Successfully'},status=status.HTTP_201_CREATED)

@api_view(['GET'])
def getLabAttendance(request):
   LabAttendanceFilters = {}
   LabAttendances = LabAttendance.objects.filter(**LabAttendanceFilters)
   serializer = LabAttendanceSerializer(LabAttendances,many=True)
   return Response(serializer.data) # get attendance of all students in a particular lab
# def crudLabAttendancebyBatch():
#    pass # get attendance of all students in a particular batch
@api_view(['PATCH'])
@permission_classes([CanMarkAttendance])
def crudLabAttendance(request):
  
   serializer = LabAttendanceSerializer(request.data, many = True,partial = request.method == 'PATCH')
   if serializer.is_valid():
      serializer.save()
      return Response({"message": "Attendance updated successfully"}, status=200)

    # If validation fails, return an error response
   return Response(serializer.errors, status=400) # mark attendance of a student in labs
# def crudLabAttendancebyStudent():
#    pass
@api_view(['POST']) 
def createLabAttendance(request):
   LabAttendance = LabAttendanceSerializer(request.data)
   if LabAttendance.is_valid:
       LabAttendance.save()
       return Response({'message':'LabAttendance created Successfully'},status=status.HTTP_201_CREATED)

@api_view(['GET'])
def getTimeTables(request):
   TimetableFilters = {}
   Timetables = Timetable.objects.filter(**TimetableFilters)
   serializer = TimetableSerializer(Timetables,many=True)
   return Response(serializer.data)
   pass # get all timetables
def crudTT():
   pass

@api_view(['POST']) 
def createTimeTable(request):
   TimeTable = TimetableSerializer(request.data)
   if TimeTable.is_valid:
       TimeTable.save()
       return Response({'message':'TimeTable created Successfully'},status=status.HTTP_201_CREATED)


@api_view(['GET','PUT','PATCH','DELETE'])
def crudTimetable(request,pk):
    try:
      timetable = Timetable.objects.get(pk = pk)
      if not(request.user.userprofile.is_hod or request.user.userprofile.is_classIncharge):
        return Response({'error': 'You are not allowed to perform this action'}, status=status.HTTP_403_FORBIDDEN)

      if request.method == 'GET':
        serializer = TimetableSerializer(timetable)
        return Response(serializer.data)
      if request.method == 'DELETE':
         timetable.delete()
         return Response({'message': 'timetable deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
      if request.method in ['PUT','PATCH']:
         serializer = TimetableSerializer(timetable,request.data,partial = request.method =='PATCH')
         if serializer.is_valid:
           serializer.save()
           return Response(serializer.data)
    except Timetable.DoesNotExist:
      return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def crudTTSlotbyDay():

   pass

@api_view(['GET'])
def getTimeTableSlots(request):
   TimetableSlotFilters = {}
   TimetableSlots = TimeTableSlot.objects.filter(**TimetableSlotFilters)
   serializer = TimeTableSlotSerializer(TimetableSlots,many=True)
   return Response(serializer.data)


@api_view(['POST']) 
def createTimeTableSlot(request):
   TimeTableSlot = TimeTableSlotSerializer(request.data)
   if TimeTableSlot.is_valid:
       TimeTableSlot.save()
       return Response({'message':'TimeTableSlot created Successfully'},status=status.HTTP_201_CREATED)


@api_view(['GET','PUT','PATCH','DELETE'])
def crudTimeTableSlot(request,pk):
    try:
      timeTableSlot = TimeTableSlot.objects.get(pk = pk)
      if not(request.user.userprofile.is_hod or request.user.userprofile.is_classIncharge):
        return Response({'error': 'You are not allowed to perform this action'}, status=status.HTTP_403_FORBIDDEN)
      if request.method == 'GET':
        serializer = TimeTableSlotSerializer(timeTableSlot)
        return Response(serializer.data)
      if request.method == 'DELETE':
         timeTableSlot.delete()
         return Response({'message': 'timeTableSlot deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
      if request.method in ['PUT','PATCH']:
         serializer = TimeTableSlotSerializer(timeTableSlot,request.data,partial = request.method =='PATCH')
         if serializer.is_valid:
           serializer.save()
           return Response(serializer.data)
    except TimeTableSlot.DoesNotExist:
      return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



def getPercentAttendanceofStudentinaCourseLecs():
   pass
def getPercentAttendanceofStudentinaCourseLabs():
   pass
def getPercentAttendanceofAllStudentinaCourseLecs():
   pass
def getPercentAttendanceofAllStudentinaCourseLabs():
   pass






'''

from django.http import JsonResponse
from .models import Lecture
from .serializers import LectureSerializer

def lecture_list(request, **kwargs):
    # Use kwargs as needed to dynamically build filters
    filters = {}

    # Example: Check if 'course_id' is provided in kwargs
    if 'course_id' in kwargs:
        filters['course__id'] = kwargs['course_id']

    # Example: Check if 'room_number' is provided in kwargs
    if 'room_number' in kwargs:
        filters['room'] = kwargs['room_number']

    # Apply filters to the queryset
    lectures = Lecture.objects.filter(**filters)

    # Serialize the queryset
    serializer = LectureSerializer(lectures, many=True)

    # Return JSON response
    return JsonResponse(serializer.data, safe=False)
And in your urls.py:

python
Copy code
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('lectures/', views.lecture_list, name='lecture-list'),
    path('lectures/course/<int:course_id>/', views.lecture_list, name='lecture-list-by-course'),
    path('lectures/room/<int:room_number>/', views.lecture_list, name='lecture-list-by-room'),
    path('lectures/course/<int:course_id>/room/<int:room_number>/', views.lecture_list, name='lecture-list-by-course-and-room'),
]


'''