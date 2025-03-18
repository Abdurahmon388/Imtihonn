from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from app_config.views import PopulateMockDataView
from rest_framework_simplejwt.views import (
    TokenObtainSlidingView,
    TokenRefreshSlidingView, TokenVerifyView, TokenBlacklistView
)
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'attendances/levels', AttendanceLevelViewSet, basename='attendancelevel')
router.register(r'attendances', AttendanceViewSet, basename='attendance')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'homework-reviews', GroupHomeWorkViewSet, basename='homeworkreview')
router.register(r'homework-submissions', HomeWorkViewSet, basename='homeworksubmission')
router.register(r'table-types', TableTypeViewSet, basename='tabletype')
router.register(r'tables', TableViewSet, basename='table')
# router.register(r'students', , basename='student')
router.register(r'parent', ParentViewSet, basename='parent')
router.register(r'workers', WorkerViewSet, basename='worker')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'teachers', TeacherViewSet, basename='teachers')
router.register(r'populate-mock-data', MockDataViewSet, basename="mockdata")
router.register(r'statuses', StatusViewSet, basename='status')



urlpatterns = [
    path('', UserListView.as_view(), name='user-list'), 
    path('user/<int:id>/', UserDetailView.as_view(), name='user-detail'), 
    
    path('create/student/', StudentCreateAPIView.as_view(), name='create-student'),
    path('create/teacher/', TeacherCreateAPIView.as_view(), name='create-teacher'),
    
    # Teacher CRUD
    path('teachers/',TeacherListView.as_view(),name="all_teachers"),
    path('teacher/<int:id>/',TeacherRetrieveAPIView.as_view(),name="teacher"),
    path('create/teacher/',TeacherCreateAPIView.as_view(), name='add_teacher'),
    path('update/teacher/<int:id>/',TeacherUpdateView.as_view(), name="update_teacher"),
    path('teacher-groups/<int:teacher_id>/',TeacherGroupsAPIView.as_view(), name="teacher_groups"),
    path('get-teachers-by-ids/',GetTeachersByIds.as_view(), name='teachers-by-id'),

    # Student CRUD
    path('students/', StudentListCreateAPIView.as_view(), name='student-list-create'),
    path('students/<int:pk>/', StudentRetrieveUpdateDestroyAPIView.as_view(), name='student-detail'),
    path('students/<int:student_id>/attendance/', StudentAttendanceListView.as_view(), name='student-attendance'),

    path('users/create/user/', UserCreateView.as_view(), name='create-user'),
    path("users/create/superuser/", CreateSuperUserView.as_view(), name="create-superuser"),
    path('users/student-groups/<int:student_id>/', StudentGroupsView.as_view(), name='student-groups'),
    path('users/student/user/', StudentCreateAPIView.as_view(), name='student-userlari'),

    path('teachers/<int:teacher_id>/groups/', teacher_group_list, name='teacher-group-list'),

    # path('create/student/', StudentCreateAPIView.as_view(), name='create-student'),
    path("auth/login/", LoginAPIView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/me/", CurrentUserView.as_view(), name="me"),
    
    path('students-statistic/', StudentFilterView.as_view(), name='recent-students'),
     
    path('api/token/', TokenObtainSlidingView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshSlidingView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('populate-mock-data/', PopulateMockDataView.as_view(), name='populate-mock-data'),

    path('auth/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('auth/reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
    path('auth/verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('auth/set-new-password/', SetNewPasswordAPIView.as_view(), name='set-new-password'),
    path('auth/token/refresh/', CustomTokenRefreshView.as_view(), name='token-refresh'),
    
    path('', include(router.urls)),
]