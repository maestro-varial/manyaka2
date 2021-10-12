from django.urls import path
from . import views

app_name = "ecommerce"

urlpatterns = [
    path('', views.CartView, name="CartView"),
    path('checkout/', views.CheckoutView, name="CheckoutView"),
    path('api/update/', views.UpdateItemAPI.as_view(), name="UpdateItemAPI"),
    path('api/apply_coupon/', views.AddCouponAPI.as_view(), name="AddCouponAPI"),
    path('api/pay/', views.ProceedCheckoutAPI.as_view(), name="ProceedCheckoutAPI"),
]