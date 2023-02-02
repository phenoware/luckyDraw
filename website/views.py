from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.db.models import Count, F, Value, Q
from django.db.models.functions import Length, Upper
import datetime
from django.contrib.auth import logout  
from dashboard.models import APKFile
from django.conf import settings
from django.core.mail import send_mail
from dashboard.models import Market, JodiMarket, Games, Customer, BiddingHistory, JodiBiddingHistory, Withdraw, Transaction, Notifications,BankAccount, Partner, PartnerUser, PartnerWithdraw, PanelChartRegulerMarket , PanelChartJodiMarket, UserRoll, Card, Product

from django.contrib.auth import logout  
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template.context_processors import csrf

import random
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template.context_processors import csrf
import hashlib
from django.template.loader import get_template
from django.template import Context, Template,RequestContext
from django.conf import settings
from django.core.mail import send_mail
from pattiMallProj import Checksum
import random
import requests
import json
# import PaytmChecksum
import datetime

# Live Mode
PAYTM_MID = "wdRVdJ51632956452397"
PAYTM_MERCHANT_KEY = "jJ819wGiAlcp1eH0"
PAYTM_ENVIRONMENT= 'https://securegw.paytm.in'
PAYTM_WEBSITE= 'DEFAULT'

# test mode 
# PAYTM_MID = "POoumm70492980245805"
# PAYTM_MERCHANT_KEY = "jcoNsN&V7gch3G&j"
# PAYTM_ENVIRONMENT= 'https://securegw-stage.paytm.in'
# PAYTM_WEBSITE= 'WEBSTAGING'


# Email Templates.

def emailTemplate(request):
    return render(request, "app/new-account-mail.html")

# Paytm Payment gateway Integration

def paytmweb(request):

    if 'name' not in request.session:
        request.session['name'] = request.POST['name']
        request.session['email'] = request.POST['email']
        request.session['phone'] = request.POST['phone']
        request.session['city'] = request.POST['city']
        request.session['address'] = request.POST['address']
        request.session['qnt'] = request.POST['qnt']
        request.session['msg'] = request.POST['msg']
    else:

        # Delete Old Session 
        del request.session['name']
        del request.session['email']
        del request.session['phone']
        del request.session['city']
        del request.session['address']
        del request.session['qnt']
        del request.session['msg']
        del request.session["amount"]
        del request.session["productName"]

        # Set New Session 
        request.session['name'] = request.POST['name']
        request.session['email'] = request.POST['email']
        request.session['phone'] = request.POST['phone']
        request.session['city'] = request.POST['city']
        request.session['address'] = request.POST['address']
        request.session['qnt'] = request.POST['qnt']
        request.session['msg'] = request.POST['msg']



    if request.POST['product'] == '0':
        return HttpResponse("Please select product")
    else :
        product = Product.objects.get(id  = request.POST['product'])
        qnt = int(request.POST['qnt'])
        amount= str(product.price) * qnt
        productName = product.name
    
    # amount = 1
    print('amount is :'+str(amount) )
    request.session["amount"] = amount
    request.session["productName"] = productName


    
    # Payment gateway integration 
    order_id='order_'+str(datetime.datetime.now().timestamp())
    custId = request.POST['email']
    paytmParams = dict() 
    paytmParams["body"] = {
        "requestType"   : "Payment",
        "mid"           : PAYTM_MID,
        "websiteName"   : PAYTM_WEBSITE,
        "orderId"       : order_id,
        "callbackUrl"   : "http://127.0.0.1:8000/handlerequestweb/",
        "txnAmount"     : {
            "value"     : str(amount),
            "currency"  : "INR",
        },
        "userInfo"      : {
            "custId"    : custId,
        },
    }

    # Generate checksum by parameters we have in body
    # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys 
    checksum = Checksum.generateSignature(json.dumps(paytmParams["body"]), PAYTM_MERCHANT_KEY)

    paytmParams["head"] = {
        "signature"    : checksum
    }

    post_data = json.dumps(paytmParams)

    url = PAYTM_ENVIRONMENT+"/theia/api/v1/initiateTransaction?mid="+PAYTM_MID+"&orderId="+order_id

    response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
    response_str = json.dumps(response)
    res = json.loads(response_str)
    if res["body"]["resultInfo"]["resultStatus"]=='S':
        token=res["body"]["txnToken"]
    else:
        token=""

    dataParams = {'mid':PAYTM_MID, 'amount':str(amount), 'orderid':order_id, 'env':PAYTM_ENVIRONMENT, 'token':token}
    return render(request, 'website/index1.html', dataParams)



