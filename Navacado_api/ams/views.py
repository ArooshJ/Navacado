from django.shortcuts import render
from rest_framework.response import Response # for rest framework api views
from rest_framework.decorators import api_view,permission_classes,parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .permissions import IsAdminOrSuperuser,IsClassInchargeOrHod,IsHod
from .models import Department, Faculty, Class, Batch, Student, Course,Enrollment, Lecture, Lab, Timetable, TimeTableSlot, LecAttendance, LabAttendance,UserProfile
from django.db.models import *
from .serializers import *
from django.contrib.auth.models import User
from datetime import datetime
# Create your views here.
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer # for auth
from rest_framework_simplejwt.views import TokenObtainPairView # for auth

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token
# May be this is also copied
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# Create your views here.


# User is created along with userprofile itself but we can create seperate user only from here:. 
@api_view(['POST'])
def createUser(request):
    serializer = UserSerializer(data = request.data)
    print (request.data)
    if serializer.is_valid():
        user=serializer.save()
      #   accserializer = AccountSerializer(data= {'user':user.pk})
      #   if(accserializer.is_valid()):
      #       accserializer.save()
      #       return Response({'message': 'User registered and Account created successfully'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfiles(request):
   filters = {}
   
   UserProfiles = UserProfile.objects.filter(**filters)
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
# @permission_classes([IsAuthenticated])
def createUserProfile(request):
   # permission = request.user.is_superuser
   # if not permission:
   #       return Response({'error': 'You are not allowed to perform this action on this profile'}, status=status.HTTP_403_FORBIDDEN)
 try:
   us = UserSerializer(data = request.data.get("UserInfo"))
   print(request.data.get("UserInfo"))
   
   if us.is_valid():
      print('user valid')
      ui = us.save()
      print('user created')
      profile_data = request.data.get("ProfileInfo")
      profile_data['user'] = ui.id
      print(profile_data)
      UserProfile = UserProfileSerializer(data =profile_data)
      if UserProfile.is_valid():
        upi = UserProfile.save()
        print('profile created')
        if (request.data.get("FacultyInfo")):
           fac_data = request.data.get("FacultyInfo")
           fac_data['profile'] = upi.profileid
           print(fac_data)
           fac = FacultySerializer(data =fac_data)
           #fac['profile'] = upi.profileid
           if fac.is_valid():
              fac.save()
              print('faculty created')
              return Response({'message':' User and UserProfile and Faculty created Successfully','User' : us.data, 'UserProfile': UserProfile.data, 'Faculty': fac.data},status=status.HTTP_201_CREATED)
           else:
            print(fac.errors)  # Log errors if FacultySerializer fails validation
        if (request.data.get("StudentInfo")):
           print('studetn found')
           fac_data = request.data.get("StudentInfo")
           fac_data['profile'] = upi.profileid
           print(fac_data)
           fac = StudentSerializer(data=fac_data)
           if fac.is_valid():
              print('stu valid')
              fac.save()
              print('Student created')
              return Response({'message':' User and UserProfile and Student created Successfully', 'User' : us.data, 'UserProfile': UserProfile.data, 'Student': fac.data},status=status.HTTP_201_CREATED)
           else:
            print(fac.errors)  # Log errors if StudSerializer fails validation  
         
        return Response({'message':'User and UserProfile created Successfully'},status=status.HTTP_201_CREATED)
      else:
         print(UserProfile.errors)   
      return Response({'message':'User created Successfully'},status=status.HTTP_201_CREATED)
   print(us.errors)
   return Response({'message' : 'dk wtf is this'}, status= status.HTTP_204_NO_CONTENT)
 except Exception as e:
    return Response({'error':str(e)},status=status.HTTP_417_EXPECTATION_FAILED)


