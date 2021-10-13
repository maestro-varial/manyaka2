from django import template
from courses.models import *

register = template.Library()

@register.filter(name='get_video')
def get_video(value,c_id):
    course = Course.objects.get(id=c_id)
    curriculams = course.curriculams.all()
    i=0
    v_index = 0
    video = None
    while i < value:
        if curriculams[i].video:
            v_index+=1
        i+=1
    try:
        video = course.videos.all()[v_index-1]
    except:
        pass
    return video

@register.filter(name='enroll_contains')
def enroll_contains(value,c_id):
    course = Course.objects.get(id=c_id)
    enrolled_courses = value
    if not enrolled_courses:
        return False

    allowed = None
    if course in enrolled_courses:
        allowed = True
    else:
        allowed = False
    return allowed

# @register.filter(name='course_finished')
# def course_finished(value,c_id):
#     course = Course.objects.get(id=c_id)
#     enrolled_courses = value
#     if not enrolled_courses:
#         return False

#     allowed = None
#     if course in enrolled_courses:
#         allowed = True
#     else:
#         allowed = False
#     return allowed

@register.filter(name='mcqs_passed')
def mcqs_passed(value,c_id):
    # value is the user here
    course = Course.objects.get(id=c_id)
    for mcq in course.mcqs.all():
        if not value.profile in mcq.completed.all():
            return False
    return True

@register.filter(name='mcq_completed')
def mcq_completed(value,mcq_id):
    # value is the user here
    mcq = MCQ.objects.get(id=mcq_id)
    if value.profile in mcq.completed.all():
        return True
    return False