from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.shortcuts import render, HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse

from courses.models import Course
from .forms import ProfileUpdateForm, SignUpForm, UpdateProfileForm, UpdateUserForm
from .models import Profile
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        profile_form = ProfileUpdateForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            
            profile_form = ProfileUpdateForm(request.POST,request.FILES,instance=user.profile)
            if profile_form.is_valid():
                print('valid')
                profile_form.save()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            messages.success(request, 'Profile Created Successfully.')
            return HttpResponseRedirect(reverse('courses:HomeView'))
        return render(request, 'auth/signup.html', {'form': form, 'profile_form': profile_form})
    else:
        form = SignUpForm()
        profile_form = ProfileUpdateForm()
        return render(request, 'auth/signup.html', {'form': form, 'profile_form': profile_form})


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('courses:HomeView'))

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username,password = password)
            if user is not None:
                login(request,user)
                messages.success(request, 'Logged In Successfully.')
                return HttpResponseRedirect(reverse('courses:HomeView'))
        return render(request,'auth/login.html',{'form' : form})
    form = AuthenticationForm()
    return render(request,'auth/login.html',{'form' : form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('courses:HomeView'))


class EditProfileAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        res = render_to_string('template-parts/profile-edit-form.html', context)
        if not res.strip():
            Response(status=status.HTTP_204_NO_CONTENT)
        return Response(json.dumps(res.strip()),status=status.HTTP_202_ACCEPTED)

    def post(self, request):
        print('post!!!')
        user_form = UpdateUserForm(request.POST or None, instance=request.user)
        profile_form = UpdateProfileForm(request.POST or None, request.FILES or None, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, 'Your profile was successfully updated!')
            # return reverse(request, 'users:profile')
        else:
            # print(user_form)
            messages.error(request, 'Please correct the error below.')

        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        res = render_to_string('template-parts/profile-edit-form.html', context)
        if not res.strip():
            Response(status=status.HTTP_204_NO_CONTENT)
        return Response(json.dumps(res.strip()),status=status.HTTP_202_ACCEPTED)



# def EditProfileView(request): 
#     if request.method == 'POST':
#         user_form = SignUpForm(request.POST or None, request.FILES or None, instance=request.user)
#         profile_form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=request.user.profile)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, 'Your profile was successfully updated!')
#             # return reverse(request, 'users:profile')
#         else:
#             # print(user_form)
#             messages.error(request, 'Please correct the error below.')
#     else:
#         user_form = SignUpForm(instance=request.user)
#         profile_form = ProfileUpdateForm(instance=request.user.profile)
#     return render(request, 'auth/auth-settings.html', {
#         'user_form': user_form,
#         'profile_form': profile_form
#     })


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            # return reverse('userhome')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/edit_password.html', {
        'form': form
    })


def TeacherAreaView(request):
    return render(request,"courses/teacher-area.html")

def SettingsView(request):
    return render(request,"template-parts/base-settings.html")


class MyCourses(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        courses = Course.objects.filter(author=request.user.profile)
        context = {
            'courses': courses
        }
        res = render_to_string('template-parts/my-courses.html', context)
        if not res.strip():
            Response(status=status.HTTP_204_NO_CONTENT)
        return Response(json.dumps(res.strip()),status=status.HTTP_202_ACCEPTED)


class MyStudents(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        students = []
        courses = Course.objects.filter(author=request.user.profile)
        for course in courses:
            students.append(course.users.all())
        print(students)
        context = {
            'students': students
        }
        res = render_to_string('template-parts/my-students.html', context)
        if not res.strip():
            Response(status=status.HTTP_204_NO_CONTENT)
        return Response(json.dumps(res.strip()),status=status.HTTP_202_ACCEPTED)

