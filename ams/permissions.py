from .models import Department, Faculty, Class, Batch, Student, Course,Enrollment, Lecture, Lab, Timetable, TimeTableSlot, LecAttendance, LabAttendance,UserProfile
from .serializers import DepartmentSerializer,FacultySerializer,ClassSerializer,BatchSerializer,StudentSerializer,EnrollmentSerializer,CourseSerializer,LectureSerializer,LecAttendanceSerializer,LabSerializer,LabAttendanceSerializer,TimeTableSlotSerializer,TimetableSerializer,UserProfileSerializer
from rest_framework.permissions import BasePermission


class CanMarkAttendance(BasePermission):
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


  