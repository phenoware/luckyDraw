from django.urls import path,  re_path, include
from .import views

urlpatterns = [
    path('',views.home, name='home'),
    path('profile/',views.profile, name='profile'),
    path('about-us/',views.aboutUs, name='aboutUs'),
    path('contact-us/',views.contact, name='contact'),
    path('terms-condition/',views.terms, name='terms'),
    path('privacy-policy/',views.privacy, name='privacy'),
    path('refund-policy/',views.refund, name='refund'),
    path('email-template/',views.emailTemplate, name='emailTemplate'),


    path('paytm/',views.paytm, name='paytm'),
    path('handlerequest/',views.handlerequest, name='handlerequest'),
    path('payment-success/<str:transaction_id>/<str:amount>',views.paymentSuccess, name='paymentSuccess'),

    # User Authentication URL's
    path('user-login-page/',views.userLoginPage, name='userLoginPage'),
    path('user-login-apply/',views.userLoginAppy, name='userLoginAppy'),
    path('user-registration-page/',views.userRegistrationPage, name='userRegistrationPage'),
    path('user-registration-apply/',views.userRegistrationApply, name='userRegistrationApply'),
    path('user-logout/',views.userLogout, name='userLogout'),
    path('forgot-passowrd/',views.forgotPassword, name='forgotPassword'),
    path('reset-passord-link/',views.resetPasswordLink, name='resetPasswordLink'),
    path('check-otp/',views.checkOtp, name='checkOtp'),
    path('create-new-password/',views.createNewPassword, name='createNewPassword'),

    # Reguler  Market Listing & Game placing 
    path('game-list/<int:id>',views.gameList, name='gameList'),
    path('play-game/<int:marketId>/<int:gameId>',views.playGame, name='playGame'),
    path('place-bid/',views.placeBid, name='placeBid'),
    path('place-bid-megalot/',views.placeBidMegalot, name='placeBidMegalot'),

    # History
    path('history/',views.history, name='history'), 
    path('bidding-history/',views.biddingHistory, name='biddingHistory'),
    path('jodi-win-bid-history/',views.jodiWinBidHistory, name='jodiWinBidHistory'),
    path('bid-result-history/',views.bidResultHistory, name='bidResultHistory'),
    path('jodi-win-result-history/',views.jodiWinResultHistory, name='jodiWinResultHistory'),

    # Bid Details 
    path('bid-details/<int:id>',views.bidDetails, name='bidDetails'),
    path('jodi-win-bid-details/<int:id>',views.jodiWinBidDetails, name='jodiWinBidDetails'),

    # Top Winners top-winners 
    path('top-winners/',views.topWinners, name='topWinners'),
    path('top-jodi-winners/',views.topJodiWinners, name='topJodiWinners'),

    # Jodi Market Games & Bidding Place 
    path('jodi-win/',views.jodiWin, name='jodiWin'),
    path('jodi-game-list/<int:marketId>',views.jodiGameList, name='jodiGameList'),
    path('play-jodi-game/<int:marketId>/<int:gameId>',views.playJodiGame, name='playJodiGame'),
    path('place-jodi-bid/',views.placeJodiBid, name='placeJodiBid'),

    # Add Fund 
    path('add-funds/',views.addFund, name='addFund'),
    
    
    path('withdraw/',views.withdraw, name='withdraw'),
    path('pending-withdraw-request/',views.pendingWithdrawRequest, name='pendingWithdrawRequest'),
    path('send-withdraw-request/',views.sendWithdrawRequest, name='sendWithdrawRequest'),

    path('account-statement/',views.accountStatement, name='accountStatement'),

    # Games Rate 
    path('game-rate/',views.gameRate, name='gameRate'),

    # Rules & Notice Board 
    path('notice-board/',views.noticeBoard, name='noticeBoard'),
    
    # Notifications
    path('notifications/',views.notifications, name='notifications'),

    # Update bank details  
    path('update-bank-details/',views.updateBankDetails, name='updateBankDetails'),
    

    # Broker Management 
    path('broker-register/',views.brokerRegister, name='brokerRegister'),
    path('broker-registration-apply/',views.brokerRegistrationApply, name='brokerRegistrationApply'),


    

    # result Panel 
    path('jodi-game-panel-chart/<int:id>',views.jodiGamePanelChart, name='jodiGamePanelChart'),
    path('reguler-game-panel-chart/<int:id>',views.regulerGamePanelChart, name='regulerGamePanelChart'),

    # Add Card
    path('add-card/',views.addCart, name='addCart'),
    path('add-new-card/',views.addNewCart, name='addNewCart'),



    # products Management 
    path('products/',views.products, name='products'),
    path('product-details/<int:id>/',views.productsDetails, name='productsDetails'),
    path('cart/',views.cart, name='cart'),
    path('address/',views.address, name='address'),
    path('checkout/',views.checkout, name='checkout'),
    
    
    
]