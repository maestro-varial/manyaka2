from django.shortcuts import render
from django.views.generic import View
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.models import User
import datetime

from courses.models import Reviews

# Create your views here.
week =  604800
month = 2629743
year = 31557600

class DashboardView(View):
    def get(self,request):
        if not request.user.profile.role == "t":
            return HttpResponseRedirect(reverse('courses:HomeView'))

        profile = request.user.profile
        vendor = request.user.vendor

        data=[]
        labels=[]
        for course_data in vendor.get_enrolled_courses():
            print(course_data)
            data.append(course_data['enrolls'])
            labels.append(course_data['course'].title)

        courses_data={
            'labels': labels,
            'data': data,
            'form_type': 'bar'
            }
        
        
        action = 2629743

        data=[]
        labels=[]
        timenow = datetime.datetime.now()
        current = 0
        previous = 0
        two_before = 0

        for order_item in vendor.get_withdrawn_orders():
            difference =  timenow.timestamp() - order_item.withdrawn_at.timestamp()
            print(order_item.get_total)
            if difference <= action:
                current += order_item.get_total
            elif difference >= action and difference <= action*2:
                previous += order_item.get_total
            elif difference >= action*2 and difference <= action*3:
                two_before += order_item.get_total
        data = [two_before,previous,current]
        labels.append(f'Two months Before')
        labels.append(f'Previous month')
        labels.append(f'Current month')
        earnings_data={
            'labels': labels,
            'data': data,
            'form_type': 'line'
            }
        
        recent_reviews = Reviews.objects.filter(referring_course__author = profile)[:5]

        context = {"vendor": vendor,"courses_data": courses_data, "earnings_data": earnings_data, "recent_reviews": recent_reviews}

        return render(request, 'dashboard/index.html', context)