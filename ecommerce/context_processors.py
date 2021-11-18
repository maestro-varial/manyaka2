import json
from .payment_apis import get_fees

def get_payment_methods(request):
    fees = {}
    try:
        fees = get_fees(50)
    except:
        pass
    data = {}
    data = json.loads(fees).get("data", None)
    
    return {"paymentMethods": data}