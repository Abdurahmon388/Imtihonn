from django.contrib import admin
from .models import *

admin.site.register([ User, Teacher, Student, Payment, Subject, TokenModel, Course,
    Departments, Worker, Group, Parent, Attendance, AttendanceLevel,
    Topics, GroupHomeWork, HomeWork, Day, Rooms, TableType, Table,
    PaymentType, TeacherCourse, TeacherDepartments, Comment, MockData, Status
    ])


# from .models import (
#     User, Teacher, Student, Payment, Subject, TokenModel, Course,
#     Departments, Worker, Group, Parents, Attendance, AttendanceLevel,
#     Topics, GroupHomeWork, HomeWork, Day, Rooms, TableType, Table,
#     PaymentType, TeacherCourse, TeacherDepartments, Comment
# )

# # **Barcha modellarni oddiy usulda ro'yxatga olish**
# admin.site.register(User)
# admin.site.register(Teacher)
# admin.site.register(Student)
# admin.site.register(Payment)
# admin.site.register(Subject)
# admin.site.register(TokenModel)
# admin.site.register(Course)
# admin.site.register(Departments)
# admin.site.register(Worker)
# admin.site.register(Group)
# admin.site.register(Parents)
# admin.site.register(Attendance)
# admin.site.register(AttendanceLevel)
# admin.site.register(Topics)
# admin.site.register(GroupHomeWork)
# admin.site.register(HomeWork)
# admin.site.register(Day)
# admin.site.register(Rooms)
# admin.site.register(TableType)
# admin.site.register(Table)
# admin.site.register(PaymentType)
# admin.site.register(TeacherCourse)
# admin.site.register(TeacherDepartments)
# admin.site.register(Comment)