import datetime
from django.db import models
from django.contrib.auth.models import User
from parler.models import TranslatedFields, TranslatableModel
from courses.models import Course

# Create your models here.

class Promocode(models.Model):
    
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    amount = models.FloatField()
    active = models.BooleanField()


    def __str__(self):
        return f"{self.code} ({self.amount}$)"



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    coupon = models.ForeignKey(Promocode, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return str(self.id)

    @property
    def coupon_valid(self):
        current_timestamp = datetime.datetime.now().timestamp()
        if self.coupon:
            if self.coupon.valid_from.timestamp() < current_timestamp and self.coupon.valid_to.timestamp() > current_timestamp and self.coupon.active:
                return True
        return False

    @property
    def get_cart_total(self):
        super()
        orderitems = self.items.all()
        total = sum([item.get_total for item in orderitems])
        if self.coupon_valid:
            total = total - self.coupon.amount
        return total

    @property
    def get_cart_items(self):
        total = 0
        orderitems = self.items.all()
        if self.complete == False:
            total = orderitems.count()
        return total


class OrderItem(models.Model):
        
    referring_course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name="items")
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = 0
        if self.referring_course:
            total = self.referring_course.get_price()
        return total

