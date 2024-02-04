Navacado is an Attendance Management System API designed to streamline and manage attendance-related tasks in an educational institution. This system includes features for managing departments, students, courses, timetables, profiles, faculties, classes, batches, lectures, labs, enrollments, and attendance records.

This System allows Automatic creation of Lectures and Labs based on the information given in TimeTables and TimeTableSlots. A TimeTable has a validity period and Timetable slot contains all the information regarding the lecture day of the week,timings,course,faculty,class,etc.. Thus, lectures or labs are created at their respective dates based on validity period and day of week. Each lecture/lab has associated with it an attendance roster, which contains all the students of the class in which that lecture/lab is taken in and whether the student is present or not.

Based on this data, the system calculates the total lecs attended, percentage attendance of any student in lectures during a timetable, or within a specific time periods, for specific courses, etc based on the data in the database.

Beisdes this, there are views for CRUD for each model mention in the first para. Attempt has been made to manage permissions for each view, where certain crud privileges are given to faculties, hods, class incharges, course heads and superusers

The System is currently a restAPI created completely using django REST framework while the database used for testing is a local MySQL database.
