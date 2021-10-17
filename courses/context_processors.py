from django.utils.translation import get_language
import random
from .models import *


def menu_links(request):
    # catg = Category.objects.all().exclude(parent=None).order_by('-created_at')[:7]
    # links = Category.objects.filter(parent=None)
    footcategories = Category.objects.filter(parent=None)[:4]
    catg_parent = Category.objects.filter(parent=None)
    # latest_catg = Category.objects.order_by("-id")[3:10]
    return dict(footcategories=footcategories, catg_parent=catg_parent, links={})

def home_page(request):
    headerImg = HeaderImg.objects.order_by('?').first()
    testimonials = Testimonial.objects.all()[:3]
    toBeApproved = Course.objects.filter(approved=False)
    return dict(testimonials=testimonials,headerImg=headerImg,toBeApproved=toBeApproved)

# def cart_total(request):
#     if request.user.is_authenticated:
#         totalcarts = Cart.objects.filter(user=request.user, purchase=False)
#         return dict(totalcarts=totalcarts)
#     else:
#         totalcarts=[]
#         return totalcarts