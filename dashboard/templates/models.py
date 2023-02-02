from django.db import models
from  django.utils import timezone
from datetime import date
from django.conf import settings
from django.contrib.auth.models import User, auth


class UserRoll(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    roll = models.CharField(max_length=200, default="")

    def ___str___(self): 
            return self.roll   

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    roll = models.ForeignKey(UserRoll, on_delete=models.CASCADE)
    phone = models.CharField(max_length= 100, default= " ")
    walletAmount = models.IntegerField(null=True, default= 0)
    openingBalance = models.IntegerField(null=True, default= 0)
    status = models.CharField(max_length=200, default="")

    def ___str___(self): 
            return self.status           


class Partner(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length= 100, default= " ")
    city = models.CharField(max_length= 100, default= " ")
    address = models.TextField(default= " ")
    panNumber = models.CharField(max_length= 100, default= " ")
    bankName = models.CharField(max_length= 100, default= " ")
    accountNumber = models.CharField(max_length= 100, default= " ")
    ifscCode = models.CharField(max_length= 100, default= " ")
    earningAmount = models.IntegerField(null= True ,default= 0)
    commision = models.IntegerField(null= True ,default= 2)
    walletAmount = models.IntegerField(null=True, default= 0)
    openingBalance = models.IntegerField(null=True, default= 0)
    totalBiddingAmount = models.IntegerField(null=True, default= 0)
    payingBiddingAmount = models.IntegerField(null=True, default= 0)
    status = models.CharField(max_length=200, default="Acitve")

    def ___str___(self): 
            return self.phone           

class PartnerUser(models.Model):
    id = models.AutoField(primary_key=True)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=200, default="Acitve")

    def ___str___(self): 
            return self.phone           

