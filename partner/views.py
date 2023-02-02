from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login,logout
from dashboard.models import Market, JodiMarket, Games, Customer, BiddingHistory, JodiBiddingHistory, Withdraw, Transaction, Notifications,BankAccount, Partner, PartnerUser, UserRoll, PartnerWithdraw
from django.contrib import messages
from django.db.models import Count, F, Value, Q
from django.db.models.functions import Length, Upper
import datetime
import http.client
import razorpay
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import logout 
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from pattiMallProj.decorators import check_broker_account
import random
from django.db.models import Sum
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.

# HTML Mail Requirement stuff
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
from django.template.loader import render_to_string 
from django.utils.html import strip_tags



# User Authentication Views
def partnerLogin(request):
    if request.user.is_authenticated:
        if Partner.objects.filter(user_id = request.user.id).exists():
                messages.success(request,'Login Suucessfull')
                return redirect('/partner')
        else:
            logout(request)
            messages.success(request, 'Yor are not authorised to access broker panel, Please contact with admin')
            return redirect('partnerLogin')     
    return render(request, 'partner/login.html')

def handleBrokerLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            
            if Partner.objects.filter(user_id = request.user.id).exists():
                messages.success(request,'Login Suucessfull')
                return redirect('/partner')
            else:
                logout(request)
                messages.success(request, 'Yor are not authorised to access broker panel, Please contact with admin')
                return redirect('partnerLogin')
            
        else:
            messages.success(request,'Invalid Credentials')
            return redirect('partnerLogin')
    return render(request, "dashboard/error.html")

def brokerLogout(request):
    logout(request)
    messages.success(request,'Logout')
    return redirect('partnerLogin')


@login_required(login_url = '/partner/partner-login')
@check_broker_account()
def home(request):
    partner = Partner.objects.get(user_id = request.user.id)
    userCount = PartnerUser.objects.filter(partner_id = partner.id).count()
    users = PartnerUser.objects.filter(partner_id = partner.id)
    brokerId = partner.id
    print(users)
    totalBiAmount = 0 
    totalJodiBiAmount = 0 
    for i in users:
        print(i.user.id)
        bidding = BiddingHistory.objects.filter(customer_id = i.user.id)
        for b in bidding:
            totalBiAmount = totalBiAmount + int(b.points)
            print(totalBiAmount)

        jodiBidding = JodiBiddingHistory.objects.filter(customer_id = i.user.id)
        for b in jodiBidding:
            totalJodiBiAmount = totalJodiBiAmount + int(b.points)
            print(totalJodiBiAmount) 


    # total bidding amount 
    partner.totalBiddingAmount =totalBiAmount + totalJodiBiAmount
    totalPaybleBidding = partner.payingBiddingAmount
    partner.save() 

    # Broker rearing 
    earingAmount = partner.earningAmount
    
    # wallet Balance 
    walletBalance = partner.walletAmount

    # todays bidding 
    dic1 ={}
    for i in users:
        id = i.user.id
        bidding = BiddingHistory.objects.filter(customer_id = id, date= datetime.datetime.now())
        for b in bidding:
            dic1[b.id] = {'customer':b.customer.user.first_name +"  "+ b.customer.user.last_name, 'market':b.market.title +" - "+b.marketType,'game': b.game.title, 'digit': b.digit, 'points':b.points, 'status':b.status, 'winAmount':b.winAmount, 'date':b.date }

    params = {'userCount':userCount, 'totalBiAmount':totalBiAmount + totalJodiBiAmount, 'totalPaybleBidding':totalPaybleBidding, 'earingAmount':earingAmount, 'walletBalance':walletBalance , 'history':dic1, 'brokerId':brokerId}
    return render(request, 'partner/index.html', params)



# Referal user management
@login_required(login_url = '/partner/partner-login')
@check_broker_account()
def users(request):
    partner = Partner.objects.get(user_id = request.user.id)
    users = PartnerUser.objects.filter(partner_id = partner.id)

    params = {'users': users}
    return render(request, 'partner/users.html', params)



@login_required(login_url = '/partner/partner-login')
@check_broker_account()
def addNewUser(request):
    # get user data 
    firstName = request.POST['firstName']
    lastName = request.POST['lastName']
    email = request.POST['email']
    phone = request.POST['phone']
    city = request.POST['city']
    
    broker = Partner.objects.get(user_id = request.user.id)

    # create password
    randomNumber = random.randint(0000, 9999)
    password = "qwer"+ str(randomNumber)
    print(password)
    # create user auth account 
    if User.objects.filter(username = email).exists():
        messages.warning(request, 'Email address already registerd with us, Please try with different email')
        return redirect('/partner/users')
    elif User.objects.filter(email = email).exists():
        messages.warning(request, 'Email address already registerd wtth us, Please try with different email')
        return redirect('/partner/users')
    else:    
        newUser= User.objects.create_user(password = password, email= email, first_name= firstName , last_name= lastName,username=email)
        newUser.save()
        user = User.objects.get(username = email)

        roll = UserRoll(user = user, roll = 'customer')
        roll.save()
        rollObj = UserRoll.objects.get(user_id = user)

        # Create Customer Account     
        newCustomer = Customer(phone= phone, status= 'Active', user= user , roll = rollObj, walletAmount= 0)
        newCustomer.save()

        # Create Notification 
        customer = Customer.objects.get(user = user)
        notification = Notifications(customer= customer, title= "New Account Created Successfully", msg= "New user account created recently", date = datetime.datetime.now(), status = 'Account Active')
        notification.save()

        # create bank account 
        bank = BankAccount(customer= customer)
        bank.save()
        
        # create boker reference account
        brokerUser = PartnerUser(partner= broker, user= customer)
        brokerUser.save()

        # send password mail to new user 
        subject = '52 Patti Mall - Wallet credited with Rs.1000'
        email_from = settings.EMAIL_HOST_USER
        
        
        html_content = render_to_string('app/new-account-mail.html', {'username':email, 'password':password })
        text_content = strip_tags(html_content)

        email_obj = EmailMultiAlternatives(subject, text_content, email_from, [email])
        email_obj.attach_alternative(html_content, "text/html")
        
        email_obj.send()

        messages.success(request, "New user created successfully.")
        return redirect('/partner/users')        
        
