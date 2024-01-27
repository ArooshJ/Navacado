from django.shortcuts import render
from rest_framework.response import Response # for rest framework api views
from rest_framework.decorators import api_view,permission_classes,parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .permissions import CanMarkAttendance,IsAdminOrSuperuser,IsClassInchargeOrHod,IsHod
from .models import Department, Faculty, Class, Batch, Student, Course,Enrollment, Lecture, Lab, Timetable, TimeTableSlot, LecAttendance, LabAttendance,UserProfile
from django.db.models import *
from .serializers import DepartmentSerializer,FacultySerializer,ClassSerializer,BatchSerializer,StudentSerializer,EnrollmentSerializer,CourseSerializer,LectureSerializer,LecAttendanceSerializer,LabSerializer,LabAttendanceSerializer,TimeTableSlotSerializer,TimetableSerializer,UserProfileSerializer
# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfiles(request):
   UserProfileFilters = {}
   UserProfiles = UserProfile.objects.filter(**UserProfileFilters)
   serializer = UserProfileSerializer(UserProfiles,many=True)
   return Response(serializer.data)
   pass # get all profiles

@api_view(['GET','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def crudProfile(request,pk):
   try:
      profile = UserProfile.objects.get(pk = pk)
      if request.method == 'GET':
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)
      if request.method == 'DELETE':
         
         permission  = request.user == profile.user or request.user.is_superuser 
         if not permission:
            return Response({'error': 'You are not allowed to perform this action on this profile'}, status=status.HTTP_403_FORBIDDEN)
         
         profile.delete()
         return Response({'message': 'profile deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
      if request.method in ['PUT','PATCH']:
         
         permission = (request.user == profile.user) or request.user.is_superuser   
         if not permission:
            return Response({'error': 'You are not allowed to perform this action on this profile'}, status=status.HTTP_403_FORBIDDEN)
         allowed_fields = ['name', 'email', 'phone']  # Replace with your actual field names
         
         data = {k: v for k, v in request.data.items() if k in allowed_fields} 
         serializer = UserProfileSerializer(profile,data = data,partial = request.method =='PATCH')
         if serializer.is_valid():
           serializer.save()
           return Response(serializer.data)
     

   except UserProfile.DoesNotExist:
      return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
   except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST']) 
@permission_classes([IsAuthenticated])
def createUserProfile(request):
   permission = request.user.is_superuser
   if not permission:
         return Response({'error': 'You are not allowed to perform this action on this profile'}, status=status.HTTP_403_FORBIDDEN)
   UserProfile = UserProfileSerializer(request.data)
   if UserProfile.is_valid():
       UserProfile.save()
       return Response({'message':'UserProfile created Successfully'},status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getDepartments(request):
   DepartmentFilters = {}
   Departments = Department.objects.filter(**DepartmentFilters)
   serializer = DepartmentSerializer(Departments,many=True)
   return Response(serializer.data)
   pass # get a department list

@api_view(['GET','PUT','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def crudDepartment(request,pk):
   #  if not(request.user.userprofile.is_hod):
   #    return Response({'error': 'You are not allowed to perform this action'}, status=status.HTTP_403_FORBIDDEN)
        
    try:
      department = Department.objects.get(pk = pk)
      if request.method == 'GET':
        serializer = DepartmentSerializer(department)
        return Response(serializer.data)
      if request.method == 'DELETE':
         #permission
         permission = request.user.is_superuser
         if not permission:
            return Response({'error': 'You are not allowed to perform this action'}, status=status.HTTP_403_FORBIDDEN)
         
         department.delete()
         return Response({'message': 'department deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
      if request.method in ['PUT','PATCH']:
         #permission
        
         print('patch started')
         permission = (request.user.is_superuser) or (request.user.userprofile and (request.user.userprofile.faculty and request.user.userprofile.faculty.hod and request.user.userprofile.faculty.hod == department) )
         if not permission:
            return Response({'error': 'You are not allowed to perform this action'}, status=status.HTTP_403_FORBIDDEN)
         print('permission passd')
         serializer = DepartmentSerializer(department,request.data,partial = request.method =='PATCH')
         print(serializer.is_valid())
         if serializer.is_valid():
           print("valid")
           serializer.save()
           return Response(serializer.data)
         print("Not Valid")
         return Response({'error':str(serializer.errors)},status = status.HTTP_206_PARTIAL_CONTENT)

    except Department.DoesNotExist:
      print('deptnot exists')
      return Response({'error': 'Department not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print('othererr')
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST']) 
@permission_classes([IsAdminOrSuperuser])
def createDepartment(request):
   Department = DepartmentSerializer(request.data)
   if Department.is_valid():
       Department.save()
       return Response({'message':'Department created Successfully'},status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getFaculties(request):
   FacultyFilters = {}
   Facultys = Faculty.objects.filter(**FacultyFilters)
   serializer = FacultySerializer(Facultys,many=True)
   return Response(serializer.data)
   pass # get all Faculties list

@api_view(['GET','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def crudFaculty(request,pk):
   try:
      profile = request.user.userprofile
      faculty = Faculty.objects.get(pk = pk)
      if request.method == 'GET':
        serializer = FacultySerializer(faculty)
        return Response(serializer.data)
      if request.method == 'DELETE':

         #permission
         permission =  (request.user.is_superuser)
         if not permission:
            return Response({'error': 'You are not allowed to perform this action'}, status=status.HTTP_403_FORBIDDEN)
         
         faculty.delete()
         return Response({'message': 'faculty deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
      if request.method in ['PUT','PATCH']:
        
         permission = (request.user.userprofile and request.user.userprofile.faculty == faculty)
         if not permission:
             return Response({'error' :'You are not allowed to perform this action'},status =status.HTTP_403_FORBIDDEN)

         serializer = FacultySerializer(faculty,request.data,partial = request.method =='PATCH')
         if serializer.is_valid():
           serializer.save()
           return Response(serializer.data)
   

   except Faculty.DoesNotExist:
      return Response({'error': 'Faculty not found'}, status=status.HTTP_404_NOT_FOUND)
   except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
def crudClassIncharges():
   pass

@api_view(['POST']) 
@permission_classes([IsAuthenticated])
def createFaculty(request):
   permission = request.user.is_superuser
   if not permission:
             return Response({'error' :'You are not allowed to perform this action'},status =status.HTTP_403_FORBIDDEN)
   Faculty = FacultySerializer(request.data)
   if Faculty.is_valid():
       Faculty.save()
       return Response({'message':'Faculty created Successfully'},status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getClasses(request):
   ClassFilters = {}
   Classs = Class.objects.filter(**ClassFilters)
   serializer = ClassSerializer(Classs,many=True)
   return Response(serializer.data)

   pass # Get all classes

@api_view(['GET','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def crudClass(request,pk):
   
   try:
      cLass = Class.objects.get(pk = pk)
      if request.method == 'GET':
        serializer = ClassSerializer(cLass)
        return Response(serializer.data)
      if request.method == 'DELETE':
         
         permission = (request.user.userprofile.faculty.exists() and (request.user.userprofile.faculty.hod.exists() or request.user.userprofile.incharge and (request.user.userprofile.faculty.incharge == cLass.incharge)))
         if not permission:
             return Response({'error': 'You are not allowed to perform this action'}, status=status.HTTP_403_FORBIDDEN)
         
         cLass.delete()
         return Response({'message': 'cLass deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
      
      if request.method in ['PUT','PATCH']:
         
         permission = (request.user.userprofile.faculty.exists() and (request.user.userprofile.faculty.hod.exists() or request.user.userprofile.faculty.classincharge.exists()))
         if not permission:
           return Response({'error': 'You are not allowed to perform this action'}, status=status.HTTP_403_FORBIDDEN)
         
         serializer = ClassSerializer(cLass,request.data,partial = request.method =='PATCH')
         if serializer.is_valid():
           serializer.save()
           return Response(serializer.data)
     

   except Class.DoesNotExist:
      return Response({'error': 'Class not found'}, status=status.HTTP_404_NOT_FOUND)
   except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST']) 
@permission_classes([IsAuthenticated])
def createClass(request):
   Class = ClassSerializer(request.data)
   permission = request.user.is_superuser or (request.user.userprofile and request.user.userprofile.faculty and request.userprofile.faculty.hod and request.userprofile.faculty.hod == Class.department)
   if not permission:
             return Response({'error' :'You are not allowed to perform this action'},status =status.HTTP_403_FORBIDDEN)
   if Class.is_valid():
       Class.save()
       return Response({'message':'Class created Successfully'},status=status.HTTP_201_CREATED) 

def crudClassesbyYear():
   pass
def crudClassesbyDept():
   pass
def crudAllBatches():
   pass    

@api_view(['POST']) 
@permission_classes([IsAuthenticated])

def createBatch(request):
    
   Batch = BatchSerializer(request.data)
   profile = request.user.userprofile
   permission = request.user.is_superuser or (profile and profile.faculty and profile.faculty.incharge and profile.faculty.incharge == Batch.class_field.incharge)

   if not permission:
             return Response({'error' :'You are not allowed to perform this action'},status =status.HTTP_403_FORBIDDEN)
   if Batch.is_valid():
       Batch.save()
       return Response({'message':'Batch created Successfully'},status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getBatches(request):
   BatchFilters = {}
   Batchs = Batch.objects.filter(**BatchFilters)
   serializer = BatchSerializer(Batchs,many=True)
   return Response(serializer.data)

@api_view(['GET','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def crudBatch(request,pk):
   
   
   try:
      profile = request.user.userprofile
      batch = Batch.objects.get(pk = pk)
      if request.method == 'GET':
        serializer = BatchSerializer(batch)
        return Response(serializer.data)
      if request.method == 'DELETE':
         
         permission = profile and (profile.faculty and ((profile.faculty.incharge and profile.faculty.incharge == batch.class_field.incharge ) or( profile.faculty.hod and profile.faculty.hod == batch.class_field.department))) or request.user.is_superuser
         if not permission:
           return Response({'error': 'You are not allowed to perform this action'}, status=status.HTTP_403_FORBIDDEN)
        
         batch.delete()
         return Response({'message': 'batch deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
      if request.method in ['PUT','PATCH']:
          
         permission = profile and (profile.faculty and ((profile.faculty.incharge and profile.faculty.incharge == batch.class_field.incharge ) or( profile.faculty.hod and profile.faculty.hod == batch.class_field.department))) or request.user.is_superuser

         if not permission:
            return Response({'error': 'You are not allowed to perform this action'}, status=status.HTTP_403_FORBIDDEN)

         serializer = BatchSerializer(batch,request.data,partial = request.method =='PATCH')
         if serializer.is_valid():
           serializer.save()
           return Response(serializer.data)
     

   except Batch.DoesNotExist:
      return Response({'error': 'Batch not found'}, status=status.HTTP_404_NOT_FOUND)
   except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
def crudBatchByClass():
   pass

@api_view(['GET','PUT','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def RUDStudent(request,pk):
   try:
      profile = request.user.userprofile
      student = Student.objects.get(pk = pk)
      if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data)
      if request.method == 'DELETE':
         
         permission = (request.user.is_superuser)
         if not permission:
            return Response({'error': 'You are not allowed to perform this action'}, status=status.HTTP_403_FORBIDDEN)
         student.delete()
         return Response({'message': 'Student deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
     
      if request.method in ['PUT','PATCH']:
          
         serializer = StudentSerializer(student,request.data,partial = request.method =='PATCH')
         if serializer.is_valid():
           serializer.save()
           return Response(serializer.data)
      

   except Student.DoesNotExist:
      return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
   except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  


#pass #  RUD pzrticular student
# @api_view(['GET','PUT','PATCH','DELETE'])
# def RUDStudentsConditionBased(request):

#    pass

@api_view(['POST'])
@permission_classes([IsAdminOrSuperuser])
def createStudent(request):
   Student = StudentSerializer(request.data)
   if Student.is_valid():
       Student.save()
       return Response({'message':'Student created Successfully'},status=status.HTTP_201_CREATED)
   pass # also returns timetable of the class of that student, total lecs of the class of that student in the sem(as of valid tt), total he has attended, total not attended
  
# def getStudentList():
#    pass # get List pf students


@api_view(['GET','PATCH'])
@permission_classes([IsAuthenticated])
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
      if not (request.user.is_superuser or request.user.is_admin):
         return Response({'error': 'You are not allowed to perform this action'}, status=status.HTTP_403_FORBIDDEN)
      fields = request.data
      students.update(**fields)
      serializer = StudentSerializer(students,many=True)
 
      
   return Response(serializer.data)

     # get students by class  



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCourses(request):
   CourseFilters = {}
   courses = Course.objects.filter(**CourseFilters)
   serializer = CourseSerializer(courses,many=True)
   return Response(serializer.data)


@api_view(['GET','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def crudCourse(request,pk):
   try:
      profile = request.user.userprofile
      course = Course.objects.get(pk = pk)
      if request.method == 'GET':
        serializer = CourseSerializer(course)
        return Response(serializer.data)
      if request.method == 'DELETE':
         
         #permission
         permission =  (request.user.is_superuser or (profile.faculty and profile.faculty.hod and profile.faculty.hod == course.department))
         if not permission:
            return Response({'error': 'You are not allowed to perform this action'}, status=status.HTTP_403_FORBIDDEN)
         
         course.delete()
         return Response({'message': 'Course deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
      if request.method in ['PUT','PATCH']:
         #permission
         permission =  (profile.faculty and (profile.faculty.hod or (profile.faculty.head and profile.faculty.head == course)))
         if not permission:
            return Response({'error': 'You are not allowed to perform this action'}, status=status.HTTP_403_FORBIDDEN)


         serializer = CourseSerializer(course,request.data,partial = request.method =='PATCH')
         if serializer.is_valid():
           serializer.save()
           return Response(serializer.data)
         return Response({'error':str(serializer.errors)},status = status.HTTP_400_BAD_REQUEST)

   except Course.DoesNotExist:
      return Response({'error': 'Faculty not found'}, status=status.HTTP_404_NOT_FOUND)
   except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
@api_view(['POST']) 
@permission_classes([IsAuthenticated, IsHod])
def createCourse(request):
   Course = CourseSerializer(request.data)
   profile = request.user.userprofile
   permission = request.user.is_superuser or (profile.faculty and (profile.faculty.hod and profile.faculty.hod == Course.department))
   if not permission:
             return Response({'error' :'You are not allowed to perform this action'},status =status.HTTP_403_FORBIDDEN)
   if Course.is_valid():
       Course.save()
       return Response({'message':'Course created Successfully'},status=status.HTTP_201_CREATED)
   return Response({'error':str(Course.errors)},status = status.HTTP_400_BAD_REQUEST)
   
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getEnrollments(request):
   EnrollmentFilters = {}
   enrollments = Enrollment.objects.filter(**EnrollmentFilters)
   serializer = EnrollmentSerializer(enrollments,many = True)
   return Response(serializer.data)

@api_view(['POST']) 
@permission_classes([IsAuthenticated])
def createEnrollment(request):
   
   Enrollment = EnrollmentSerializer(request.data)
   if Enrollment.is_valid():
       Enrollment.save()
       return Response({'message':'Enrollment created Successfully'},status=status.HTTP_201_CREATED)
   pass

def crudEnrollment():
   pass

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getLectures(request): 
   LectureFilters = {}
   Lectures = Lecture.objects.filter(**LectureFilters)
   serializer = LectureSerializer(Lectures,many=True)
   return Response(serializer.data)
   pass # get all Lecs, with conditions

@api_view(['GET','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def crudlec(request,pk):
   
   try:
      
      lecture = Lecture.objects.get(pk = pk)
      profile = request.user.userprofile
         
      if request.method == 'GET':
        serializer = LectureSerializer(lecture)
        return Response(serializer.data)
      if request.method == 'DELETE':
         #permission

         permission = request.user.is_superuser or (profile and (profile.faculty and ((profile.faculty == lecture.faculty) or (profile.faculty.hod and profile.faculty.hod == lecture.faculty.department) or (profile.faculty.incharge and profile.faculty.incharge == lecture.class_field.incharge))))
         if not permission :
          return Response({'error': 'You are not allowed to perform this action'}, status=status.HTTP_403_FORBIDDEN)
         
         lecture.delete()
         return Response({'message': 'Lecture deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
      if request.method in ['PUT','PATCH']:
         #permission
         permission = request.user.is_superuser or (profile and (profile.faculty and ((profile.faculty == lecture.faculty) or (profile.faculty.hod and profile.faculty.hod == lecture.faculty.department) or (profile.faculty.incharge and profile.faculty.incharge == lecture.class_field.incharge))))
         if not permission:
          return Response({'error': 'You are not allowed to perform this action'}, status=status.HTTP_403_FORBIDDEN)
         
         serializer = LectureSerializer(lecture,request.data,partial = request.method =='PATCH')
         if serializer.is_valid():
           serializer.save()
           return Response(serializer.data)
     

   except Lecture.DoesNotExist:
      return Response({'error': 'Lecture not found'}, status=status.HTTP_404_NOT_FOUND)
   except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
@api_view(['POST']) 
@permission_classes([IsAuthenticated])
def createLecture(request):
   try:
      profile = request.user.profile

   except UserProfile.DoesNotExist:
      return Response({'error' : 'please sign in '}, status= status.HTTP_403_FORBIDDEN)
   lecture = LectureSerializer(request.data)
   permission = request.user.is_superuser or (profile and (profile.faculty and ((profile.faculty == lecture.faculty) or (profile.faculty.hod and profile.faculty.hod == lecture.faculty.department) or (profile.faculty.incharge and profile.faculty.incharge == lecture.class_field.incharge))))
   if not(permission):
      return Response({'error' : 'You are not allowed to perform this action'}, status = status.HTTP_403_FORBIDDEN)
   
   if lecture.is_valid():
       lecture.save()
       return Response({'message':'Lecture created Successfully'},status=status.HTTP_201_CREATED)
# def crudLecbyRoom():
#    pass
# def crudLecbyCourse():
#    pass

def CountLecsperCourseofaClass():
   pass

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getLabs(request):
   LabFilters = {}
   Labs = Lab.objects.filter(**LabFilters)
   serializer = LabSerializer(Labs,many=True)
   return Response(serializer.data)
   pass # get all Labs

@api_view(['GET','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def crudExtraLab(request,pk):
   try:
      lab = Lab.objects.get(pk = pk)
      profile = request.user.userprofile
      if request.method == 'GET':
        serializer = LabSerializer(lab)
        return Response(serializer.data)
      if request.method == 'DELETE':
         permission = (profile and(profile.faculty and ((profile.faculty == lab.faculty) or (profile.faculty.hod and profile.faculty.head == lab.faculty.department) or (profile.faculty.head and profile.faculty.head == lab.course))))
         if not permission:
             return Response({'error' :'You are not allowed to perform this action'},status =status.HTTP_403_FORBIDDEN)
         lab.delete()
         return Response({'message': 'lab deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
      if request.method in ['PUT','PATCH']:
         permission = (profile and(profile.faculty and ((profile.faculty == lab.faculty) or (profile.faculty.hod and profile.faculty.head == lab.faculty.department) or (profile.faculty.head and profile.faculty.head == lab.course))))
         if not permission:
             return Response({'error' :'You are not allowed to perform this action'},status =status.HTTP_403_FORBIDDEN)
    
         serializer = LabSerializer(lab,request.data,partial = request.method =='PATCH')
         if serializer.is_valid():
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
@permission_classes([IsAuthenticated])
def createLab(request):
   Lab = LabSerializer(request.data)
   if Lab.is_valid():
       Lab.save()
       return Response({'message':'Lab created Successfully'},status=status.HTTP_201_CREATED)
def CountLabsperCourseofaClass():
   pass

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getLecAttendances(request):
   Filters = {}
   if('sid' in request.query_params):
    try:
      s = request.query_params['sid']
      Filters['sid'] = int(s)
    except ValueError:
       return Response("Invalid student id. It should be an integer.", status=400)
   LecAttendances = LecAttendance.objects.filter(**Filters)
   serializer = LecAttendanceSerializer(LecAttendances,many=True)
   return Response(serializer.data)

@api_view(['GET','PATCH','PUT'])
#@permission_classes([CanMarkAttendance])
def crudLecAttendance(request):
   filters = {}
   if('lec' in request.query_params):
    try:
      lec = request.query_params['lec']
      filters['lecid'] = int(lec)
      print("filters updated")
    except ValueError as e:
       return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
   try:
    Att = LecAttendance.objects.filter(**filters)
    present_ids = request.data.get('present_ids',[])
    PresentAtt = Att.filter(sid__in= present_ids)
    Lect = Lecture.objects.get(pk = int(lec))
    print('filtered successfully')
   except Exception as e:
      return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
   
   
   serializer = LecAttendanceSerializer(Att, many = True)
   if request.method == 'GET':
      return Response(serializer.data) 
   
   if request.method == 'PATCH': 
    profile = request.user.userprofile
    lecture = Lect
    permission = request.user.is_superuser or (profile and (profile.faculty and ((profile.faculty == lecture.faculty) or (profile.faculty.hod and profile.faculty.hod == lecture.faculty.department) or (profile.faculty.incharge and profile.faculty.incharge == lecture.class_field))))
    if not permission:
             return Response({'error' :'You are not allowed to perform this action'},status =status.HTTP_403_FORBIDDEN)
    try:
       stat = request.data.get('present')
       PresentAtt.update(present = stat)
       serializer = LecAttendanceSerializer(PresentAtt, many = True)
       return Response(serializer.data)

    except Exception as e:
       return Response({'error':str(e)},status = status.HTTP_400_BAD_REQUEST)
    

    # If validation fails, return an error response
   return Response(serializer.errors, status=400)

   pass # mark attendance of a particular student in a particuar lec
# def crudLecAttendancebyStudent():
#    pass
@api_view(['POST']) 
@permission_classes([IsAdminOrSuperuser])
def createLecAttendance(request):

   LecAttendance = LecAttendanceSerializer(request.data)
   profile = request.user.userprofile

   if LecAttendance.is_valid():
       LecAttendance.save()
       return Response({'message':'LecAttendance created Successfully'},status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getLabAttendance(request):
   Filters = {}
   if('sid' in request.query_params):
    try:
      s = request.query_params['sid']
      Filters['sid'] = int(s)
    except ValueError:
       return Response("Invalid student id. It should be an integer.", status=400)
   LabAttendances = LabAttendance.objects.filter(**Filters)
   serializer = LabAttendanceSerializer(LabAttendances,many=True)
   return Response(serializer.data) # get attendance of all students in a particular lab
# def crudLabAttendancebyBatch():

#    pass # get attendance of all students in a particular batch
@api_view(['GET','PATCH'])
@permission_classes([IsAuthenticated])
def MarkLabAttendance(request):
   print('entered view')
   filters = {}
    
   if('lab' in request.query_params):
     try:
       labid = request.query_params['lab']
       filters['labid'] = int(labid) 
     except ValueError:
       return Response("Invalid class It should be an integer.", status=400)
   
   try:
    Att = LabAttendance.objects.filter(**filters)
    #print(Att)
    PresentIds = request.data.get('present_ids',[])
    PresentAtt = Att.filter(sid__in= PresentIds)
    print(filters)
    if filters['labid']:
      lab = Lab.objects.get(pk = filters['labid'])
      print(lab)

   except Exception as e:
      return Response({'error':str(e)},status = status.HTTP_400_BAD_REQUEST)
   serializer = LabAttendanceSerializer(Att, many = True)
   if(request.method == 'GET'):
      return Response(serializer.data)
      
   if request.method == 'PATCH':
      profile = request.user.userprofile
      permission = request.user.is_superuser or (profile and (profile.faculty and ((profile.faculty == lab.faculty) or (profile.faculty.hod and profile.faculty.hod == lab.faculty.department) or (profile.faculty.incharge and profile.faculty.incharge == lab.class_field.incharge) or (profile.faculty.head and profile.faculty.head == lab.course))))
      if not permission:
             return Response({'error' :'You are not allowed to perform this action'},status =status.HTTP_403_FORBIDDEN)
      
      try:
       stat = request.data.get('present')
       PresentAtt.update(present = stat)
       serializer = LabAttendanceSerializer(PresentAtt, many = True)
       return Response(serializer.data)

      except Exception as e:
       return Response({'error':str(e)},status = status.HTTP_400_BAD_REQUEST)
     

    # If validation fails, return an error response
   return Response(serializer.errors, status=400) # mark attendance of a student in labs
# def crudLabAttendancebyStudent():
#    pass
@api_view(['POST']) 
@permission_classes([IsAdminOrSuperuser])
def createLabAttendance(request):
   LabAttendance = LabAttendanceSerializer(request.data)
   if LabAttendance.is_valid():
       LabAttendance.save()
       return Response({'message':'LabAttendance created Successfully'},status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getTimeTables(request):
   TimetableFilters = {}
   Timetables = Timetable.objects.filter(**TimetableFilters)
   serializer = TimetableSerializer(Timetables,many=True)
   return Response(serializer.data)
   pass # get all timetables
def crudTT():
   pass

@api_view(['POST'])
@permission_classes([IsClassInchargeOrHod])
def createTimeTable(request):
   profile = request.user.userprofile
   TimeTable = TimetableSerializer(request.data)
   permission = profile and (profile.faculty and ((profile.faculty.hod and profile.faculty.hod == TimeTable.class_field.department) or (profile.faculty.incharge and profile.faculty.incharge == TimeTable.class_field)))
   
   if not permission:
           return Response({'error': 'You are not allowed to perform this action'}, status=status.HTTP_403_FORBIDDEN)
   if TimeTable.is_valid():
       TimeTable.save()
       return Response({'message':'TimeTable created Successfully'},status=status.HTTP_201_CREATED)
   return Response({'error':str(TimeTable.errors)},status = status.HTTP_400_BAD_REQUEST)
   


@api_view(['GET','PUT','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def crudTimetable(request,pk):
    try:
      profile = request.user.userprofile
      timetable = Timetable.objects.get(pk = pk)
      

      if request.method == 'GET':
        serializer = TimetableSerializer(timetable)
        return Response(serializer.data)
      if request.method == 'DELETE':

         #permission
         permission = profile and (profile.faculty and ((profile.faculty.hod and profile.faculty.hod == timetable.class_field.department) or (profile.faculty.incharge and profile.faculty.incharge == timetable.class_field)))
         if not permission:
           return Response({'error': 'You are not allowed to perform this action'}, status=status.HTTP_403_FORBIDDEN)

         timetable.delete()
         return Response({'message': 'timetable deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
      if request.method in ['PUT','PATCH']:
         #permission
         permission = profile and (profile.faculty and ((profile.faculty.hod and profile.faculty.hod == timetable.class_field.department) or (profile.faculty.incharge and profile.faculty.incharge == timetable.class_field)))
         if not permission:
           
           return Response({'error': 'You are not allowed to perform this action'}, status=status.HTTP_403_FORBIDDEN)
    
         serializer = TimetableSerializer(timetable,request.data,partial = request.method =='PATCH')
         if serializer.is_valid():
           serializer.save()
           return Response(serializer.data)
         return Response({'error':str(serializer.errors)},status = status.HTTP_400_BAD_REQUEST)
         
    
    except Timetable.DoesNotExist:
      return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def crudTTSlotbyDay():
   pass


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getTimeTableSlots(request):
   TimetableSlotFilters = {}
   TimetableSlots = TimeTableSlot.objects.filter(**TimetableSlotFilters)
   serializer = TimeTableSlotSerializer(TimetableSlots,many=True)
   return Response(serializer.data)


@api_view(['POST']) 
@permission_classes([IsAuthenticated])
def createTimeTableSlot(request):
   profile = request.user.userprofile
   TimeTableSlot = TimeTableSlotSerializer(request.data)
   permission = profile and (profile.faculty and ((profile.faculty.hod and profile.faculty.hod == TimeTableSlot.timetable.class_field.department) or (profile.faculty.incharge and profile.faculty.incharge == TimeTableSlot.timetable.class_field)))
   if not permission:
           return Response({'error': 'You are not allowed to perform this action'}, status=status.HTTP_403_FORBIDDEN)
   if TimeTableSlot.is_valid():
       TimeTableSlot.save()
       return Response({'message':'TimeTableSlot created Successfully'},status=status.HTTP_201_CREATED)


@api_view(['GET','PUT','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def crudTimeTableSlot(request,pk):
    try:
      timeTableSlot = TimeTableSlot.objects.get(pk = pk)
      profile = request.user.userprofile
      if request.method == 'GET': 
        serializer = TimeTableSlotSerializer(timeTableSlot)
        return Response(serializer.data)
      if request.method == 'DELETE':
         #permission
         permission = profile and (profile.faculty and ((profile.faculty.hod and profile.faculty.hod == timeTableSlot.timetable.class_field.department) or (profile.faculty.incharge and profile.faculty.incharge == timeTableSlot.timetable.class_field)))
         if not permission:
           return Response({'error': 'You are not allowed to perform this action'}, status=status.HTTP_403_FORBIDDEN)
    
         timeTableSlot.delete()
         return Response({'message': 'timeTableSlot deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
      if request.method in ['PUT','PATCH']:
         #permission
         permission = profile and (profile.faculty and ((profile.faculty.hod and profile.faculty.hod == timeTableSlot.timetable.class_field.department) or (profile.faculty.incharge and profile.faculty.incharge == timeTableSlot.timetable.class_field)))
         if not permission:
           return Response({'error': 'You are not allowed to perform this action'}, status=status.HTTP_403_FORBIDDEN)
           
         
         serializer = TimeTableSlotSerializer(timeTableSlot,request.data,partial = request.method =='PATCH')
         if serializer.is_valid():
           serializer.save()
           return Response(serializer.data)
    except TimeTableSlot.DoesNotExist:
      return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def getLecLabsPerCourseinTT(request,pk,lec_lab):
   filters = {}
   tt = Timetable.objects.get(pk=pk)
   dateCondition = Q(date__gte = tt.valid_from) and Q(date__lte = tt.valid_till)
   #print('good till condition')
   lecsWithinthisTT = Lecture.objects.filter(dateCondition)
   labsWithinthisTT = Lab.objects.filter(dateCondition)
   #print('err here?')
   
   if('course' in request.query_params):
    try:
      c = request.query_params['course']
      filters['course'] = int(c)
    except ValueError:
       return Response("Invalid student id. It should be an integer.", status=400)
   
   # 1 = lec, lab = 0
   if(lec_lab):
      op = lecsWithinthisTT.filter(**filters)
      serializer = LectureSerializer(op,many=True)
     # print('err here')
      return Response(serializer.data)
   else:
      if('batch' in request.query_params):
        try:
         c = request.query_params['batch']
         filters['batch'] = int(c)
        except ValueError:
          return Response("Invalid student id. It should be an integer.", status=400)
      op = labsWithinthisTT.filter(**filters)
      serializer = LabSerializer(op,many=True)
      return Response(serializer.data)






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