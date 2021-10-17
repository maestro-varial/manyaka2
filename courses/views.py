import json
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404, HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render,get_object_or_404, HttpResponseRedirect
from django.template.loader import get_template, render_to_string
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic.base import View
from django.utils.translation import get_language
from django.views.generic.detail import DetailView
from parler.views import TranslatableSlugMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from courses.utils import render_to_pdf
from courses.serializers import CourseSerializer
from ecommerce.models import Order, OrderItem
from courses.custom_perms import IsTeacher, hasEnrolled
from .models import Category, Course, Reviews, video
from .forms import *


# Create your views here.
# messages.success(request, 'Profile details updated.')
# messages.info(request, 'info should be.')
# messages.warning(request, 'warning is it.')
# messages.error(request, 'Error is this')

def HomeView(request):
    courses = Course.objects.filter(approved=True).order_by('-id')[:15]
    context = {'courses': courses}
    return render(request,"courses/home.html", context)

def AllCoursesView(request):
    courses = Course.objects.filter(approved=True)
    context = {'courses': courses}
    return render(request,"courses/list_courses.html", context)

# @login_required
# def EnrolledCoursesView(request):
#     courses = request.user.profile.enrolled.all()
#     context = {'courses': courses}
#     return render(request,"courses/enrolled-courses.html", context)

def CategoryView(request, slug):
    category = Category.objects.get(translations__slug = slug,approved=True)
    courses = category.courses.all()
    context = {'courses': courses, 'category': category}
    return render(request,"courses/list_courses.html", context)


def ApproveCourses(request):
    if request.method == "GET":
        if request.user.is_staff:
            return render(request,"courses/approve_courses.html")
        return HttpResponse(status=404)

class ChangeApproved(View):
    def post(self,request):
        if request.user.is_staff:
            course_id = request.POST.get('course_id')
            course = get_object_or_404(Course, id = course_id)
            course.approved = True
            course.save()
            return HttpResponse(status=200)
        return HttpResponse(status=403)

def CourseDetailView(request, slug):
    # course = Course.objects.get(translations__slug=slug)
    course = get_object_or_404(Course, translations__slug = slug)
    context = {'course': course}
    if course.approved:
        return render(request,"courses/detail_course.html", context)
    elif request.user.is_staff:
        return render(request,"courses/detail_course.html", context)
    return HttpResponse(status=404)

# class CourseDetailView(TranslatableSlugMixin, DetailView):
#     model = Course
#     template_name = 'courses/detail_course.html'

@login_required
def CourseEnrollView(request, slug):
    course = Course.objects.get(translations__slug = slug)
    if request.user.is_authenticated:
        if course in request.user.profile.enrolled.all():
            context = {'course': course}
            return render(request,"courses/enroll_course.html", context)
        else:
            course = get_object_or_404(Course, translations__slug=slug)
            order, created = Order.objects.get_or_create(user = request.user, complete = False)
            orderItem, created = OrderItem.objects.get_or_create(order=order, referring_course=course)
            if created:
                orderItem.save()
            return HttpResponseRedirect(reverse('ecommerce:CartView'))
    return HttpResponseRedirect(reverse('users:signup_view'))

class GetVideoAPI(APIView):
    permission_classes = (IsAuthenticated, hasEnrolled)
    def get(self, request):
        video_id = request.GET['video_id']
        video_obj = video.objects.get(id=video_id)
        res = render_to_string('template-parts/embed-video.html', {'video':video_obj})
        if not res.strip():
            res = render_to_string('template-parts/embed-404.html')
        return Response(json.dumps(res.strip()),status=status.HTTP_202_ACCEPTED)


