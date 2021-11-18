import http.client
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_text, force_bytes
import base64
import requests
import json
import uuid

MERCHANDKEY = 'PHARMONY1'
SUBSCRIPTION_KEY = 'PH4NXZA9UXXXY1'
APPLICATION_CODE = 'AP4NXZA9UXXXGV5TN'
BASE_URL = "https://twsv03.adwapay.cm"

def get_token():

    url = f"{BASE_URL}/getADPToken"
    key = f"{MERCHANDKEY}:{SUBSCRIPTION_KEY}"
    key_bytes = key.encode('ascii')
    base64_bytes = base64.b64encode(key_bytes)
    base64_message = base64_bytes.decode('ascii')

    auth_key = f'Basic {base64_message}'

    payload = {"application": APPLICATION_CODE}

    headers = {
        'Authorization': auth_key,
        'Content-Type': 'text/plain'
    }

    response = requests.post(url, headers=headers, json=payload)
    res = response.json()
    res_data = res.get("data", None)
    if res_data:
        return res_data.get('tokenCode', None)
    return None



def get_fees(amount):
    url = f"{BASE_URL}/getFees"

    payload = {
        "amount": amount,
        "currency": "XAF"
    }

    headers = {
    'AUTH-API-TOKEN': f"Bearer {get_token()}",
    'AUTH-API-SUBSCRIPTION': f'{SUBSCRIPTION_KEY}',
    'Content-Type': 'text/plain'
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.content


def request_to_pay(payment_number, payment_method, order):
    amount = order.get_cart_total

    fees = get_fees(amount)
    data = {}
    try:
        data = json.loads(fees).get("data", None)
    except:
        pass

    for method in data:
        if method["meanCode"] == payment_method:
            data = method

    url = f"{BASE_URL}/requestToPay"

    order_number = f"{uuid.uuid1()}"

    payload = {
        "meanCode": data.get("meanCode", None),
        "paymentNumber": payment_number,
        "orderNumber": order_number,
        "amount": amount,
        "currency": data.get("currency", None),
        "feesAmount": data.get("feesAmount", None)
    }
    print(
        payload
    )
    # payload = {
    #     "meanCode": "MOBILE-MONEY",
    #     "paymentNumber": "650668282",
    #     "orderNumber": "DSJGDGDF.36834476466D",
    #     "amount": "1500",
    #     "currency": "XAF",
    #     "feesAmount": "200"
    # }

    headers = {
        'AUTH-API-TOKEN': f"Bearer {get_token()}",
        'AUTH-API-SUBSCRIPTION': f'{SUBSCRIPTION_KEY}',
        'Content-Type': 'text/plain'
    }
    print(headers)
    response = requests.post(url, headers=headers, json=payload)
    res = json.loads(response.content)
    print(
    res,
    res.get('data', None)
    )
    if not res.get('data', None):
        return {}
    return res








def disburse_payment(payment_number, payment_method, amount, order):
    amount = 1000
    order_number = order.transaction_id
    fees = get_fees(amount)
    data = {}
    try:
        data = json.loads(fees).get("data", None)
    except:
        pass

    for method in data:
        if method["meanCode"] == payment_method:
            data = method

    url = f"{BASE_URL}/requestToDisburse"
    # order_number = f"{urlsafe_base64_encode(force_bytes(vendor.user.username))}-{urlsafe_base64_encode(force_bytes(amount))}"
    payload = {
        "meanCode": data.get("meanCode", None),
        "paymentNumber": payment_number,
        "orderNumber": order_number,
        "amount": amount,
        "currency": data.get("currency", None),
        "feesAmount": data.get("feesAmount", None)
    }
    print(data.get("feesAmount", None))

    # payload = {
    #     "meanCode": "ORANGE-MONEY",
    #     "paymentNumber": "656155971",
    #     "orderNumber": "DSJGDGDFFEFYTUFUUTYFU5",
    #     "amount": 50,
    #     "currency": "XAF",
    #     "feesAmount": "100"
    # }
    
    # payload = {
    #     "meanCode": "MOBILE-MONEY",
    #     "paymentNumber": "650668282",
    #     "orderNumber": "DSJGDGDF.36834476466D",
    #     "amount": "1500",
    #     "currency": "XAF",
    #     "feesAmount": "200"
    # }

    headers = {
        'AUTH-API-TOKEN': f"Bearer {get_token()}",
        'AUTH-API-SUBSCRIPTION': f'{SUBSCRIPTION_KEY}',
        'Content-Type': 'text/plain'
    }
    print(headers)

    response = requests.post(url, headers=headers, json=payload)
    res = json.loads(response.content)
    print(res)
    if not res.get('data', None):
        return {}
    return res





# class ProceedCheckoutAPI(APIView):
#     permission_classes = (IsAuthenticated,)
#     def post(self,request):
#         user = request.user
#         orderItems = OrderItem.objects.filter(referring_course__author=user.profile, vendor_paid= False)

#         amount = 0
#         vendor = None

#         for item in orderItems:
#             amount += item.get_total
#             vendor = item.get_vendor

#         # TODO: Do payment process here
#         payment_method = request.POST.get('paymentMethod', None)
#         payment_number = request.POST.get('payment-number', None)

#         api_response = request_to_pay(payment_number, payment_method, round(amount, 2), vendor)

#         payment_data = api_response.get("data", None)
#         payment_data.get("adpFootprint", None)
#         payment_data.get("orderNumber", None)
#         # {'pesake': {'code': '', 'level': 0, 'detail': None}, 'data': {'adpFootprint': 'PHARMONY1____DQ52HK1B', 'orderNumber': 'Mw', 'status': 'E', 'description': None}}


#         # messages.success(request, "Payment Succeeded!")


#         # for item in order.items.all():
#         #     user.profile.enrolled.add(item.referring_course)

#         # order.complete = True
#         # order.save()

#         return Response(status=status.HTTP_200_OK)