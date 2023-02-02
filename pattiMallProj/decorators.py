from functools import wraps
from django.http import HttpResponseRedirect, HttpResponse
from dashboard.models import Market, JodiMarket, Games, Customer, BiddingHistory, JodiBiddingHistory, Withdraw, Transaction, Notifications,BankAccount, Partner, PartnerUser
from django.contrib.auth import logout
from django.contrib import messages

def check_broker_account():
    def decorator(view_func):
        @wraps(view_func)
        def _is_logged_in(request, *args, **kwargs):
            if request.user.is_authenticated:
                if Partner.objects.filter(user_id = request.user.id).exists():
                    return view_func(request, *args, **kwargs)
                else:
                    logout(request)
                    messages.success(request, 'Yor are not authorised to access broker panel, Please contact with admin')
                    return HttpResponseRedirect('/partner/partner-login')

            else:
                return view_func(request, *args, **kwargs)
        return _is_logged_in
    return decorator