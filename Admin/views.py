from django.shortcuts import render
from django.contrib.auth import get_user_model
from Episode.models import Episode
from Subscription.models import Subscription

User = get_user_model()

def admin_dashboard(request):
    subscriptions = Subscription.objects.all()
    subscriptions_total_amount = 0
    for item in subscriptions:
        subscriptions_total_amount += item.type.price

    context = {
        'users_count' : User.objects.count(),
        'videos_count' : Episode.objects.count(),
        'subscriptions_total_amount' : subscriptions_total_amount,
    }
    return render(request , 'Admin/admin-dashboard.html' , context)