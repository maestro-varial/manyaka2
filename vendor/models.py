from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from itertools import chain

from ecommerce.models import OrderItem

# Create your models here.


class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='vendor', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     ordering = ['name']

    def __str__(self):
        return f"Vendor: {self.user}"

    def get_paid_amount(self):
        total = 0
        courses = self.user.profile.courses.all()

        for course in courses:
            for order_item in course.order_items.filter(vendor_paid=True):
                total += order_item.get_total

        return total

    def get_pending_orders(self):
        order_items = []
        courses = self.user.profile.courses.all()

        for course in courses:
            for order_item in course.order_items.filter(vendor_paid=False).order_by("-id"):
                order_items.append(order_item)

        return order_items

    def get_withdrawn_orders(self):
        order_items = []
        courses = self.user.profile.courses.all()

        for course in courses:
            for order_item in course.order_items.filter(vendor_paid=True).order_by("-id"):
                order_items.append(order_item)

        return order_items

    def get_funds(self):
        total_funds = 0
        courses = self.user.profile.courses.all()

        for course in courses:
            for order_item in course.order_items.filter(vendor_paid=False):
                total_funds += order_item.get_total

        return round(total_funds, 2)

    def get_enrolled_courses(self):
        data = []
        courses = self.user.profile.courses.all()
        for course in courses:
            enrolls = OrderItem.objects.filter(
                referring_course=course,
                order__complete = True
            ).count()
            _data = {
                "course": course,
                "enrolls": enrolls
            }
            data.append(_data)

        return data

    def get_students(self):
        students = []
        courses = self.user.profile.courses.all()
        for course in courses:
            for profile in course.users.all():
                if not profile in students:
                    students.append(profile)
        return students



@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Vendor.objects.create(user=instance)
    instance.vendor.save()