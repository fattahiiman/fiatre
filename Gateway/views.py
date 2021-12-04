from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.views.decorators.http import require_http_methods
from zeep import Client
from Subscription.models import Subscription, Type
from Coupon.models import Coupon, CouponUser
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.http import Http404
import jdatetime
from django.conf import settings

########################################################################

def DeleteLastData(request):
    try:
        request.session.pop('payment_amount')
        request.session.pop('coupon_price')
        request.session.pop('coupon')
    except:
        pass


def CheckSubscriptionAmount(amount, subscription, coupon_price):
    if subscription.type.price - coupon_price != amount:
        return False
    return True


def Delete_User_Active_Subscription(user):
    subscription = Subscription.objects.filter(user=user, status=True)
    subscription.delete()


def Delete_User_DeActive_Subscription(user):
    subscription = Subscription.objects.filter(user=user, status=False)
    subscription.delete()


def CheckCoupon(code, request):
    if code:
        if code == request.session.get('coupon', None):
            coupon = Coupon.objects.filter(code=code).first()
            if coupon:
                today = timezone.now()
                expiration = coupon.created_at + relativedelta(months=coupon.time)
                if today <= expiration:
                    return coupon

    return None


def CalculateCouponAmount(coupon_percent, price):
    percent_amount = (price * coupon_percent) / 100
    NewPrice = price - percent_amount
    return round(NewPrice)


#############  Buy Subcription and Special Account #####################

MERCHANT = settings.MERCHANT_CODE
# client = Client('https://sandbox.zarinpal.com/pg/services/WebGate/wsdl')
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
amount = 0  # Toman / Required
description = "خرید اشتراک ویژه سایت فیاتر"  # Required
email = settings.EMAIL_ADDRESS  # Optional
mobile = settings.MOBILE_NUMBER  # Optional
CallbackURL = settings.URL + '/subscriptions/buy/verify/'  # Important: need to edit for realy server.


@login_required(login_url='/login')
@require_http_methods(["POST"])
def pay(request):
    type = get_object_or_404(Type, slug=request.POST.get('type_slug', 0))

    DeleteLastData(request)

    Subscription.objects.create(type=type, user=request.user, status=False)
    total_amount = type.price

    coupon = CheckCoupon(request.POST.get('coupon'), request)
    if coupon:
        total_amount = CalculateCouponAmount(coupon.percent, total_amount)
        request.session['coupon_price'] = (type.price * coupon.percent) / 100
        request.session['coupon'] = coupon.id

    if total_amount == 0:
        return redirect('/')

    request.session['payment_amount'] = total_amount

    result = client.service.PaymentRequest(MERCHANT, total_amount, description, email, mobile, CallbackURL)
    if result.Status == 100:
        # return redirect('https://sandbox.zarinpal.com/pg/StartPay/' + str(result.Authority))
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status))


@login_required(login_url='/login')
def verify(request):
    subscription = Subscription.objects.filter(status=False, user=request.user).last()
    if not subscription:
        raise Http404

    amount = int(request.session.get('payment_amount', 0))
    coupon_price = int(request.session.get('coupon_price', 0))
    coupon = int(request.session.get('coupon', 0))

    context = {}
    context['type_name'] = subscription.type.name

    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            if amount > 0 and CheckSubscriptionAmount(amount, subscription, coupon_price):
                Delete_User_Active_Subscription(request.user)

                subscription.status = True
                subscription.save()

                if coupon:
                    CouponUser.objects.create(user=request.user , coupon_id=coupon)

                Delete_User_DeActive_Subscription(request.user)
                DeleteLastData(request)

                context['ref_code'] = result.RefID
                context['expiration_date'] = jdatetime.datetime.fromgregorian(
                    datetime=subscription.type.created_at + relativedelta(months=subscription.type.time))

                return render(request, 'Front/Gateway/payment_success.html', context)

    Delete_User_DeActive_Subscription(request.user)
    return render(request, 'Front/Gateway/payment_error.html', context)
