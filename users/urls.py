from django.urls import path
from . import views


app_name = "users"

urlpatterns = [
    path('signup/', views.signup_view, name="signup_view"),
    path('login/', views.login_view, name="login_view"),
    path('logout/', views.logout_view, name="logout_view"),
    path('settings/', views.SettingsView, name="SettingsView"),
    # path('edit_profile/', views.EditProfileView, name="EditProfileView"),
    path('api/edit_profile/', views.EditProfileAPI.as_view(), name="EditProfileAPI"),
    path('dashboard/teacher/', views.TeacherAreaView, name="TeacherAreaView"),
    path('dashboard/mycourses/', views.MyCourses.as_view(), name="MyCourses"),
    path('dashboard/mystudents/', views.MyStudents.as_view(), name="MyStudents"),
]