class BankAccount(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    accountNumber = models.CharField(max_length=100, default="0")
    ifscCode = models.CharField(max_length= 300, default= "")
    bankName = models.CharField(max_length= 300, default= "")
    accountName = models.CharField(max_length= 300, default= "")
    status = models.CharField(max_length=200, default="")
    date = models.DateField(null =True)

    def ___str___(self): 
            return self.accountName           

class Market(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length = 300, default= " ")
    openTime = models.CharField(max_length=100, default= "")
    closeTime = models.CharField(max_length=100, default= "")
    status = models.CharField(max_length= 300, default= "Game running now")
    resultOpen = models.TextField(default= "***")
    resultClose = models.TextField(default= "***")
    
    openResultPattern = models.CharField(max_length= 300, default= "")
    closeResultPattern = models.CharField(max_length= 300, default= "")
    remark = models.CharField(max_length= 300, default= "")
    updateDate = models.DateField(null=True)
    
    def ___str___(self): 
            return self.title           

class JodiMarket(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length = 300, default= " ")
    closeTime = models.CharField(max_length=100, default= "")
    result = models.CharField(max_length= 300, default= "**")
    status = models.CharField(max_length= 300, default= "Game running now")
    remark = models.CharField(max_length= 300, default= "")
    
    def ___str___(self): 
            return self.title           
    
class Games(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length = 300, default= " ")
    marketType = models.CharField(max_length = 300, default= " ")  #Normal & Jodi
    rate = models.CharField(max_length= 300, default= "")
    multipleTimes = models.IntegerField(null= True , default= 9)
    status = models.CharField(max_length= 300, default= "Active")
    remark = models.CharField(max_length= 300, default= "")
    logo = models.ImageField(upload_to="dashboard/game/logo",default="")
    
    def ___str___(self): 
            return self.title           

class BiddingHistory(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    game = models.ForeignKey(Games, on_delete=models.CASCADE)
    rummyCard = models.TextField(default= "***")  
    jokerCard = models.TextField(default= "*")  
    cardPattern = models.CharField(max_length= 300, default= "")
    winAmount = models.IntegerField(null=True, default= 0)  
    points = models.CharField(max_length= 300, default= "")
    date = models.DateField(null= True)
    time = models.TimeField(null= True)
    status = models.CharField(max_length=200, default="")
    marketType = models.CharField(max_length=200, default="") #Open Or Close

    def ___str___(self): 
            return self.id           

class JodiBiddingHistory(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    market = models.ForeignKey(JodiMarket, on_delete=models.CASCADE)
    game = models.ForeignKey(Games, on_delete=models.CASCADE)
    digit = models.CharField(max_length= 30, default= "")  
    winAmount = models.IntegerField(null=True, default= 0)
    points = models.CharField(max_length= 300, default= "")
    date = models.DateField(null= True)
    time = models.TimeField(null= True)
    status = models.CharField(max_length=200, default="Placed")

    def ___str___(self): 
            return self.id           

class TopWinner(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    digit = models.IntegerField(null=True, default= 0)  
    points = models.CharField(max_length= 300, default= "")
    date = models.DateField(null= True)
    time = models.TimeField(null= True)
    status = models.CharField(max_length=200, default="Placed")

    def ___str___(self): 
            return self.id           

class JodiTopWinner(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    digit = models.IntegerField(null=True, default= 0)  
    points = models.CharField(max_length= 300, default= "")
    date = models.DateField(null= True)
    time = models.TimeField(null= True)
    status = models.CharField(max_length=200, default="Placed")

    def ___str___(self): 
            return self.id           

class Notifications(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    title = models.CharField(max_length= 300, default= "")
    msg = models.CharField(max_length= 500, default= "")
    date = models.DateField(null= True)
    status = models.CharField(max_length=200, default="Placed")

    def ___str___(self): 
            return self.id           

class Rulls(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length= 300, default= "")
    msg = models.CharField(max_length= 500, default= "")
    date = models.DateField(null= True)
    status = models.CharField(max_length=200, default="Placed")

    def ___str___(self): 
            return self.id           

# Banking operations 
class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.IntegerField(null=True, default= 0)  
    transactionType = models.CharField(max_length= 300, default= "")
    transactionMode = models.CharField(max_length= 300, default= "")
    signature = models.CharField(max_length= 300, default= "")
    successPaymentId = models.CharField(max_length= 300, default= "")
    successOrderId = models.CharField(max_length= 300, default= "")
    date = models.DateField(null= True)
    status = models.CharField(max_length=200, default="success")

    def ___str___(self): 
            return self.id           
# Withdraw request
class Withdraw(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.IntegerField(null=True, default= 0)  
    date = models.DateField(null= True)
    status = models.CharField(max_length=200, default="New")
    remark = models.CharField(max_length=200, default="New Withdraw request")

    def ___str___(self): 
            return self.id          

class PartnerWithdraw(models.Model):
    id = models.AutoField(primary_key=True)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    amount = models.IntegerField(null=True, default= 0)  
    biddingAmount = models.IntegerField(null=True, default= 0)  
    commision = models.IntegerField(null=True, default= 2)  
    date = models.DateField(null= True)
    status = models.CharField(max_length=200, default="New")
    remark = models.CharField(max_length=200, default="New Withdraw request")

    def ___str___(self): 
            return self.id          

# Android APK File 
class APKFile(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(null= True)
    apk = models.FileField(null=True)

    def ___str___(self): 
            return self.id          

# Result Panel Chart 
class PanelChartRegulerMarket(models.Model):
    id = models.AutoField(primary_key=True)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    openThreeDigit = models.TextField(default= "***")  
    closeThreeDigit = models.TextField(default= "***")  
    openSingleDigit = models.TextField(default= "***")  
    CloseSingleDigit = models.TextField(default= "***")  
    date = models.DateField(null= True)
    status = models.CharField(max_length=200, default="Closed")
    remark = models.CharField(max_length=200, default="Previous Result")

    def ___str___(self): 
            return self.id

class PanelChartJodiMarket(models.Model):
    id = models.AutoField(primary_key=True)
    market = models.ForeignKey(JodiMarket, on_delete=models.CASCADE)
    resultDigit = models.TextField(default= "**")  
    date = models.DateField(null= True)
    status = models.CharField(max_length=200, default="Closed")
    remark = models.CharField(max_length=200, default="Previous Result")

    def ___str___(self): 
            return self.id


class Card(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default= "")  
    value = models.CharField(max_length=200, default="")
    category = models.CharField(max_length=200, default="")
    image = models.ImageField(upload_to="dashboard/images/card",default="")
    def ___str___(self): 
            return self.id