@login_required(login_url = '/partner/partner-login')
@check_broker_account()
def userDetails(request, id):
    customer = Customer.objects.filter(id = id)
    biddingHistory = BiddingHistory.objects.filter(customer_id = id)
    jodiBiddingHistory = JodiBiddingHistory.objects.filter(customer_id = id)
    biddingCount  = BiddingHistory.objects.filter(customer_id = id).count()
    jodiBiddingCount = JodiBiddingHistory.objects.filter(customer_id = id).count()
            

    BidtotalWin = 0 
    jodiTotalWin = 0 
    for i in biddingHistory:
        totalWin = i.winAmount

    for i in jodiBiddingHistory:
        i.winAmount

    totalWin = BidtotalWin + jodiTotalWin

    totalBidding = biddingCount + jodiBiddingCount
    withdraw = Withdraw.objects.filter(customer_id = id)
    transaction = Transaction.objects.filter(customer_id = id)
    bankAccount = BankAccount.objects.filter(customer_id = id)

    totalBiAmount = 0
    userBidding= BiddingHistory.objects.filter(customer_id = id)
    userJodiBidding = JodiBiddingHistory.objects.filter(customer_id = id)
    
    biddingSum = 0 
    jodiBiddingSum = 0 
    for i in userBidding:
        biddingSum = biddingSum + int(i.points)
        
    for i in userJodiBidding:
        jodiBiddingSum = jodiBiddingSum + int(i.points)

    totalBiAmount = biddingSum + jodiBiddingSum
    params = {'customer': customer, 'biddingHistory': biddingHistory, 'jodiBiddingHistory':jodiBiddingHistory,'withdraw':withdraw, 
    'transaction': transaction, 'bankAccount':bankAccount, 'totalBidding':totalBidding, 'totalWin':totalWin, 'totalBiAmount':totalBiAmount}
    return render(request, 'partner/user-details.html', params)

@login_required(login_url = '/partner/partner-login')
@check_broker_account()
def biddingHistory(request):
    partner = Partner.objects.get(user_id = request.user.id)
    users = PartnerUser.objects.filter(partner_id = partner.id)

    dic1 ={}
    for i in users:
        id = i.user.id
        bidding = BiddingHistory.objects.filter(customer_id = id)
        for b in bidding:
            dic1[b.id] = {'customer':b.customer.user.first_name +"  "+ b.customer.user.last_name, 'market':b.market.title +" - "+b.marketType,'game': b.game.title, 'digit': b.digit, 'points':b.points, 'status':b.status, 'winAmount':b.winAmount, 'date':b.date }
        

    params = {'users': users, 'history': dic1}
    return render(request, 'partner/bidding-history.html', params)


@login_required(login_url = '/partner/partner-login')
@check_broker_account()
def jodiBiddingHistory(request):
    partner = Partner.objects.get(user_id = request.user.id)
    users = PartnerUser.objects.filter(partner_id = partner.id)

    dic1 ={}
    for i in users:
        id = i.user.id
        bidding = JodiBiddingHistory.objects.filter(customer_id = id)
        for b in bidding:
            dic1[b.id] = {'customer':b.customer.user.first_name +"  "+ b.customer.user.last_name, 'market':b.market.closeTime ,'game': b.game.title, 'digit': b.digit, 'points':b.points, 'status':b.status, 'winAmount':b.winAmount, 'date':b.date }
        

    params = {'users': users, 'history': dic1}
    return render(request, 'partner/jodi-bidding-history.html', params)


@login_required(login_url = '/partner/partner-login')
@check_broker_account()
def withdrawRequest(request):
    partner = Partner.objects.get(user_id = request.user.id)
    withdraw  = PartnerWithdraw.objects.filter(partner_id = partner.id)

    params = {'withdraw': withdraw}
    return render(request, 'partner/withdraw.html', params)


@login_required(login_url = '/partner/partner-login')
@check_broker_account()
def newWithdrawRequest(request):
    partner = Partner.objects.get(user_id = request.user.id)
    withdraw  = PartnerWithdraw.objects.filter(partner_id = partner.id)

    # id = models.AutoField(primary_key=True)
    # partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    # amount = models.IntegerField(null=True, default= 0)  
    # biddingAmount = models.IntegerField(null=True, default= 0)  
    # commision = models.IntegerField(null=True, default= 2)  
    # date = models.DateField(null= True)
    # status = models.CharField(max_length=200, default="New")
    # remark = models.CharField(max_length=200, default="New Withdraw request")

    amount = request.POST['amount']
    remark = request.POST['remark']

    newRequest = PartnerWithdraw(partner = partner, amount= amount,biddingAmount= partner.payingBiddingAmount, commision = partner.commision, date= datetime.datetime.now(), remark = remark, )

    newRequest.save()
    messages.success(request, "New withdraw request has been sent to admin")
    return redirect('/partner/withdraw-request')

@login_required(login_url = '/partner/partner-login')
@check_broker_account()
def transferWallet(request,id ):
    broker = Partner.objects.get(id = id)
    payAbleBiiding = broker.payingBiddingAmount
    broker.walletAmount = float(broker.walletAmount)  + float((payAbleBiiding * 2)/100)
    broker.payingBiddingAmount = 0

    broker.save()
    return redirect('/partner') 
    