class GetEnrolledCoursesAPI(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        courses = request.user.profile.enrolled.all()
        context = {'courses': courses}
        res = render_to_string('template-parts/enrolled-courses.html', context)
        if not res.strip():
            Response(status=status.HTTP_204_NO_CONTENT)
        return Response(json.dumps(res.strip()),status=status.HTTP_202_ACCEPTED)


class MarkCourseComplete(APIView):
    permission_classes = (IsAuthenticated,hasEnrolled)
    def post(self, request):
        course_id = request.POST.get('course_id')
        is_checked = request.POST.get('isChecked')
        course = Course.objects.get(id=course_id)
        if str(is_checked) == 'true':
            request.user.profile.finished.add(course)
        else:
            request.user.profile.finished.remove(course)
        request.user.profile.save()
        return Response(status=status.HTTP_202_ACCEPTED)


class ReviewViewAPI(APIView):
    permission_classes = (IsAuthenticated,hasEnrolled)
    def post(self, request):
        course_id = request.POST.get('course_id')
        course = Course.objects.get(id=course_id)
        content = request.POST.get('content')
        stars = request.POST.get('stars')

        review,created = Reviews.objects.get_or_create(user=request.user, referring_course= course)
        review.content = content
        review.stars = stars
        review.save()
        return Response(status=status.HTTP_200_OK)


def SearchView(request):
    if request.method == "GET":
        search = request.GET['q']
        courses = Course.objects.filter(Q(translations__title__icontains=search) | Q(translations__meta_desc__icontains=search))
        context = {'courses':courses, 'search':search}
        return render(request, 'courses/search.html', context)


class SearchViewApi(APIView):
    def get(self,request):
        search = request.GET['q']
        courses = Course.objects.filter(Q(translations__title__icontains=search) | Q(translations__meta_desc__icontains=search))
        context = {'courses':courses, 'search':search}
        serializer = CourseSerializer(courses,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# TODO:
class CreateCourseAPI(APIView):
    permission_classes = (IsAuthenticated,IsTeacher)

    def post(self, request):
        form = CreateCourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Course was successfully Created!')
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            messages.error(request, 'Please correct the error below.')
        context = {
            'form': form,
        }
        return Response(context,status=status.HTTP_304_NOT_MODIFIED)


class CreateCourseView(View):
    def get(self, request):
        course_form = CreateCourseForm()
        curriculam_form = curriculam_formset()
        video_form = video_formset()
        features_form = features_formset()
        faq_form = faq_formset()
        mcq_form = mcq_formset()
        certificate_form = CertificateForm()

        context = {
            'course_form': course_form,
            'curriculam_form': curriculam_form,
            'video_form': video_form,
            'features_form': features_form,
            'faq_form': faq_form,
            'mcq_form': mcq_form,
            'certificate_form': certificate_form,
        }
        return render(request, 'courses/create-course-form.html', context)

    def post(self, request):
        course_form = CreateCourseForm(request.POST, request.FILES)
        curriculam_form = curriculam_formset(request.POST)
        video_form = video_formset(request.POST)
        features_form = features_formset(request.POST)
        faq_form = faq_formset(request.POST)
        mcq_form = mcq_formset(request.POST)
        certificate_form = CertificateForm(request.POST)

        context = {
            'course_form': course_form,
            'curriculam_form': curriculam_form,
            'video_form': video_form,
            'features_form': features_form,
            'faq_form': faq_form,
            'mcq_form': mcq_form,
            'certificate_form': certificate_form,
        }

        if course_form.is_valid() and curriculam_form.is_valid() and video_form.is_valid() and features_form.is_valid() and faq_form.is_valid() and mcq_form.is_valid():
            course = course_form.save(commit=False)
            course.author = request.user.profile
            course.save()

            for cat in course_form.cleaned_data['category']:
                course.category.add(cat)

            curriculams = curriculam_form.save(commit=False)
            for curriculam in curriculams:
                curriculam.course = course
                curriculam.save()

            videos = video_form.save(commit=False)
            for index, video in enumerate(videos):
                video.course = course
                video.serial_number = index
                video.save()

            features = features_form.save(commit=False)
            for feature in features:
                feature.course = course
                feature.save()

            faqs = faq_form.save(commit=False)
            for faq in faqs:
                faq.course = course
                faq.save()

            # options = [
            #     mcq_form.cleaned_data.get('option1'),
            #     mcq_form.cleaned_data.get('option2'),
            #     mcq_form.cleaned_data.get('option3'),
            # ]
            
            certificate = certificate_form.save(commit=False)
            certificate.course = course
            certificate.save()

            mcqs = mcq_form.save(commit=False)
            for index, mcq_data in enumerate(mcqs):
                mcq, option_instances = mcq_data
                mcq.serial_number = index+1
                mcq.course = course
                mcq.save()
                # option_instances = mcq.pre_save()
                for option in option_instances:
                    option.save()

            messages.success(request, 'Your Course was successfully Created!')
            return render(request, 'courses/create-course-form.html', context)
        else:
            messages.error(request, 'Please correct the error below.')
        return render(request, 'courses/create-course-form.html', context)


class ManageMCQView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        mcq_id = request.GET.get('mcq_id')
        mcq = MCQ.objects.get(id=mcq_id)
        context = {'mcq':mcq}
        res = render_to_string('template-parts/course-mcq.html',context)
        if not res.strip():
            Response(status=status.HTTP_204_NO_CONTENT)
        return Response(json.dumps(res.strip()),status=status.HTTP_202_ACCEPTED)

    def post(self, request, *args, **kwargs):
        mcq_id = request.POST.get('mcq_id')
        selected_option_id = request.POST.get('options')
        mcq = MCQ.objects.get(id=mcq_id)
        mcqOption = McqOption.objects.get(id=selected_option_id)
        if mcqOption in  mcq.options.all():
            if mcqOption.correct:
                mcq.completed.add(request.user.profile)
                mcq.save()
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


class GenerateCertificateView(View):
    def get(self, request, *args, **kwargs):
        course_slug = request.GET.get('course')
        # e.g: ?course=machine-learning&download=true
        course = get_object_or_404(Course, translations__slug=course_slug)
        context = {
            "name": request.user.first_name + ' ' + request.user.last_name,
            "course": course.title,
            "certificate": course.certificate,
        }
        pdf = render_to_pdf('template-parts/certificate.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Certificate_%s.pdf" %(course.title)
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download == 'true':
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
