from django.urls import path
from .import views

urlpatterns = [

    # Partner authentication process
    path('partner-login/',views.partnerLogin, name='partnerLogin'),
    path('handle-broker-login/',views.handleBrokerLogin, name='handleBrokerLogin'),
    path('broker-logout/',views.brokerLogout, name='brokerLogout'),

    path('',views.home, name='home'),

    # refer user management     
    path('users/',views.users, name='users'),
    path('add-new-user/',views.addNewUser, name='addNewUser'),
    path('user-details/<int:id>/',views.userDetails, name='userDetails'),

    # History  
    path('bidding-history/',views.biddingHistory, name='biddingHistory'),
    path('jodi-bidding-history/',views.jodiBiddingHistory, name='jodiBiddingHistory'),

    # withdraw request  
    path('withdraw-request/',views.withdrawRequest, name='withdrawRequest'),
    path('new-withdraw-request/',views.newWithdrawRequest, name='newWithdrawRequest'),

    # Transfer Wallet 
    path('transfer-wallet/<int:id>',views.transferWallet, name='transferWallet'),

]