# To create profile from currently authenticated user ||
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProfile(request):
    try:
        user = request.user  # Get the currently authenticated user

        profile_data = request.data.get("ProfileInfo")
        if not profile_data:
            return Response({'error': 'Profile information is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        profile_data['user'] = user.id
        user_profile_serializer = UserProfileSerializer(data=profile_data)
        
        if user_profile_serializer.is_valid():
            upi = user_profile_serializer.save()
            print('profile created')
            
            if request.data.get("FacultyInfo"):
                fac_data = request.data.get("FacultyInfo")
                fac_data['profile'] = upi.profileid
                fac = FacultySerializer(data=fac_data)
                if fac.is_valid():
                    fac.save()
                    print('faculty created')
                    return Response({'message': 'UserProfile and Faculty created successfully', 'UserProfile': user_profile_serializer.data, 'Faculty': fac.data}, status=status.HTTP_201_CREATED)
                else: 
                   print(fac.errors)
            if request.data.get("StudentInfo"):
                print('student found')
                stu_data = request.data.get("StudentInfo")
                stu_data['profile'] = upi.profileid
                print(stu_data)
                stu = StudentSerializer(data=stu_data)
                if stu.is_valid():
                    print('student valid')
                    stu.save()
                    print('student created')
                    return Response({'message': 'UserProfile and Student created successfully', 'UserProfile': user_profile_serializer.data, 'Student': stu.data}, status=status.HTTP_201_CREATED)
                else: print(stu.errors)  
            return Response({'message': 'UserProfile created successfully'}, status=status.HTTP_201_CREATED)
        
        return Response(user_profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
   

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
 try:
   Department = DepartmentSerializer(data = request.data)
   if Department.is_valid():
       Department.save()
       return Response({'message':'Department created Successfully'},status=status.HTTP_201_CREATED)
 except Exception as e:
    return Response({'error':str(e)},status=status.HTTP_417_EXPECTATION_FAILED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getFaculties(request):
   filters = {}
   if('dept' in request.query_params):
    try:
      d = request.query_params.get('dept')
      filters['department'] = d
    except ValueError as e:
       return Response({'error':str(e)},status= status.HTTP_403_FORBIDDEN)
   if('hod' in request.query_params):
    try:
      filters['hod__notnull'] = False
    except ValueError as e:
       return Response({'error':str(e)},status= status.HTTP_403_FORBIDDEN)
   if('classincharge' in request.query_params):
    try:
      filters['incharge__notnull'] = False
    except ValueError as e:
       return Response({'error':str(e)},status= status.HTTP_403_FORBIDDEN)
   if('coursehead' in request.query_params):
    try:
      filters['head__notnull'] = False
    except ValueError as e:
       return Response({'error':str(e)},status= status.HTTP_403_FORBIDDEN)
   
   Facultys = Faculty.objects.filter(**filters)
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
   try:
     Faculty = FacultySerializer(data = request.data)
     if Faculty.is_valid():
       Faculty.save()
       return Response({'message':'Faculty created Successfully'},status=status.HTTP_201_CREATED)
   except Exception as e:
     return Response({'error':str(e)},status=status.HTTP_417_EXPECTATION_FAILED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getClasses(request):
   filters = {}
   if('dept' in request.query_params):
    try:
      d = request.query_params.get('dept')
      filters['department'] = d
    except ValueError as e:
       return Response({'error':str(e)},status= status.HTTP_403_FORBIDDEN)
   
   if('year' in request.query_params):
    try:
      d = request.query_params.get('year')
      filters['year'] = d
    except ValueError as e:
       return Response({'error':str(e)},status= status.HTTP_403_FORBIDDEN)
   
   if('acad_yr' in request.query_params):
    try:
      d = request.query_params.get('acad_yr')
      filters['acad_year'] = d
    except ValueError as e:
       return Response({'error':str(e)},status= status.HTTP_403_FORBIDDEN)
   
   Classs = Class.objects.filter(**filters)
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
 try: 
   Class = ClassSerializer(data = request.data)
   permission = request.user.is_superuser or (request.user.userprofile and request.user.userprofile.faculty and request.userprofile.faculty.hod and request.userprofile.faculty.hod == Class.department)
   if not permission:
             return Response({'error' :'You are not allowed to perform this action'},status =status.HTTP_403_FORBIDDEN)
   if Class.is_valid():
       Class.save()
       return Response({'message':'Class created Successfully'},status=status.HTTP_201_CREATED) 
 except Exception as e:
    return Response({'error':str(e)},status=status.HTTP_417_EXPECTATION_FAILED)

def crudClassesbyCondition():
   pass


@api_view(['POST']) 
@permission_classes([IsAuthenticated])

def createBatch(request):
 try:
   Batch = BatchSerializer(data = request.data)
   profile = request.user.userprofile
   permission = request.user.is_superuser or (profile and profile.faculty and profile.faculty.incharge and profile.faculty.incharge == Batch.class_field.incharge)

   if not permission:
             return Response({'error' :'You are not allowed to perform this action'},status =status.HTTP_403_FORBIDDEN)
   if Batch.is_valid():
       Batch.save()
       return Response({'message':'Batch created Successfully'},status=status.HTTP_201_CREATED)
 except Exception as e:
    return Response({'error':str(e)},status=status.HTTP_417_EXPECTATION_FAILED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getBatches(request):
   filters = {}
   if('class' in request.query_params):
    try:
      d = request.query_params.get('class')
      filters['class_field'] = d
    except ValueError as e:
       return Response({'error':str(e)},status= status.HTTP_403_FORBIDDEN)
   Batchs = Batch.objects.filter(**filters)
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
 try:
   Student = StudentSerializer(data = request.data)
   if Student.is_valid():
       Student.save()
       return Response({'message':'Student created Successfully'},status=status.HTTP_201_CREATED)
 except Exception as e:
    return Response({'error':str(e)},status=status.HTTP_417_EXPECTATION_FAILED)
   
    # also returns timetable of the class of that student, total lecs of the class of that student in the sem(as of valid tt), total he has attended, total not attended
  
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
   filters = {}
   if('sem' in request.query_params):
    try:
      d = request.query_params.get('sem')
      filters['semester'] = d
    except ValueError as e:
       return Response({'error':str(e)},status= status.HTTP_403_FORBIDDEN)
   if('dept' in request.query_params):
    try:
      d = request.query_params.get('dept')
      
      filters['department'] = d
    except ValueError as e:
       return Response({'error':str(e)},status= status.HTTP_403_FORBIDDEN)

   courses = Course.objects.filter(**filters)
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
         permission = request.user.is_superuser or (profile.faculty and (profile.faculty.hod or (profile.faculty.head and profile.faculty.head == course)))
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
@permission_classes([IsAuthenticated])
def createCourse(request):
 try:
   Course = CourseSerializer(data = request.data)
   profile = request.user.userprofile
   permission = request.user.is_superuser or (profile.faculty and (profile.faculty.hod and profile.faculty.hod == Course.department))
   if not permission:
             return Response({'error' :'You are not allowed to perform this action'},status =status.HTTP_403_FORBIDDEN)
   if Course.is_valid():
       
       Course.save()
       return Response({'message':'Course created Successfully'},status=status.HTTP_201_CREATED)
   else: print(Course.errors)
   return Response({'error':str(Course.errors)},status = status.HTTP_400_BAD_REQUEST)
 except Exception as e:
    return Response({'error':str(e)},status=status.HTTP_417_EXPECTATION_FAILED)
   
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getEnrollments(request):
   filters = {}
   if('course' in request.query_params):
    try:
      d = request.query_params.get('course')
      filters['cid'] = d
    except ValueError as e:
       return Response({'error':str(e)},status= status.HTTP_403_FORBIDDEN)
   if('sid' in request.query_params):
    try:
      d = request.query_params.get('sid')
      filters['sid'] = d
    except ValueError as e:
       return Response({'error':str(e)},status= status.HTTP_403_FORBIDDEN)
   
   enrollments = Enrollment.objects.filter(**filters)
   serializer = EnrollmentSerializer(enrollments,many = True)
   return Response(serializer.data)

@api_view(['POST']) 
@permission_classes([IsAuthenticated])
def createEnrollment(request):
 try:
   Enrollment = EnrollmentSerializer(data =request.data)
   if Enrollment.is_valid():
       Enrollment.save()
       return Response({'message':'Enrollment created Successfully'},status=status.HTTP_201_CREATED)
 except Exception as e:
    return Response({'error':str(e)},status=status.HTTP_417_EXPECTATION_FAILED)
   

def crudEnrollment():
   pass

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getLectures(request): 
   filters = {}
   if('date' in request.query_params):
    try:
      d = request.query_params.get('date')
      date_object = datetime.strptime(d, '%d-%m-%Y').date()
      filters['date'] = date_object
    except ValueError as e:
       return Response({'error':str(e)},status= status.HTTP_403_FORBIDDEN)
  
   if('from' in request.query_params):
    try:
      d = request.query_params.get('from')
      date_object = datetime.strptime(d, '%d-%m-%Y').date()
      filters['date__gte'] = date_object
    except ValueError as e:
       return Response({'error':str(e)},status= status.HTTP_403_FORBIDDEN)
   
   if('to' in request.query_params):
    try:
      d = request.query_params.get('to')
      date_object = datetime.strptime(d, '%d-%m-%Y').date()
      filters['date__lte'] = date_object
    except ValueError as e:
       return Response({'error':str(e)},status= status.HTTP_403_FORBIDDEN)
   
   if('course' in request.query_params):
    try:
      d = request.query_params.get('course')
      #date_object = datetime.strptime(d, '%d-%m-%Y').date()
      filters['course'] = d
    except ValueError as e:
       return Response({'error':str(e)},status= status.HTTP_403_FORBIDDEN)
   
   if('slot' in request.query_params):
    try:
      d = request.query_params.get('slot')
      #date_object = datetime.strptime(d, '%d-%m-%Y').date()
      filters['slot'] = d
    except ValueError as e:
       return Response({'error':str(e)},status= status.HTTP_403_FORBIDDEN)
   
   if('start' in request.query_params):
    try:
      d = request.query_params.get('start')
      #print(d)
      time_object = datetime.strptime(d, '%H:%M').time()
     #-  print(time_object)
      filters['start_time'] = time_object
    except ValueError as e:
       return Response({'error':str(e)},status= status.HTTP_403_FORBIDDEN)
    
   Lectures = Lecture.objects.filter(**filters).order_by('start_time')
   serializer = LectureSerializer(Lectures,many=True)
   return Response(serializer.data)
   pass # get all Lecs, with conditions

@api_view(['GET','DELETE'])
def crudLecsConditional(request):
   filters = {}
   if('date' in request.query_params):
    try:
      d = request.query_params.get('date')
      date_object = datetime.strptime(d, '%d-%m-%Y').date()
      filters['date'] = date_object
    except ValueError as e:
       return Response({'error':str(e)},status= status.HTTP_403_FORBIDDEN)
   lecs = Lecture.objects.filter(**filters) 

   try:
     if request.method == 'GET':
      serializer = LectureSerializer(lecs, many=True)
      return Response(serializer.data)
     if request.method == 'DELETE':
      lecs.delete()
      return Response("Deleted Successfully", status=status.HTTP_200_OK)
   
   except Exception as e:
     return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)


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

   lecture = LectureSerializer(data = request.data)
   permission = request.user.is_superuser or (profile and (profile.faculty and ((profile.faculty == lecture.faculty) or (profile.faculty.hod and profile.faculty.hod == lecture.faculty.department) or (profile.faculty.incharge and profile.faculty.incharge == lecture.class_field.incharge))))
   if not(permission):
      return Response({'error' : 'You are not allowed to perform this action'}, status = status.HTTP_403_FORBIDDEN)
   
   if lecture.is_valid():
       lecture.save()
       return Response({'message':'Lecture created Successfully'},status=status.HTTP_201_CREATED)
 except Exception as e:
    return Response({'error':str(e)},status=status.HTTP_417_EXPECTATION_FAILED)
 
# def crudLecbyRoom():
#    pass
# def crudLecbyCourse():
#    pass

def CountLecsperCourseofaClass():
   pass

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getLabs(request):
   filters = {}
   if('date' in request.query_params):
    try:
      d = request.query_params.get('date')
      date_object = datetime.strptime(d, '%d-%m-%Y').date()
      filters['date'] = date_object
    except ValueError as e:
       return Response({'error':str(e)},status= status.HTTP_403_FORBIDDEN)
   if('start' in request.query_params):
    try:
      d = request.query_params.get('start')
      time_object = datetime.strptime(d, '%H:%M').time()
      filters['start_time'] = time_object
    except ValueError as e:
       return Response({'error':str(e)},status= status.HTTP_403_FORBIDDEN)
   if('from_date' in request.query_params):
    try:
      d = request.query_params.get('from_date')
      date_object = datetime.strptime(d, '%d-%m-%Y').date()
      filters['date__gte'] = date_object
    except ValueError as e:
       return Response({'error':str(e)},status= status.HTTP_403_FORBIDDEN)
   
   if('to_date' in request.query_params):
    try:
      d = request.query_params.get('to_date')
      date_object = datetime.strptime(d, '%d-%m-%Y').date()
      filters['date__lte'] = date_object
    except ValueError as e:
       return Response({'error':str(e)},status= status.HTTP_403_FORBIDDEN)
   Labs = Lab.objects.filter(**filters)
   serializer = LabSerializer(Labs,many=True)
   return Response(serializer.data)
   pass # get all Labs

@api_view(['GET','DELETE'])
def crudLabsConditional(request):
   filters = {}
   if('date' in request.query_params):
    try:
      d = request.query_params.get('date')
      date_object = datetime.strptime(d, '%d-%m-%Y').date()
      filters['date'] = date_object
    except ValueError as e:
       return Response({'error':str(e)},status= status.HTTP_403_FORBIDDEN)
   labs = Lab.objects.filter(**filters)

   if request.method == 'GET':
      serializer = LabSerializer(labs, many=True)
      return Response(serializer.data)
   if request.method == 'DELETE':
      labs.delete()
      return Response("Deleted Successfully", status=status.HTTP_200_OK)
   return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)



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
 try:
   Lab = LabSerializer(data = request.data)
   if Lab.is_valid():
       Lab.save()
       return Response({'message':'Lab created Successfully'},status=status.HTTP_201_CREATED)
 except Exception as e:
    return Response({'error':str(e)},status=status.HTTP_417_EXPECTATION_FAILED)
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
   if('lec' in request.query_params):
    try:
      s = request.query_params['lec']
      Filters['lecid'] = int(s)
    except ValueError:
       return Response("Invalid lec id. It should be an integer.", status=400)
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
 try:
   LecAttendance = LecAttendanceSerializer(data = request.data)
   profile = request.user.userprofile

   if LecAttendance.is_valid():
       LecAttendance.save()
       return Response({'message':'LecAttendance created Successfully'},status=status.HTTP_201_CREATED)
 except Exception as e:
    return Response({'error':str(e)},status=status.HTTP_417_EXPECTATION_FAILED)

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
   if('labid' in request.query_params):
    try:
      s = request.query_params['labid']
      Filters['labid'] = int(s)
    except ValueError:
       return Response("Invalid lab id. It should be an integer.", status=400)
   if('from_date' in request.query_params):
    try:
      d = request.query_params.get('from_date')
      date_object = datetime.strptime(d, '%d-%m-%Y').date()
      Filters['labid__date__gte'] = date_object
    except ValueError as e:
       return Response({'error':str(e)},status= status.HTTP_403_FORBIDDEN)
   
   if('to_date' in request.query_params):
    try:
      d = request.query_params.get('to_date')
      date_object = datetime.strptime(d, '%d-%m-%Y').date()
      Filters['labid__date__lte'] = date_object
    except ValueError as e:
       return Response({'error':str(e)},status= status.HTTP_403_FORBIDDEN)
   LabAttendances = LabAttendance.objects.filter(**Filters)
   serializer = LabAttendanceSerializer(LabAttendances,many=True)
   return Response(serializer.data) # get attendance of all students in a particular lab
# def crudLabAttendancebyBatch():

#    pass # get attendance of all students in a particular batch
@api_view(['GET','PATCH'])
@permission_classes([IsAuthenticated])
def MarkLabAttendance(request):
   #print('entered view')
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
 try:
   LabAttendance = LabAttendanceSerializer(data = request.data)
   if LabAttendance.is_valid():
       LabAttendance.save()
       return Response({'message':'LabAttendance created Successfully'},status=status.HTTP_201_CREATED)
 except Exception as e:
    return Response({'error':str(e)},status=status.HTTP_417_EXPECTATION_FAILED)

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
@permission_classes([IsAuthenticated])
def createTimeTable(request):
 try:
   profile = request.user.userprofile
   TimeTable = TimetableSerializer(data = request.data)
   permission = request.user.is_superuser or (profile and (profile.faculty and ((profile.faculty.hod and profile.faculty.hod == TimeTable.class_field.department) or (profile.faculty.incharge and profile.faculty.incharge == TimeTable.class_field))))
   
   if not permission:
           return Response({'error': 'You are not allowed to perform this action'}, status=status.HTTP_403_FORBIDDEN)
   if TimeTable.is_valid():
       TimeTable.save()
       return Response({'message':'TimeTable created Successfully'},status=status.HTTP_201_CREATED)
   return Response({'error':str(TimeTable.errors)},status = status.HTTP_400_BAD_REQUEST)
 except Exception as e:
    return Response({'error':str(e)},status=status.HTTP_417_EXPECTATION_FAILED)
   


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
   Filters = {}
   if('tt' in request.query_params):
    try:
      s = request.query_params['tt']
      Filters['ttid'] = int(s)
    except ValueError:
       return Response("Invalid tt id. It should be an integer.", status=400)
   if('day' in request.query_params):
    try:
      s = request.query_params['day']
      Filters['day'] = int(s)
    except ValueError:
       return Response("Invalid tt id. It should be an integer.", status=400)
   if('sem' in request.query_params):
    try:
      s = request.query_params['sem']
      Filters['ttid__semester'] = int(s)
    except ValueError:
       return Response("Invalid tt id. It should be an integer.", status=400)

   TimetableSlots = TimeTableSlot.objects.filter(**Filters).order_by('day', 'start_time')
   serializer = TimeTableSlotSerializer(TimetableSlots,many=True)
   return Response(serializer.data)


@api_view(['POST']) 
@permission_classes([IsAuthenticated])
def createTimeTableSlot(request):
 try:
   profile = request.user.userprofile
   TimeTableSlot = TimeTableSlotSerializer(data = request.data)
   permission = request.user.is_superuser or (profile and (profile.faculty and ((profile.faculty.hod and profile.faculty.hod == TimeTableSlot.timetable.class_field.department) or (profile.faculty.incharge and profile.faculty.incharge == TimeTableSlot.timetable.class_field))))
   if not permission:
           return Response({'error': 'You are not allowed to perform this action'}, status=status.HTTP_403_FORBIDDEN)
   if TimeTableSlot.is_valid():
       TimeTableSlot.save()
       return Response({'message':'TimeTableSlot created Successfully'},status=status.HTTP_201_CREATED)
 except Exception as e:
    return Response({'error':str(e)},status=status.HTTP_417_EXPECTATION_FAILED)

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
         permission = request.user.is_superuser or (profile and (profile.faculty and ((profile.faculty.hod and profile.faculty.hod == timeTableSlot.timetable.class_field.department) or (profile.faculty.incharge and profile.faculty.incharge == timeTableSlot.timetable.class_field))))
         if not permission:
           return Response({'error': 'You are not allowed to perform this action'}, status=status.HTTP_403_FORBIDDEN)
    
         timeTableSlot.delete()
         return Response({'message': 'timeTableSlot deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
      if request.method in ['PUT','PATCH']:
         #permission
         permission = request.user.is_superuser or (profile and (profile.faculty and ((profile.faculty.hod and profile.faculty.hod == timeTableSlot.timetable.class_field.department) or (profile.faculty.incharge and profile.faculty.incharge == timeTableSlot.timetable.class_field))))
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
   if(lec_lab == 1):
      op = lecsWithinthisTT.filter(**filters)
      serializer = LectureSerializer(op,many=True)
     # print('err here')
      return Response(serializer.data)
   elif(lec_lab == 0):
      if('batch' in request.query_params):
        try:
         c = request.query_params['batch']
         filters['batch'] = int(c)
        except ValueError:
          return Response("Invalid student id. It should be an integer.", status=400)
      op = labsWithinthisTT.filter(**filters)
      serializer = LabSerializer(op,many=True)
      return Response(serializer.data)
   
@api_view(['GET'])
def getTotalLecLabsPerCourseinTT(request,pk,lec_lab):
   filters = {}
   tt = Timetable.objects.get(pk=pk)
   dateCondition = Q(date__gte = tt.valid_from) and Q(date__lte = tt.valid_till)
   #print('good till condition')
   lecsWithinthisTT = Lecture.objects.filter(dateCondition)
   labsWithinthisTT = Lab.objects.filter(dateCondition)
   #print('err here?')
   
  
   
   # 1 = lec, lab = 0
   if(lec_lab == 1):
      op = lecsWithinthisTT.filter(**filters).values('course').annotate(lec_count = Count(id))
      serializer = LectureCountSerializer(op,many=True)
     # print('err here')
      return Response(serializer.data)
   elif(lec_lab == 0):
      if('batch' in request.query_params):
        try:
         c = request.query_params['batch']
         filters['batch'] = int(c)
        except ValueError:
          return Response("Invalid student id. It should be an integer.", status=400)
     
      op = labsWithinthisTT.filter(**filters).values('course').annotate(lab_count = Count(id))
    
      serializer = LabCountSerializer(op,many=True)
      return Response(serializer.data)
   





@api_view(['GET'])
def getPercentAttendanceofStudentinaCourseLecs(request,pk,lec_lab):
   filters = {}
   AttFilters ={}
   tt = Timetable.objects.get(pk=pk)
   from_date = tt.valid_from
   to_date = tt.valid_till
   if('course' in request.query_params):
    try:
      c = request.query_params['course']
      filters['course'] = int(c)
    except ValueError:
       return Response("Invalid course id. It should be an integer.", status=400)
   
   if('sid' in request.query_params):
       try:
        s = request.query_params['sid']
        AttFilters['sid'] = int(s)
       except ValueError:
        return Response("Invalid student id. It should be an integer.", status=400)
   if('from_date' in request.query_params):
    try:
      d = request.query_params.get('from_date')
      date_object = datetime.strptime(d, '%d-%m-%Y').date()
      from_date = date_object
    except ValueError as e:
       return Response({'error':str(e)},status= status.HTTP_403_FORBIDDEN)
   if('to_date' in request.query_params):
    try:
      d = request.query_params.get('to_date')
      date_object = datetime.strptime(d, '%d-%m-%Y').date()
      to_date = date_object
    except ValueError as e:
       return Response({'error':str(e)},status= status.HTTP_403_FORBIDDEN)
   
   
   
   dateCondition = Q(date__gte = from_date) and Q(date__lte = to_date)
   #print('good till condition')
   lecsWithinthisTT = Lecture.objects.filter(dateCondition)
   labsWithinthisTT = Lab.objects.filter(dateCondition)
   LeccoursesInThisTT = lecsWithinthisTT.values('course').distinct() 
   #print(LeccoursesInThisTT)
   LabcoursesInThisTT = labsWithinthisTT.values('course').distinct() 
   #print('err here?')
   lecslotsinThistt = TimeTableSlot.objects.filter(ttid = tt.id, lec_lab =1).values('course').distinct()
   labslotsinThistt = TimeTableSlot.objects.filter(ttid = tt.id, lec_lab =0).values('course').distinct()
   

   # 1 = lec, lab = 0
   if(lec_lab == 1):
    Data = []
    for c in lecslotsinThistt:
      #print(c)
      
      lecscount = lecsWithinthisTT.values('course').annotate(lec_count =  Count(id))
      lecsofCourse = lecsWithinthisTT.filter(course = c['course'])
      lecAttsofCourse = LecAttendance.objects.filter(lecid__in = lecsofCourse)
      lecAttsofStudentinCourse = lecAttsofCourse.filter(**AttFilters)
      TotalAttended = lecAttsofStudentinCourse.filter(present = True).count()
      
      percentAttendance = TotalAttended * 100/lecsofCourse.count()
      print(percentAttendance)
      AttendacneStats = {'Course': c['course'],'TotalLecs' : lecsofCourse.count(), 'LecsAttended' : TotalAttended, 'PercentAttendance' : percentAttendance }
      Data.append(AttendacneStats)
       

    
    serializer = LecAttendacnceStatSerializer(Data,many=True)
     # print('err here')
    return Response(serializer.data)
   
   elif(lec_lab == 0):
    Data = []
    for c in labslotsinThistt:
      if('batch' in request.query_params):
        try:
         b = request.query_params['batch']
         filters['batch'] = int(b)
        except ValueError:
          return Response("Invalid student id. It should be an integer.", status=400)
     
      op = labsWithinthisTT.filter(batch = int(b)).values('course').annotate(lab_count = Count(id))
      labsofCourse = labsWithinthisTT.filter(course = c['course'])
      labAttsofCourse = LabAttendance.objects.filter(labid__in = labsofCourse)
      labAttsofStudentinCourse = labAttsofCourse.filter(**AttFilters)
      TotalAttended = labAttsofStudentinCourse.filter(present = True).count()

      percentAttendance = TotalAttended * 100/labsofCourse.count()
      print(percentAttendance)
      AttendanceStats = {'Course': c['course'],'TotalLabs' : labsofCourse.count(), 'LabsAttended' : TotalAttended, 'PercentAttendance' : percentAttendance }
      Data.append(AttendanceStats)
    serializer = LabAttendacnceStatSerializer(Data,many =True)
    return Response(serializer.data)
   pass 


def getPercentAttendanceofStudentinaCourseLabs():
   pass
def getPercentAttendanceofAllStudentinaCourseLecs():
   pass
def getPercentAttendanceofAllStudentinaCourseLabs():
   pass
