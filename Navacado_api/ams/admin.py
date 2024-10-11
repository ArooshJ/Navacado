from django.contrib import admin

from .models import Department, Faculty, Class, Batch, Student, Course,Enrollment, Lecture, Lab, Timetable, TimeTableSlot, LecAttendance, LabAttendance,UserProfile

# Register your models here.

admin.site.register(Department)
admin.site.register(Faculty)
admin.site.register(Class)
admin.site.register(Batch)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(Lab)
admin.site.register(Timetable)
admin.site.register(TimeTableSlot)
admin.site.register(LecAttendance)
admin.site.register(LabAttendance)
admin.site.register(UserProfile)
admin.site.register(Enrollment)

