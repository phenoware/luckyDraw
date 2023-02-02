from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login,logout
from dashboard.models import *
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
import json

# Create your views here.



# User Authentication Views
def adminLogin(request):
    if request.user.is_authenticated:
        return redirect('/') 
    return render(request, 'dashboard/login.html')

def handleAdminLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request,'Login Suucessfull')
            return redirect('/dashboard')
            # return HttpResponse("Login Successfull")
        else:
            messages.success(request,'Invalid Credentials')
            return redirect('adminLogin')
    return render(request, "dashboard/error.html")

def userLogout(request):
    logout(request)
    messages.success(request,'Logout')
    return redirect('adminLogin')

def resetMarket(request):
    market = Market.objects.all()
    for i in market:
        i.status = "game is running now"
        i.resultOpen ="***" 
        i.resultClose ="***" 
        i.openResultPattern ="" 
        i.closeResultPattern ="" 
        i.save()
        
    joMarket = JodiMarket.objects.all()
    for i in joMarket:
        i.status = "game is running now"
        i.result ="**" 
        i.save()
    return redirect('/dashboard')



def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == 1:
            usersCount = Customer.objects.all().count()
            regulerMarketCount = Market.objects.all().count()
            jodiWinMarketCount = JodiMarket.objects.all().count()
            gamesCount = Games.objects.all().count()

            userWalletBalance = 0 
            users = Customer.objects.all()
            for i in users:
                userWalletBalance = userWalletBalance + int(i.walletAmount)

            pendingWithdrawRequest = Withdraw.objects.filter(status = 'New').count()
            
            pendingWithAmount = 0
            pendingWithdraw = Withdraw.objects.filter(status = 'New')
            for i in pendingWithdraw:
                pendingWithAmount = pendingWithAmount + int(i.amount)

            todaysBiddingCount = 0 
            todayBidding = BiddingHistory.objects.filter(date = datetime.datetime.now()).count()
            todayJodiBidding = JodiBiddingHistory.objects.filter(date = datetime.datetime.now()).count()

            todaysBiddingCount = todayBidding + todayJodiBidding    
            history = BiddingHistory.objects.filter(date = datetime.datetime.now())


            # upadate all market status ap per closing 
            # ct = datetime.datetime.now().strftime('%H:%M:%S') 
            
            # marketList = Market.objects.filter(closeTime__lte = ct)
            # for i in marketList:
            #     i.status = "Batting is closed for today"
            #     i.save()
            #     print(i)
            
            
            # marketListJodiwin = JodiMarket.objects.filter(closeTime__lte = ct)
            # for i in marketListJodiwin:
            #     i.status = "Batting is closed for today"
            #     i.save()
            #     print(i)

            
            params = {'usersCount': usersCount, 'regulerMarketCount': regulerMarketCount, 'jodiWinMarketCount':jodiWinMarketCount, 'gamesCount':gamesCount, 'userWalletBalance':userWalletBalance, 'pendingWithdrawRequest':pendingWithdrawRequest, 'pendingWithAmount':pendingWithAmount, 'todaysBiddingCount':todaysBiddingCount, 'history':history}
            return render(request, 'dashboard/index.html', params)
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')


# Market Listing

