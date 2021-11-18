from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from parler.models import TranslatedFields, TranslatableModel


# Create your models here.

ROLES = (
    ('st','Student'),
    ('t','Teacher'),
)
class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    profile_pic = models.ImageField(upload_to="profile_pics/", default="main/default.jpg", null=True, blank=True)
    phone = models.CharField(max_length=25)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    role = models.CharField(choices=ROLES, max_length=3, null=False, default='st')
    enrolled = models.ManyToManyField("courses.Course", blank=True, related_name="users")
    finished = models.ManyToManyField("courses.Course", blank=True, related_name="users_finished")

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"

    def __str__(self):
        return self.user.username

    # def get_pending_orders(self):
    #     return self.user.orders



@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()