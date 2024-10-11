from .models import Department, Faculty, Class, Batch, Student, Course,Enrollment, Lecture, Lab, Timetable, TimeTableSlot, LecAttendance, LabAttendance,UserProfile
from .serializers import DepartmentSerializer,FacultySerializer,ClassSerializer,BatchSerializer,StudentSerializer,EnrollmentSerializer,CourseSerializer,LectureSerializer,LecAttendanceSerializer,LabSerializer,LabAttendanceSerializer,TimeTableSlotSerializer,TimetableSerializer,UserProfileSerializer
from rest_framework.permissions import BasePermission



class CanMarkAttendance(BasePermission):#useless
    message = "You arent authorized to mark attendance"
    def has_permission(self, request, view):
        l = request.data.get("Lecture")
        la = request.data.get("Lab")
        
        lec = Lecture.objects.get(pk = l)
        lab = Lab.objects.get(pk = la)
        return (
            request.user.userprofile.faculty.exists()
              and(request.user.userprofile.faculty == lec.faculty or request.user.userprofile.faculty == lab.faculty)
              ) or request.user.userprofile.is_hod or request.user.userprofile.is_coursehead or request.user.userprofile.is_classIncharge


class IsClassInchargeOrHod(BasePermission):
    def has_permission(self, request, view):
        user_profile = request.user.userprofile

        # Check if the user has the necessary permissions
        return user_profile.faculty and (
            user_profile.faculty.hod.exists() or user_profile.faculty.classincharge.exists()
        )

class IsHod(BasePermission):
    def has_permission(self, request, view):
        profile = request.user.profile
        return profile.faculty and profile.faculty.hod.exists()



class IsAdminOrSuperuser(BasePermission):
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        # Check if the user is an admin or superuser
        return request.user.is_staff or request.user.is_superuser
    

    