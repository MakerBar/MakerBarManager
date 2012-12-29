from datetime import datetime

from MakerBarManager.SupplyRequest.models import Order_Request

from django.shortcuts import render_to_response

def order_request(request):
    requestor = 'eabraham'
    order_requests=Order_Request.objects.all()
    return render_to_response('index.html',{'order_requests':order_requests,'requestor':requestor})