from datetime import timedelta
from django.shortcuts import redirect
from django.utils import timezone
from Auth.models import PasswordReset


class CheckLoginMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return super().dispatch(request, *args, **kwargs)


class CheckPasswordResetExpirationMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.session.has_key('reset_password_code'):
            reset_password = PasswordReset.objects.filter(code=request.session['reset_password_code']).first()
            if reset_password:
                today = timezone.now()
                expiration = reset_password.created_at + timedelta(minutes=15)
                if today < expiration:
                    return super().dispatch(request, *args, **kwargs)

        del request.session['reset_password_code']
        return redirect('/')