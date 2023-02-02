from django.urls import path
from .import views

urlpatterns = [


    path('paytmweb/',views.paytmweb, name='paytmweb'),
    path('handlerequestweb/',views.handlerequestweb, name='handlerequestweb'),
    path('payment-success-web/<str:successPaymentId>',views.paymentSuccessWeb, name='paymentSuccessWeb'),

    path('',views.home, name='home'),
    path('about-us/',views.aboutUs, name='aboutUs'),
    path('term-of-services/',views.termServices, name='termServices'),
    path('refund-policy/',views.refundPolicy, name='refundPolicy'),
    path('privacy-policy/',views.privacyPolicy, name='privacyPolicy'),

    path('upload-apk/',views.uploadApk, name='uploadApk'),
    path('make-upload-apk/',views.makeUpload, name='makeUpload'),
    
    path('place-order/',views.placeOrder, name='placeOrder'),

    
    path('result-panel/',views.resultPanel, name='resultPanel'),
    path('result-panel-chart/<int:id>',views.resultPanelChart, name='resultPanelChart'),

]