from django.urls import path
from .views import *

urlpatterns = [
    path('' , Index.as_view() , name='index'),
    path('about/' , About_us.as_view() , name='about_us'),
    path('terms/' , Terms.as_view() , name='terms'),
    path('faq/' , Faq.as_view() , name='faq'),
    path('categories/<slug>/' , Cat.as_view() , name='category'),
    path('episodes/<slug>/' , EpisodeDetail.as_view() , name='episode'),
    path('episodes/increase/view_count/<slug>/' , EpisodesViewCountIncreaseView.as_view() , name='episode-increase-view'),

    path('account/' , Account.as_view() , name='account'),

    ## Subscription ##
    path('subscription/plans/' , SubscriptionPlans.as_view() , name='subscription-plans'),
    path('subscription/buy/<slug>/' , SubscriptionBuy.as_view() , name='subscription-buy'),
    path('subscription/coupon/check/' , SubscriptionCheckCoupon.as_view() , name='subscription-coupon-check'),

    ## User Watchinh ##
    path('watching/status/' , WatchingStatusChangeView.as_view() , name='watching-status-change-view'),
]
