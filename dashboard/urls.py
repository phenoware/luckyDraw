from django.urls import path
from .import views

urlpatterns = [
    path('',views.home, name='home'),
    path('reset-market/',views.resetMarket, name='resetMarket'),

    # User Authentication URL's
    path('admin-login/',views.adminLogin, name='adminLogin'),
    path('handle-admin-login/',views.handleAdminLogin, name='handleAdminLogin'),
    path('admin-logout/',views.userLogout, name='userLogout'),

    # Market Listing 
    path('reguler-market/',views.regulerMarket, name='regulerMarket'),
    path('market-detials/<int:id>/',views.marketDetails, name='marketDetails'),
    path('jodi-market-detials/<int:id>/',views.jodiMarketDetails, name='jodiMarketDetails'),

    # Declare Result 
    path('update-open-four-cards/',views.updateOpenFourCards, name='updateOpenFourCards'),
    path('update-close-four-cards/',views.updateCloseFourCards, name='updateCloseFourCards'),
    path('update-open-single-digit/',views.updateOpenSingleDigit, name='updateOpenSingleDigit'),
    path('update-close-single-digit/',views.updatecloseSingleDigit, name='updatecloseSingleDigit'),

    # Result for Jodi Win 
    path('update-jodi-win-digit/',views.updateJodiWinDigit, name='updateJodiWinDigit'),

    # Delete Market  
    path('delete-reguler-market/<int:id>',views.deleteRegulerMarket, name='deleteRegulerMarket'),
    path('delete-jodi-market/<int:id>',views.deleteJodiMarket, name='deleteJodiMarket'),

    path('edit-market/',views.editMarket, name='editMarket'),
    path('edit-jodi-win-market/',views.editJodiwinMarket, name='editJodiwinMarket'),
    path('add-reguler-market/',views.addRegulerMarket, name='addRegulerMarket'),
    path('jodi-market/',views.jodiMarket, name='jodiMarket'),
    path('add-jodi-market/',views.addJodiMarket, name='addJodiMarket'),

    #Games
    path('games/',views.games, name='games'),
    path('update-game/',views.updateGame, name='updateGame'),
    path('add-game/',views.addGame, name='addGame'),
    path('submit-new-game/',views.submitNewGame, name='submitNewGame'),

    

    # User 
    path('users/',views.users, name='users'),
    path('user-details/<int:id>/',views.userDetails, name='userDetails'),

    #Transaction History
    path('transaction/',views.transaction, name='transaction'),
    path('withdraw-request/',views.withdrawRequest, name='withdrawRequest'),
    path('make-withdraw/<int:id>/<str:status>',views.makeWithdraw, name='makeWithdraw'),
    

    # Bidding History 
    path('bidding-history/',views.biddingHistory, name='biddingHistory'),
    path('bidding-result-history/',views.biddingResultHistory, name='biddingResultHistory'),

    # Jodi Bidding History 
    path('jodi-bidding-history/',views.jodiBiddingHistory, name='jodiBiddingHistory'),
    path('jodi-win-bidding-result-history/',views.jodiWinBiddingResultHistory, name='jodiWinBiddingResultHistory'),

    # Brokers Management 
    path('brokers/',views.brokers, name='brokers'),
    path('broker-details/<int:id>/',views.brokerDetails, name='brokerDetails'),

    # Brokers withdraw Management
    path('broker-withdraw-request/',views.brokerWithdrawRequest, name='brokerWithdrawRequest'),
    path('make-broker-withdraw/<int:id>/<str:status>',views.makeBrokerWithdraw, name='makeBrokerWithdraw'),


    # Result Panel Chart   resultPanelJodiMarket
    path('result-panel-reguler-market/',views.resultPanelRegulerMarket, name='resultPanelRegulerMarket'),
    path('add-result-chart/<int:id>/',views.addResultChart, name='addResultChart'),
    path('add-result-reguler-market/',views.addResultRegulerMarket, name='addResultRegulerMarket'),

    # Jodi Result Panel Chart   
    path('result-panel-jodi-market/',views.resultPanelJodiMarket, name='resultPanelJodiMarket'),
    path('add-jodi-result-chart/<int:id>/',views.addJodiResultChart, name='addJodiResultChart'),
    path('add-result-jodi-market/',views.addResultJodiMarket, name='addResultJodiMarket'),


    path('products/',views.productsList, name='productsList'),
    path('add-new-product/',views.addNewProduct, name='addNewProduct'),
    path('update-product/<int:id>/',views.updateProduct, name='updateProduct'),
    path('delete-product/<int:id>/',views.deletProduct, name='deletProduct'),

    
    

    
    ]