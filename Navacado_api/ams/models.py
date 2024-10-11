from django.db import models
from django.contrib.auth.models import User, Group
from datetime import timedelta
from django.db.models import *
 

# Create your models here. aj@Nav AJ

class UserProfile(models.Model):
    profileid = models.AutoField(primary_key=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='userprofile')
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True,blank=True)
    phone = models.BigIntegerField(null=True,blank=True)
    date_of_birth = models.DateField()
    # is_cr = models.BooleanField(default=False)
    # is_br = models.BooleanField(default=False)
    # is_hod = models.BooleanField(default=False)
    # is_coursehead = models.BooleanField(default=False)
    # is_classIncharge = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        super().save(*args,**kwargs)
        
        pass


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    dname = models.CharField(max_length=255)
    hod = models.OneToOneField('Faculty', on_delete=models.SET_NULL, null=True, blank=True, related_name='hod')
    def __str__(self):
        return self.dname
    
    # def save(self,*args,**kwargs):
    #     super().save(*args,**kwargs)
    #     #self.hod.profile.is_hod = True


class Faculty(models.Model):
    id = models.BigAutoField(primary_key=True)
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE,related_name = 'faculty')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='faculty')
    def __str__(self):
        return self.profile.name

class Class(models.Model):
    id = models.AutoField(primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='classes')
    year = models.IntegerField()
    division = models.CharField(max_length=1)
    acad_year = models.CharField(max_length=10)
    incharge = models.OneToOneField('Faculty',on_delete=models.SET_NULL, null=True, related_name= 'incharged_class')
    cr = models.ForeignKey('Student', on_delete=models.SET_NULL, null=True, blank=True, related_name='class_representatives')
    def __str__(self):
        return f"{self.department}, {self.year}, {self.division}, {self.acad_year}"
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        pass

class Batch(models.Model):
    id = models.AutoField(primary_key=True)
    bname = models.CharField(max_length=255)
    class_field = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='batches')
    br = models.ForeignKey('Student', on_delete=models.SET_NULL, null=True, blank=True, related_name='batch_representatives')
    def __str__(self):
        return f"Batch {self.bname}, {self.class_field}"

class Student(models.Model):
    uid = models.BigAutoField(primary_key=True)
    profile = models.OneToOneField(UserProfile,on_delete=models.CASCADE,related_name='student')
    joined_year = models.IntegerField()
    class_field = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='student',null = True, blank = True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='students', null=True, blank=True)
    def __str__(self):
        return self.profile.name
    def save(self, *args, **kwargs):
     if self.uid == None:
       super().save(*args,**kwargs)
       if self.class_field:
            lecs = Lecture.objects.filter(class_field = self.class_field)
            for lec in lecs:
                LecAttendance.objects.create(
                    sid = self,
                    lecid = lec,
                )
       if self.batch:
            labs = Lab.objects.filter(batch = self.batch)
            for lab in labs:
                LabAttendance.objects.create(
                    sid = self,
                    labid = lab,
                )
     else: 
        super().save(*args,**kwargs)

        


class Course(models.Model):
    cid = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=255)
    semester = models.IntegerField()
    head = models.OneToOneField(Faculty, on_delete=models.SET_NULL, null=True, blank=True, related_name='head')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    def __str__(self):
        return self.cname

class Enrollment(models.Model):
    id = models.AutoField(primary_key=True)
    cid = models.ForeignKey(Course,on_delete= models.CASCADE)
    sid = models.ForeignKey(Student,on_delete=models.CASCADE)

class Timetable(models.Model):
    id = models.AutoField(primary_key=True)
    class_field = models.ForeignKey(Class, related_name='timetables',on_delete=models.CASCADE,null=True)
    semester = models.IntegerField()
    valid_from = models.DateField(null=True, blank=True)
    valid_till = models.DateField(null=True, blank=True)
    def __str__(self):
        return f" {self.class_field} ,{self.semester}"