@csrf_exempt
def handlerequestweb(request):

    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]


    verify = Checksum.verifySignature(response_dict, PAYTM_MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            transaction_id = response_dict['BANKTXNID']
            
            print('order successful')
            return redirect('/payment-success-web/'+transaction_id)
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'website/paymentstatus.html', {'response': response_dict})


def paymentSuccessWeb(request,successPaymentId):
    # Get Seesion data 
    name = request.session.get('name')
    email = request.session.get('email')
    phone = request.session.get('phone')
    city = request.session.get('city')
    address = request.session.get('address')
    qnt = request.session.get('qnt')
    msg = request.session.get('msg')
    amount = request.session.get('amount')
    productName = request.session.get('productName')
    
    

    # Mail For Admin
    subject = 'New order from Lucky Draw Card website'
    message = f'Dear Sir,\n\nYou have received new order from website as below \nCustomer name : '+name+' ,\nPhone : '+phone+' ,\nAddress : '+address+' ,\nCity : '+city+' ,\nProduct name : '+productName+' ,\nQauntity : '+str(qnt)+',\n\n'+msg
        
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['52pattimall@gmail.com']
    send_mail( subject, message, email_from, recipient_list )
    

    # Mail for customer 
    subject = 'Order placed successfully - Lucky Draw Card'
    message = f'Dear Sir,\nCongratilations,  \n\nYour order placed successfully , We will contact you shortly.\nProducts Name :'+productName+',\nQauntity : '+str(qnt)+'\n\nThanking you\nTeam 52 Patti Mall'
        
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail( subject, message, email_from, recipient_list )

    # Delete Old Sessop 
    del request.session['name']
    del request.session['email']
    del request.session['phone']
    del request.session['city']
    del request.session['address']
    del request.session['qnt']
    del request.session['msg']
    del request.session["amount"]
    del request.session["productName"]
    return render(request, 'website/order-success.html')
    

def home(request):
    app = APKFile.objects.filter(id =1)
    products = Product.objects.all().order_by('-id')

    params = {'app': app, 'products':products}
    return render(request, 'website/index.html', params)


def aboutUs(request):
    app = APKFile.objects.filter(id =1)
    params = {'app': app}
    return render(request,'website/about-us.html',params)

def termServices(request):
    app = APKFile.objects.filter(id =1)
    params = {'app': app}
    return render(request,'website/term.html',params)

def refundPolicy(request):
    app = APKFile.objects.filter(id =1)
    params = {'app': app}
    return render(request,'website/refund.html',params)

def privacyPolicy(request):
    app = APKFile.objects.filter(id =1)
    params = {'app': app}
    return render(request,'website/privacy.html',params)


def uploadApk(request):
    return render(request, 'website/upload-apk.html')

def makeUpload(request):
    apk = request.FILES['file']
    date = datetime.datetime.now()
    newApk = APKFile(apk = apk, date= date)
    newApk.save()
    return redirect('/')

def placeOrder(request):
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    city = request.POST['city']
    address = request.POST['address']
    product = request.POST['product']
    qnt = request.POST['qnt']
    msg = request.POST['msg']

    # Mail for admin 
    subject = 'New order from 52 Patti Mall website'
    message = f'Dear Sir,\n\nYou have received new order from website as below \nCustomer name : '+name+' ,\nPhone : '+phone+' ,\nAddress : '+address+' ,\nCity : '+city+' ,\nProduct name : '+product+' ,\nQauntity : '+str(qnt)+',\n\n'+msg
        
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['inwmarathi@gmail.com']
    send_mail( subject, message, email_from, recipient_list )
    

    # Mail for customer 
    subject = 'Order placed successfully - 52 Patti Mall'
    message = f'Dear Sir,\nCongratilations,  \n\nYour order placed successfully , We will contact you shortly.\n\nThanking you\nTeam 52 Patti Mall'
        
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail( subject, message, email_from, recipient_list )
    return render(request, 'website/order-success.html')

def resultPanel(request):
    markets = Market.objects.all()
    params = {'markets': markets }
    return render(request, 'website/result-panel.html', params)


def resultPanelChart(request, id):
    market = Market.objects.get(id= id)
    marketName = market.title
    chart = PanelChartRegulerMarket.objects.filter(market_id = id)
    params = {'chart': chart, 'marketName':marketName }
    return render(request, 'website/result-panel-chart.html', params)