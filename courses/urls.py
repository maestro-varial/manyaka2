from django.urls import path
from . import views

app_name = "courses"

urlpatterns = [
    path('', views.HomeView, name="HomeView"),
    path('courses/', views.AllCoursesView, name="AllCoursesView"),
    path('course/', views.SearchView, name="SearchView"),
    path('course/create/', views.CreateCourseView.as_view(), name="CreateCourseView"),
    path('cat/<slug:slug>/', views.CategoryView, name="CategoryView"),
    path('course/<slug:slug>/', views.CourseDetailView, name="CourseDetailView"),
    path('course/enroll/<slug:slug>/', views.CourseEnrollView, name="CourseEnrollView"),
    path('course/mcq/', views.ManageMCQView.as_view(), name="ManageMCQView"),
    # path('courses/enrolled/', views.EnrolledCoursesView, name="EnrolledCoursesView"),

    # --APIS--
    path('api/course/create/', views.CreateCourseAPI.as_view(), name="CreateCourseAPI"),
    path('api/search/', views.SearchViewApi.as_view(), name="SearchViewApi"),
    path('api/enrolled/', views.GetEnrolledCoursesAPI.as_view(), name="GetEnrolledCoursesAPI"),
    path('api/get_video_api/', views.GetVideoAPI.as_view(), name="GetVideoAPI"),
    path('api/mark_course_complete/', views.MarkCourseComplete.as_view(), name="MarkCourseComplete"),
    path('api/review_submit/', views.ReviewViewAPI.as_view(), name="ReviewViewAPI"),
    path('cert/', views.GenerateCertificateView.as_view(), name="GenerateCertificateView"),
]