class TimeTableSlot(models.Model):
    id = models.BigAutoField(primary_key=True)
    ttid = models.ForeignKey(Timetable, on_delete=models.CASCADE, related_name='time_table_slots')
    day = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    lec_lab = models.BooleanField(default=True) # = 1 for lec and 0 for labs
    batch = models.ForeignKey(Batch, on_delete = models.CASCADE,null = True,blank=True)
    def __str__(self):
        Days = {1:'Mon',2:'Tue',3:'Wed',4:'Thu',5:'Fri',6:'Sat',7:'Sun'}
        return f"{self.course}, {Days[self.day]}, {self.start_time}"
    def save(self, *args, **kwargs):
     if self.id == None:
        super().save(*args,**kwargs)
        print('saved self')
        if self.ttid.valid_from and self.ttid.valid_till:
            current_date = self.ttid.valid_from
            current_day_of_week = current_date.isoweekday()
            days_until_target = (self.day - current_day_of_week) % 7
            current_date += timedelta(days=days_until_target)
            while current_date <= self.ttid.valid_till:
             if self.lec_lab:
                Lecture.objects.create(
                    course=self.course,
                    class_field= self.ttid.class_field,
                    faculty=self.faculty,
                    date=current_date,
                    start_time=self.start_time,
                    end_time=self.end_time,
                    slot = self
                )
                print('creating lec\n')
                print(f"Current date: {current_date}, Valid till: {self.ttid.valid_till}")
                current_date += timedelta(days=7)

             else:
                Lab.objects.create(
                    course=self.course,
                    batch=self.batch,
                    faculty=self.faculty,
                    date=current_date,
                    start_time=self.start_time,
                    end_time=self.end_time,
                    slot = self
                )
                print('creating lab')
                current_date += timedelta(days=7)

                

                # Increment current_date by 7 days for the next week
            current_date += timedelta(days=7)
     else:
         oldday = self.day
         super().save(*args,**kwargs)
         newday = self.day
         print(newday - oldday)
       #timecons = Q(date__gte = self.ttid__valid_from) and Q(date__lte = self.ttid__valid_till)
         if self.lec_lab:
            lecs = Lecture.objects.filter(slot = self)
            for lec in lecs:
               lec.course = self.course
               lec.faculty = self.faculty
               lec.start_time = self.start_time
               lec.end_time = self.end_time
               daychange = newday - oldday
               if daychange < 0 : daychange += 7
               lec.date += timedelta(days = daychange)
               lec.save()
         else:
            labs = Lab.objects.filter(slot = self)
            for lec in labs:
               lec.course = self.course
               lec.faculty = self.faculty
               lec.start_time = self.start_time
               lec.end_time = self.end_time
               lec.batch = self.batch
               daychange = newday - oldday
               if daychange < 0 : daychange += 7
               lec.date += timedelta(days = daychange)
               lec.save()
 
         
         


class Lecture(models.Model):
    id = models.BigAutoField(primary_key=True)
    course = models.ForeignKey(Course, related_name='lectures',on_delete=models.CASCADE,null=True)
    class_field = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='lectures',null=True)
    faculty = models.ForeignKey(Faculty, related_name='lectures',on_delete=models.SET_NULL,null=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.IntegerField(null=True,blank=True) 
    slot = models.ForeignKey(TimeTableSlot, on_delete = models.CASCADE, null = True, blank = True)
    def save(self,*args,**kwargs):
      if self.id == None:
        super().save(*args,**kwargs)
        classList = Student.objects.filter(class_field = self.class_field)
        for s in classList:
            # print(s.profile.name)
            LecAttendance.objects.create(
                sid = s,
                lecid = self,
            )
      else:
          super().save(*args,*kwargs)
    def __str__(self):
            Days = {1:'Mon',2:'Tue',3:'Wed',4:'Thu',5:'Fri',6:'Sat',7:'Sun'}
            return f"{self.course}, {self.class_field}, {self.date}, {self.start_time}"


class Lab(models.Model):
    id = models.BigAutoField(primary_key=True)
    course = models.ForeignKey(Course, related_name='labs',on_delete=models.CASCADE,null=True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='labs', null=True, blank=True)
    faculty = models.ForeignKey(Faculty, related_name='labs',on_delete=models.SET_NULL,null=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.IntegerField(null = True, blank= True)
    slot = models.ForeignKey(TimeTableSlot, on_delete = models.CASCADE, null = True, blank = True)

    def save(self,*args,**kwargs):
     if self.id == None:
        super().save(*args,**kwargs)
        batchList = Student.objects.filter(batch = self.batch)
        for s in batchList:
            print(s.profile.name)
            LabAttendance.objects.create(
                sid = s,
                labid = self,
            )
     else:
         super().save(*args,**kwargs)
 


class LecAttendance(models.Model):
    id = models.BigAutoField(primary_key=True)
    sid = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='lecture_attendance')
    lecid = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='attendance')
    present = models.BooleanField(default=False)

class LabAttendance(models.Model):
    id = models.BigAutoField(primary_key=True)
    sid = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='lab_attendance')
    labid = models.ForeignKey(Lab, on_delete=models.CASCADE, related_name='attendance')
    present = models.BooleanField(default=False)

# alter table table_name auto_increment = 1;