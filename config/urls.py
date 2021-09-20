"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('django_admin/', admin.site.urls),

    ## Front ##
    path('', include('Front.urls')),
    path('', include('Auth.urls')),
    path('subscriptions/', include('Gateway.urls')),

    ## Admin Panel ##
    path('admin/', include('Admin.urls')),
    path('admin/users/', include('User.urls')),
    path('admin/categories/', include('Category.urls')),
    path('admin/episodes/', include('Episode.urls')),
    path('admin/subscriptions/', include('Subscription.urls')),
    path('admin/settings/', include('Setting.urls')),
    path('admin/coupons/', include('Coupon.urls')),
]


urlpatterns +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)