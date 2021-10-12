from rest_framework import permissions
from courses.models import Course, video
import json

class hasEnrolled(permissions.BasePermission):
    """
    Global permission check for enrolled course. If enrolled then return true.
    """

    def has_permission(self, request, view):
        video_id = request.GET.get('video_id', None)
        course_id = request.POST.get('course_id', None)
        enrolled_courses = request.user.profile.enrolled.all()
        course = None
        if video_id:
            video_obj = video.objects.get(id=video_id)
            if video_obj.is_preview:
                return True
            course = video_obj.course
        elif course_id:
            course = Course.objects.get(id=course_id)
        else:
            return False
        allowed = None
        if course in enrolled_courses:
            allowed = True
        else:
            allowed = False
        return allowed



class IsTeacher(permissions.BasePermission):
    """
    Global permission check for Teacher verification. If profile.role = t then return true.
    """

    def has_permission(self, request, view):
        if request.user.profile.role == 't':
            return True
        return False