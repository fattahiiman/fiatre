from django.urls import path , include
from .views import *

urlpatterns = [
    path('login/' , Login.as_view() , name='login'),
    path('logout/' , Logout.as_view() , name='logout'),
    path('register/' , Register.as_view() , name='register'),

    path('password/reset/' , ResetPasswordView.as_view() , name='password-reset'),
    path('password/reset/confirm/' , ResetPasswordConfirmView.as_view() , name='password-reset-confirm'),
    path('password/reset/enter/' , ResetPasswordEnterView.as_view() , name='password-reset-enter'),

    path('login/code/', LoginCodeView.as_view(), name='login-code'),
    path('login/code/confirm/', LoginCodeConfirmView.as_view(), name='login-code-confirm'),
]
