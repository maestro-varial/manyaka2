from datetime import datetime
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.template.loader import render_to_string
from django.template import RequestContext
from django.middleware import csrf
from ecommerce.context_processors import get_payment_methods
from ecommerce.payment_apis import disburse_payment, get_fees, get_token

from vendor.models import Vendor
# Create your views here.

class VendorViewAPI(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        # get_token()
        # res = get_fees()
        user_id = request.GET.get("id", None)
        if not user_id:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user = get_object_or_404(User, id=user_id)
        paymentMethod =  get_payment_methods(request)
        context = {'user': user, 'csrf_value': csrf.get_token(request), "paymentMethods": paymentMethod.get("paymentMethods",None)}
        res = render_to_string('template-parts/vendor-items.html', context)
        if not res.strip():
            Response(status=status.HTTP_204_NO_CONTENT)
        return Response(res.strip(), status=status.HTTP_202_ACCEPTED)

    def post(self, request):
        vendor_id = request.POST.get("vendor_id", None)
        vendor = get_object_or_404(Vendor, id=vendor_id)

        payment_method = request.POST.get("paymentMethod", None)
        payment_number = request.POST.get("payment-number", None)
        amount = vendor.get_funds()
        pending_order_items = vendor.get_pending_orders()

        res = disburse_payment(payment_number, payment_method, amount, pending_order_items[0].order)
        print(res)

        # for order_item in vendor.get_pending_orders():
        #     order_item.vendor_paid = True
        #     order_item.withdrawn_at = datetime.now()
        #     order_item.save()
        return Response(status=status.HTTP_202_ACCEPTED)



class WithdrawnViewAPI(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        user_id = request.GET.get("id", None)
        if not user_id:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        user = get_object_or_404(User, id=user_id)
        context = {'user': user, 'csrf_value': csrf.get_token(request)}
        
        res = render_to_string('template-parts/withdrawn-items.html', context)
        if not res.strip():
            Response(status=status.HTTP_204_NO_CONTENT)
        return Response(res.strip(), status=status.HTTP_202_ACCEPTED)
