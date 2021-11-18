# from store.models import Product
# from reports.utils import get_client_ip
# from django.db import models
# from django.contrib.auth.models import User
# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType
# from .signals import object_viewed_signal
# from django.contrib.sessions.models import Session

# # Create your models here.

# class ObjectViewed(models.Model):
#   user = models.ForeignKey(User,blank=True,null=True,on_delete=models.DO_NOTHING)
#   ip_address = models.CharField(max_length=220,blank=True,null=True)
#   product = models.ForeignKey(Product,on_delete=models.DO_NOTHING,default=None,null=True)
#   timestamp = models.DateTimeField(auto_now_add=True)

#   def __str__(self):
#     return f"{self.product} viewed on {self.timestamp}"

#   class Meta:
#     ordering = ['-timestamp']
#     verbose_name = 'Object Viewed'
#     verbose_name_plural = 'Objects Viewed'

# def object_viewed_reciever(sender,instance,request,*args, **kwargs):
#   # c_type = ContentType.objects.get_for_model(sender)
#   user = None
#   if request.user.is_authenticated:
#     user = request.user
#   new_obj_view = ObjectViewed.objects.create(
#     user = user,
#     ip_address = get_client_ip(request),
#     # object_id = instance.id,
#     # content_type = c_type
#     product = instance
#   )

# object_viewed_signal.connect(object_viewed_reciever)