def regulerMarket(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == 1:
            markets = Market.objects.all()
            params = {'markets': markets }
            return render(request, 'dashboard/reguler-market.html', params)
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')

def marketDetails(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser == 1:
            cards = Card.objects.all()
            market = Market.objects.filter(id = id)
            for i in market:
                marketName = i.title
            marketObj = Market.objects.get(id = id)


            rummyGame  = Games.objects.get(id = 1)
            # rummyGame  = Games.objects.get(id = 1)
            megalotGame = Games.objects.get(id = 3)
            # megalotGame = Games.objects.get(id = 3)

            resultOpenCard = ''
            resultCloseCard = ''
            # Create dictionery for results card 
            if marketObj.resultOpen == '***':
                pass
            else:
                resultOpenCard = json.loads(marketObj.resultOpen)

            if marketObj.resultClose == '***':
                pass
            else:
                resultCloseCard = json.loads(marketObj.resultClose)

            # Bidding Count 
            biddingAmount = BiddingHistory.objects.filter(market = marketObj, date= datetime.datetime.now()).aggregate(Sum('points'))
            totalBidding = BiddingHistory.objects.filter(market = marketObj, date= datetime.datetime.now()).count()

            bidding  = BiddingHistory.objects.filter(market = marketObj, date= datetime.datetime.now())
  

            # Loading Dictiony For OPen Bidding 
            biddingOpen  = BiddingHistory.objects.filter(market = marketObj, game = rummyGame, date= datetime.datetime.now(), marketType="open")
            Dic1 = {}

            for i in biddingOpen:
                cardPattern = i.cardPattern
                rc = BiddingHistory.objects.filter(cardPattern= cardPattern, market = marketObj, game = rummyGame, date= datetime.datetime.now(), marketType="open")
                for r in rc:
                    openRummyCard = r.rummyCard
                    openJokerCard = r.jokerCard
                
                openRummyCardDict = json.loads(openRummyCard)
                openJokerCardDict = json.loads(openJokerCard)
                
                # print("images are :" +str(imagesopen), type(imagesopen))
                # Rummy Cards Count  and points 
                openCardCount = BiddingHistory.objects.filter(cardPattern= cardPattern, market = marketObj, game = rummyGame, date= datetime.datetime.now(), marketType="open").count()

                totalPointsOpenCard = BiddingHistory.objects.filter(cardPattern= cardPattern, market = marketObj, game = rummyGame,date= datetime.datetime.now(), marketType="open").aggregate(Sum('points'))
                
                Dic1[cardPattern] = {'totalPointsOpenCard':totalPointsOpenCard, 'openCardCount':openCardCount , 'openRummyCard':openRummyCard, 'openJokerCard':openJokerCard, 'openRummyCardDict':openRummyCardDict, 'openJokerCardDict':openJokerCardDict}
                
                
            
            # Loading Dictiony For Close Bidding 
            biddingClose  = BiddingHistory.objects.filter(market = marketObj,game = rummyGame, date= datetime.datetime.now(), marketType="close")
            Dic2 = {}
            for i in biddingClose:
                cardPattern = i.cardPattern
                rc = BiddingHistory.objects.filter(cardPattern= cardPattern, game = rummyGame, market = marketObj, date= datetime.datetime.now(), marketType="close")
                for r in rc:
                    closeRummyCard = r.rummyCard
                    closeJokerCard = r.jokerCard
                
                closeRummyCardDict = json.loads(closeRummyCard)
                closeJokerCardDict = json.loads(closeJokerCard)
                
                # close rummyCard count and points 
                closeCardCount = BiddingHistory.objects.filter(cardPattern= cardPattern, game = rummyGame, market = marketObj, date= datetime.datetime.now(), marketType="close").count()

                totalPointsCloseCard = BiddingHistory.objects.filter(cardPattern= cardPattern, game = rummyGame, market = marketObj, date= datetime.datetime.now(), marketType="close").aggregate(Sum('points'))
  


                Dic2[cardPattern] = {'totalPointsCloseCard':totalPointsCloseCard, 'closeCardCount':closeCardCount, 'closeRummyCardDict':closeRummyCardDict,  'closeJokerCardDict': closeJokerCardDict}
                

            rummyCardDict ={}
            jokerCardDict ={}
            for i in bidding:
                rummyCards = json.loads(i.rummyCard) 
                rummyCardDict[i] = {'rummyCards': rummyCards}

                jokerCards = json.loads(i.jokerCard) 
                jokerCardDict[i] = {'jokerCards':jokerCards}

           

            # Loading Dictiony For megalot Bidding 
            biddingMegalot  = BiddingHistory.objects.filter(market = marketObj, game = megalotGame, date= datetime.datetime.now())
            dictMegalot = {}

            for i in biddingMegalot:
                cardPattern = i.cardPattern
                rc = BiddingHistory.objects.filter(cardPattern= cardPattern, market = marketObj, game = megalotGame, date= datetime.datetime.now())
                for r in rc:
                    openRummyCardMegalot = r.rummyCard
                    openJokerCardMegalot = r.jokerCard
                
                openRummyCardDictMegalot = json.loads(openRummyCardMegalot)
                openJokerCardDictMegalot = json.loads(openJokerCardMegalot)
                
                # print("images are :" +str(imagesopen), type(imagesopen))
                # Rummy Cards Count  and points 
                megalotCardCount = BiddingHistory.objects.filter(cardPattern= cardPattern, market = marketObj, game = megalotGame, date= datetime.datetime.now()).count()

                totalPointsMegalotCard = BiddingHistory.objects.filter(cardPattern= cardPattern, market = marketObj, game = megalotGame,date= datetime.datetime.now()).aggregate(Sum('points'))
                
                dictMegalot[cardPattern] = {'totalPointsOpenCard':totalPointsMegalotCard, 'openCardCount':megalotCardCount , 'openRummyCardDict':openRummyCardDictMegalot, 'openJokerCardDict':openJokerCardDictMegalot}


            params = {'market': market,'totalBidding':totalBidding, 'biddingAmount':biddingAmount, 'bidding':bidding, 'biddingOpen':biddingOpen, 'biddingClose':biddingClose, 'Dic1' :Dic1,'Dic2' :Dic2 , 'marketName':marketName, 'cards':cards, 'resultOpenCard':resultOpenCard, 'marketObj':marketObj, 'resultCloseCard':resultCloseCard, 'rummyCardDict':rummyCardDict, 'jokerCardDict':jokerCardDict, 'dictMegalot':dictMegalot}

            return render(request, 'dashboard/market-details.html', params)
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')



def jodiMarketDetails(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser == 1:
            cards = Card.objects.all()
            market = JodiMarket.objects.filter(id = id)
            marketObj = JodiMarket.objects.get(id = id)
            
            resultCard = ''
            if marketObj.result == '**':
                pass
            else:
                resultCard = json.loads(marketObj.result)
            # Get Game List 
            jodiDigit  = Games.objects.get(id = 2)
            # jodiDigit  = Games.objects.get(id = 2)


            # Jodi Digit  
            gameJodiDigit = JodiBiddingHistory.objects.filter(market = marketObj, game = jodiDigit,date= datetime.datetime.now())

            # Bidding Count 
            biddingAmount = JodiBiddingHistory.objects.filter(market = marketObj, game = jodiDigit, date= datetime.datetime.now()).aggregate(Sum('points')) 
            totalBidding = JodiBiddingHistory.objects.filter(market = marketObj, game = jodiDigit, date= datetime.datetime.now()).count()
            bidding  = JodiBiddingHistory.objects.filter(market = marketObj, game = jodiDigit, date= datetime.datetime.now())
            
            # Loading Dictiony For Jodi Win Jodi Bidding 
            jodiWinDigitList  = JodiBiddingHistory.objects.filter(market = marketObj, game = jodiDigit,date= datetime.datetime.now())
            dic1 = {}
            for i in jodiWinDigitList: 
                cardPattern = i.cardPattern
                rc = JodiBiddingHistory.objects.filter(cardPattern= cardPattern, market = marketObj, game = jodiDigit,
                date= datetime.datetime.now())
                for r in rc:
                    resultCardDict = json.loads(r.resultCard)
                
                digitCount = JodiBiddingHistory.objects.filter(cardPattern= cardPattern, market = marketObj, game = jodiDigit,
                date= datetime.datetime.now()).count()

                totalPoints = JodiBiddingHistory.objects.filter(cardPattern= cardPattern, market = marketObj, game = jodiDigit,
                date= datetime.datetime.now()).aggregate(Sum('points'))


                dic1[cardPattern] = {'totalPoints':totalPoints, 'digitCount':digitCount, 'resultCardDict':resultCardDict }
            

            cardsImgDict ={}
            for i in jodiWinDigitList:
                cardsImg = json.loads(i.resultCard) 
                cardsImgDict[i] = {'cardsImg': cardsImg}


            params = {'market': market, 'gameJodiDigit':gameJodiDigit, 'totalBidding':totalBidding, 'biddingAmount':biddingAmount, 'jodiWinDigitList':dic1, 'marketObj':marketObj, 'cards':cards , 'resultCard':resultCard, 'cardsImgDict':cardsImgDict}

            return render(request, 'dashboard/jodi-market-details.html', params)
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')

def editMarket(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == 1:

            id = request.POST['id']
            market = Market.objects.get(id = id)
            
            market.title = request.POST['title']
            market.openTime = request.POST['openTime']
            market.closeTime = request.POST['closeTime']
            market.status = request.POST['status']
            market.save()
            messages.success(request, "Market Result Updated")
           
            
            return redirect('/dashboard/market-detials/'+str(id))
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')

def editJodiwinMarket(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == 1:

            id = request.POST['id']
            market = JodiMarket.objects.get(id = id)
            
            market.title = request.POST['title']
            market.closeTime = request.POST['closeTime']
            market.status = request.POST['status']
            market.save()
            messages.success(request, "Market Result Updated")
            
            return redirect('/dashboard/jodi-market-detials/'+str(id))
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')


# Delete Market 
def deleteRegulerMarket(request,id):
    if request.user.is_authenticated:
        if request.user.is_superuser == 1:
            market = Market.objects.get(id = id )
            market.delete()

            messages.success(request, "Market Deleted Successfully")
            return redirect('/dashboard/reguler-market')
            
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')

def deleteJodiMarket(request,id):
    if request.user.is_authenticated:
        if request.user.is_superuser == 1:
            market = JodiMarket.objects.get(id = id )
            market.delete()

            messages.success(request, "Jodi Market Deleted Successfully")
            return redirect('/dashboard/jodi-market')
            
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')

# Declare Result Here 
def updateOpenFourCards(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == 1:

            id = request.POST['id']
            openCard = request.POST['openCard']
            rummyGame  = Games.objects.get(id = 1)
            # rummyGame  = Games.objects.get(id = 1)
            # Create open card pattern 
            openCardPattern= ""
            openCardDict = json.loads(request.POST['openCard'])
            for c in openCardDict.values():
                openCardPattern = openCardPattern + str(c[0])

            market = Market.objects.get(id = id)
            
            market.openResultPattern = openCardPattern
            market.resultOpen = openCard
            market.status = "game is running for close"
            market.save()
            messages.success(request, "Market Result Updated")
            
            if PanelChartRegulerMarket.objects.filter(market_id = id,date = datetime.datetime.now()).exists():
                print("Under panel chart")
                chart = PanelChartRegulerMarket.objects.get(market_id = id, date = datetime.datetime.now())
                chart.openThreeDigit = openCard
                chart.save()
            else:
                chart = PanelChartRegulerMarket(openThreeDigit = openCard, date= datetime.datetime.now(), market = market)
                chart.save()

            reusltOpenThreeDigit = BiddingHistory.objects.filter(market = market , game= rummyGame, date= datetime.datetime.now(), marketType= "open")
            
            for i in reusltOpenThreeDigit:
                winnigPoint =0
                if int(i.cardPattern) == int(openCardPattern):
                    i.status = 'win'
                    i.winAmount = int(i.points)* i.game.multipleTimes
                    winnigPoint = int(i.points)* i.game.multipleTimes
                    i.save()

                    customer = Customer.objects.get(id = i.customer.id)
                    customer.walletAmount = customer.walletAmount + winnigPoint
                    customer.save()
                
                else:
                    i.status = 'loss'
                    i.save()        
            
            
            return redirect('/dashboard/market-detials/'+str(id))
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')

def updateCloseFourCards(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == 1:

            id = request.POST['id']
            closeCard = request.POST['closeCard']
            rummyGame  = Games.objects.get(id = 1)
            # rummyGame  = Games.objects.get(id = 1)
            # Create open card pattern 
            closeCardPattern= ""
            closeCardDict = json.loads(request.POST['closeCard'])
            for c in closeCardDict.values():
                closeCardPattern = closeCardPattern + str(c[0])

            market = Market.objects.get(id = id)
          
            market.closeResultPattern = closeCardPattern
            market.resultClose = closeCard
            market.status = "game is closed for today"
            market.save()
            messages.success(request, "Market Result Updated")
            
            if PanelChartRegulerMarket.objects.filter(market_id = id,date = datetime.datetime.now()).exists():
                print("Under panel chart")
                chart = PanelChartRegulerMarket.objects.get(market_id = id,date = datetime.datetime.now())
                chart.closeThreeDigit = closeCard
                chart.save()
            else:
                chart = PanelChartRegulerMarket(closeThreeDigit = closeCard, date= datetime.datetime.now(), market = market)
                chart.save()

            reusltCloseThreeDigit = BiddingHistory.objects.filter(market = market , game= rummyGame, date= datetime.datetime.now(), marketType= "close")
            
            if(reusltCloseThreeDigit):
                for i in reusltCloseThreeDigit:
                    winnigPoint =0
                    if int(i.cardPattern) == int(closeCardPattern):
                        i.status = 'win'
                        i.winAmount = int(i.points)* i.game.multipleTimes
                        winnigPoint = int(i.points)* i.game.multipleTimes
                        i.save()
                        
                        customer = Customer.objects.get(id = i.customer.id)
                        customer.walletAmount = customer.walletAmount + winnigPoint
                        customer.save()
                    else:
                        i.status = 'loss'
                        i.save()

                    
            
            # Declrae Mega Lot result
            ocr = market.openResultPattern
            ccr = market.closeResultPattern
            megaCardPattern = ocr + ccr
            megalotGame = Games.objects.get(id = 3)
            # megalotGame = Games.objects.get(id = 3)
            megalotGameBiddingHistory = BiddingHistory.objects.filter(market = market , game = megalotGame,  date= datetime.datetime.now(), marketType= "close")

            for i in megalotGameBiddingHistory:
                openCardPattern= ""
                closeCardPattern= ""
                rummyCardDict = json.loads(i.rummyCard)
                jokerCardDict = json.loads(i.jokerCard)
                rummyCount = 0
                jokerCount = 0

                # OPenCard Result 
                for c in rummyCardDict.values():
                    if(rummyCount < 3):
                        openCardPattern = openCardPattern + str(c[0])
                        rummyCount = rummyCount + 1
                    else:
                        closeCardPattern = closeCardPattern + str(c[0])

                for c in jokerCardDict.values():
                    if(jokerCount < 1):
                        openCardPattern = openCardPattern + str(c[0])
                        jokerCount = jokerCount + 1
                    else:
                        closeCardPattern = closeCardPattern + str(c[0])

                cardPattern = openCardPattern + closeCardPattern
                
                # Make win or loss customer
                winnigPoint =0
                if int(cardPattern) == int(megaCardPattern):
                    i.status = 'win'
                    i.winAmount = int(i.points)* i.game.multipleTimes
                    winnigPoint = int(i.points)* i.game.multipleTimes
                    i.save()
                            
                    customer = Customer.objects.get(id = i.customer.id)
                    customer.walletAmount = customer.walletAmount + winnigPoint
                    customer.save()
                else:
                    i.status = 'loss'
                    i.save()
                 
                        

            print(megaCardPattern)
            return redirect('/dashboard/market-detials/'+str(id))
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')

def updateOpenSingleDigit(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == 1:

            id = request.POST['id']
            market = Market.objects.get(id = id)
            
            market.reusltOpenAnk = request.POST['reusltOpenAnk']
            market.status = "Batting is running for close"
            resultDigit = request.POST['reusltOpenAnk']
            market.save()
            messages.success(request, "Market Result Updated")

             # Get Game List 
            rate = 0 
            singleDigit = Games.objects.get(id = 10)
            jodiDigit  = Games.objects.get(id = 4)
            singleDigitRate = Games.objects.filter(id = 10)

            if PanelChartRegulerMarket.objects.filter(market_id = id,date = datetime.datetime.now()).exists():
                print("Under panel chart")
                chart = PanelChartRegulerMarket.objects.get(market_id = id,date = datetime.datetime.now())
                chart.openSingleDigit = resultDigit
                chart.save()
            else:
                chart = PanelChartRegulerMarket(openSingleDigit = resultDigit, date= datetime.datetime.now(), market = market)
                chart.save()

            resultOpenSingleDigit = BiddingHistory.objects.filter(market = market , game= singleDigit, date= datetime.datetime.now(), marketType= "open")
            
            for i in resultOpenSingleDigit:
                winnigPoint = 0
                if int(i.digit) == int(resultDigit):
                    i.status = 'win'
                    i.winAmount = int(i.points)* i.game.multipleTimes
                    winnigPoint = int(i.points)* i.game.multipleTimes
                    i.save()

                    customer = Customer.objects.get(id = i.customer.id)
                    customer.walletAmount = customer.walletAmount + winnigPoint
                    customer.save()
                    
                else:
                    i.status = 'loss'
                    i.save()        
            
            
            return redirect('/dashboard/market-detials/'+str(id))
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')

def updatecloseSingleDigit(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == 1:

            id = request.POST['id']
            market = Market.objects.get(id = id)
            
            market.reusltCloseAnk = request.POST['reusltCloseAnk']
            market.status = "Batting is closed for today"
            resultDigit = request.POST['reusltCloseAnk']
            market.save()
            messages.success(request, "Market Result Updated")

            if PanelChartRegulerMarket.objects.filter(market_id = id,date = datetime.datetime.now()).exists():
                print("Under panel chart")
                chart = PanelChartRegulerMarket.objects.get(market_id = id,date = datetime.datetime.now())
                chart.CloseSingleDigit = resultDigit
                chart.save()
            else:
                chart = PanelChartRegulerMarket(CloseSingleDigit = resultDigit, date= datetime.datetime.now(), market = market)
                chart.save()    

            jodiResultDigit = 0
            m= Market.objects.filter(id = id)
            for i in m:
                jodiResultDigit = i.reusltOpenAnk + i.reusltCloseAnk

            # Get Game List 
            rate = 0 
            singleDigit = Games.objects.get(id = 10)
            jodiDigit  = Games.objects.get(id = 4)
            singleDigitRate = Games.objects.filter(id = 10)

            for i in singleDigitRate:
                rate = i.multipleTimes



            # Result for close single digit 
            resultCloseSingleDigit = BiddingHistory.objects.filter(market = market , game= singleDigit, date= datetime.datetime.now(), marketType= "close")
            
            for i in resultCloseSingleDigit:
                winnigPoint = 0
                if int(i.digit) == int(resultDigit):
                    i.status = 'win'
                    i.winAmount = int(i.points)* rate 
                    winnigPoint = int(i.points)* rate
                    i.save()

                    customer = Customer.objects.get(id = i.customer.id)
                    customer.walletAmount = customer.walletAmount + winnigPoint
                    customer.save()
                else:
                    i.status = 'loss'
                    i.save()        
            
            # Result for jodi 
            jodiDigitResult = BiddingHistory.objects.filter(market = market , game= jodiDigit, date= datetime.datetime.now())
            
            for i in jodiDigitResult:
                winnigPoint = 0
                if int(i.digit) == int(jodiResultDigit):
                    i.status = 'win'
                    i.winAmount = int(i.points)* i.game.multipleTimes
                    winnigPoint = int(i.points)* i.game.multipleTimes
                    i.save()

                    customer = Customer.objects.get(id = i.customer.id)
                    customer.walletAmount = customer.walletAmount + winnigPoint
                    customer.save()
                else:
                    i.status = 'loss'
                    i.save()        
            
            
            return redirect('/dashboard/market-detials/'+str(id))
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')

# Jodi Win Result 
def updateJodiWinDigit(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == 1:

            id = request.POST['id']
            result = request.POST['resultCard']
            market = JodiMarket.objects.get(id = id)
            
            resultPattern= ""
            resultCardDict = json.loads(result)
            for c in resultCardDict.values():
                resultPattern = resultPattern + str(c[0])


            market.result = result
            market.resultPattern = resultPattern
            market.status = "game is closed for today"
            market.save()
            messages.success(request, "Market Result Updated")
            
            if PanelChartJodiMarket.objects.filter(market_id = id,date = datetime.datetime.now()).exists():
                print("Under panel chart")
                chart = PanelChartJodiMarket.objects.get(market_id = id,date = datetime.datetime.now())
                chart.resultDigit = result
                chart.save()
            else:
                chart = PanelChartJodiMarket(resultDigit = result, date= datetime.datetime.now(), market = market)
                chart.save()

            # Get Game List 
            rate = 0 
            jodiDigit  = Games.objects.get(id = 2)
            # jodiDigit  = Games.objects.get(id = 2)
            jodiDigitRate = Games.objects.filter(id = 2)
            # jodiDigitRate = Games.objects.filter(id = 2)

            for i in jodiDigitRate:
                rate = i.multipleTimes

            # Result for jodi 
            jodiDigitResult = JodiBiddingHistory.objects.filter(market = market , game= jodiDigit, date= datetime.datetime.now())
            
            for i in jodiDigitResult:
                winnigPoint = 0 
                if int(i.cardPattern) == int(resultPattern):
                    i.status = 'win'
                    i.winAmount = int(i.points)* rate
                    winnigPoint = int(i.points)* rate
                    i.save()

                    customer = Customer.objects.get(id = i.customer.id)
                    customer.walletAmount = customer.walletAmount + winnigPoint
                    customer.save()
                else:
                    i.status = 'loss'
                    i.save()        
            
            
            return redirect('/dashboard/jodi-market-detials/'+str(id))
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')



def addRegulerMarket(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == 1:

            title = request.POST['title']
            openTime = request.POST['openTime']
            closeTime = request.POST['closeTime']

            market = Market(title=title, openTime= openTime, closeTime=closeTime )
            market.save()

            messages.success(request, "Market Addedd Successfully")
            return redirect('regulerMarket')
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')


def jodiMarket(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == 1:
            markets = JodiMarket.objects.all()

            resultCardsDict ={}
            resultCards= {}
            for i in markets:
                if i.result == '**':
                    pass
                else:
                    resultCards = json.loads(i.result) 
                    resultCardsDict[i] = {'resultCards': resultCards}


            params = {'markets': markets, 'resultCardsDict':resultCardsDict }
            return render(request, 'dashboard/jodi-market.html', params)
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')


def addJodiMarket(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == 1:

            title = request.POST['title']
            closeTime = request.POST['closeTime']

            market = JodiMarket(title=title, closeTime=closeTime )
            market.save()

            messages.success(request, "Market Addedd Successfully")
            return redirect('jodiMarket')
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')


# Games
def games(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == 1:
            games = Games.objects.all()
            params = {'games': games }
            return render(request, 'dashboard/games.html', params)
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')

def updateGame(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == 1:

            id = request.POST['id']
            game = Games.objects.get(id = id)
            game.title = request.POST['title']
            game.marketType = request.POST['marketType']
            game.rate = request.POST['rate']
            game.multipleTimes = request.POST['multipleTimes']

            game.save()

            messages.success(request, "Game update Successfully")
            return redirect('games')
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')

def addGame(request):
    return render(request, "dashboard/add-game.html")

def submitNewGame(request):
    
    title = request.POST['title']
    marketType = request.POST['marketType']
    rate = request.POST['rate']
    title = request.POST['title']
    multipleTimes = request.POST['multipleTimes']
    logo = request.FILES['logo']

    game = Games(title= title, marketType = marketType, rate= rate, multipleTimes= multipleTimes, logo= logo)
    game.save()
    return redirect('/dashboard/add-game')
def users(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == 1:
            users = Customer.objects.all()
            params = {'users': users }
            return render(request, 'dashboard/users.html', params)
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')

def userDetails(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser == 1:
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

            params = {'customer': customer, 'biddingHistory': biddingHistory, 'jodiBiddingHistory': jodiBiddingHistory, 'withdraw':withdraw, 
            'transaction': transaction, 'bankAccount':bankAccount, 'totalBidding':totalBidding , 'totalWin':totalWin}
            return render(request, 'dashboard/user-details.html', params)
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')


#Transaction History 
def transaction(request):
    if request.user.is_authenticated:   
        if request.user.is_superuser == 1:
            transactions = Transaction.objects.all()

            params = {'transactions': transactions}
            return render(request,'dashboard/transaction.html', params)
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')

def withdrawRequest(request):
    if request.user.is_authenticated:   
        if request.user.is_superuser == 1:
            withdraw = Withdraw.objects.all()

            params = {'withdraw': withdraw}
            return render(request,'dashboard/withdraw.html', params)
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')

def makeWithdraw(request, id, status):
    if request.user.is_authenticated:   
        if request.user.is_superuser == 1:
            withdraw = Withdraw.objects.get(id= id)
            withdrawRequest = Withdraw.objects.filter(id= id)
            amount =0 
            for i in withdrawRequest:
                amount= amount + int(i.amount)
                custId = i.customer.id
            
            if status == "Done":
                messages.success(request, "Payment already transfered")
                return redirect('/dashboard/withdraw-request')
            elif status == 'New':
                withdraw.status = "Done"
                withdraw.remark = "Payment transfered "
                withdraw.save()

                # customer= Customer.objects.filter(id = custId)
                # walletBalance = 0 
                # for i in customer:
                #     walletBalance = walletBalance + i.walletAmount

                # customerObj = Customer.objects.get(id = custId)
                # customerObj.walletAmount = walletBalance - amount
                # customerObj.save()

                messages.success(request, "Status updated")
                return redirect('/dashboard/withdraw-request')

        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')

# Bidding History 
def biddingHistory(request):
    if request.user.is_authenticated:   
        if request.user.is_superuser == 1:
            history = BiddingHistory.objects.all()

            params = {'history': history}
            return render(request,'dashboard/bidding-history.html', params)
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')

def biddingResultHistory(request):
    if request.user.is_authenticated:   
        if request.user.is_superuser == 1:
            history = BiddingHistory.objects.filter(status= "win")

            params = {'history': history}
            return render(request,'dashboard/bidding-result-history.html', params)
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')


# Jodi Bidding History
def jodiBiddingHistory(request):
    if request.user.is_authenticated:   
        if request.user.is_superuser == 1:
            history = JodiBiddingHistory.objects.all()

            params = {'history': history}
            return render(request,'dashboard/jodi-bidding-history.html', params)
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')

def jodiWinBiddingResultHistory(request):
    if request.user.is_authenticated:   
        if request.user.is_superuser == 1:
            history = JodiBiddingHistory.objects.filter(status= "win")

            params = {'history': history}
            return render(request,'dashboard/jodi-win-result-bidding.html', params)
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')


def brokers(request):
    if request.user.is_authenticated:   
        if request.user.is_superuser == 1:
            broker = Partner.objects.all()

            params = {'broker': broker}
            return render(request,'dashboard/brokers.html', params)
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')

def brokerDetails(request, id):
    if request.user.is_authenticated:   
        if request.user.is_superuser == 1:
            broker = Partner.objects.filter(id = id )
            brokerUsers = PartnerUser.objects.filter(partner_id = id)
            userCount = PartnerUser.objects.filter(partner_id = id).count()
            withdraw = PartnerWithdraw.objects.filter(partner_id = id)

            params = {'broker': broker, 'brokerUsers':brokerUsers, 'userCount':userCount, 'withdraw':withdraw}
            return render(request,'dashboard/broker-details.html', params)
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')

# Broker Withdraw Mmanagement 
def brokerWithdrawRequest(request):
    if request.user.is_authenticated:   
        if request.user.is_superuser == 1:
            withdraw = PartnerWithdraw.objects.all()
            print(withdraw)
            params = {'withdraw':withdraw}
            return render(request,'dashboard/broker-withdraw.html',params)
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')

def makeBrokerWithdraw(request, id, status):
    if request.user.is_authenticated:   
        if request.user.is_superuser == 1:
            withdraw = PartnerWithdraw.objects.get(id= id)
            withdrawRequest = PartnerWithdraw.objects.filter(id= id)
            amount =0 
            
            for i in withdrawRequest:
                amount= amount + int(i.amount)
                brokerId = i.partner.id
            
            if status == "Done":
                messages.success(request, "Payment already transfered")
                return redirect('/dashboard/broker-withdraw-request')
            elif status == 'New':
                withdraw.status = "Done"
                withdraw.remark = "Payment transfered "
                withdraw.save()

                partner= Partner.objects.get(id = brokerId)
                partner.walletAmount = partner.walletAmount - amount
                partner.earningAmount = partner.earningAmount + amount
                partner.save()

                messages.success(request, "Status updated")
                return redirect('/dashboard/broker-withdraw-request')

        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')


# Result Panel Chart reguler market
def resultPanelRegulerMarket(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == 1:
            markets = Market.objects.all()
            params = {'markets': markets }
            return render(request, 'dashboard/reguler-market-result-panel.html', params)
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')

def addResultChart(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser == 1:
            markets = PanelChartRegulerMarket.objects.filter(market_id = id)
            params = {'markets': markets , 'marketId':id }
            return render(request, 'dashboard/reguler-market-result-panel-chart.html', params)
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')

def addResultRegulerMarket(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == 1:
            id = request.POST['id']
            market = Market.objects.get(id = request.POST['id'])
            openThreeDigit = request.POST['openThreeDigit']
            closeThreeDigit = request.POST['closeThreeDigit']
            openSingleDigit = request.POST['openSingleDigit']
            CloseSingleDigit = request.POST['closeSingleDigit']
            date = datetime.datetime.now()
            chart= PanelChartRegulerMarket(market = market, openThreeDigit = openThreeDigit, closeThreeDigit= closeThreeDigit, openSingleDigit=openSingleDigit, CloseSingleDigit=CloseSingleDigit, date= date)
            chart.save()
            messages.success(request, "New result added in chart")
            
            return redirect('/dashboard/add-result-chart/'+str(id)+'/')
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')


# Result Panel Chart jodi win market  market
def resultPanelJodiMarket(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == 1:
            markets = JodiMarket.objects.all()
            params = {'markets': markets }
            return render(request, 'dashboard/jodi-market-result-panel.html', params)
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')

def addJodiResultChart(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser == 1:
            markets = PanelChartJodiMarket.objects.filter(market_id = id)
            params = {'markets': markets , 'marketId':id }
            return render(request, 'dashboard/jodi-market-result-panel-chart.html', params)
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')

def addResultJodiMarket(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == 1:
            id = request.POST['id']
            market = JodiMarket.objects.get(id = request.POST['id'])
            resultDigit = request.POST['resultDigit']
            date = datetime.datetime.now()
            chart= PanelChartJodiMarket(market = market, resultDigit = resultDigit, date= date)
            chart.save()
            messages.success(request, "New result added in chart")
            
            return redirect('/dashboard/add-jodi-result-chart/'+str(id)+'/')
        messages.success(request, 'You are not authorized to access') 
        return render(request, 'dashboard/login.html')
    return redirect('adminLogin')


def productsList(request):
    products = Product.objects.all().order_by('-id')

    params = {'products':products}
    return render(request, 'dashboard/products.html', params)

def addNewProduct(request):
    if request.method == 'POST':
        name = request.POST['name'] 
        price = request.POST['price'] 
        unit = request.POST['unit'] 
        description = request.POST['description'] 
        image = request.FILES['image'] 

        product = Product(name = name, price = price, unit= unit, image= image, description= description)
        product.save()
        messages.success(request, 'Product added')
        return redirect('/dashboard/products')     
    return redirect('/dashboard/products')

def updateProduct(request, id):
    product  = Product.objects.get(id = id )
    product.name = request.POST['name']
    product.price = request.POST['price']
    product.unit = request.POST['unit']
    product.status = request.POST['status']

    product.save()
    messages.success(request, 'Products updated')
    return redirect('/dashboard/products')

def deletProduct(request, id):
    product  = Product.objects.get(id = id )
    product.delete()

    messages.success(request, 'Products deleted')
    return redirect('/dashboard/products')
