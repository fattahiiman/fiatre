import random
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from .forms import *
from django.contrib import messages
from .mixins import *
from .models import *
from django.http import JsonResponse


def login_method(phone, password, remember_me, request):
    user = authenticate(phone=phone, password=password)
    if user:
        if remember_me:
            request.session.set_expiry(2419200)

        login(request, user)
        return [True, user]

    return [False, user]

################################################

class Register(CheckLoginMixin, View):
    def get(self, request):
        return render(request, 'Auth/register.html')

    def post(self, request):
        form = RegisterForm(data=request.POST or None)

        if form.is_valid():
            phone = form.cleaned_data.get('phone')
            password = form.cleaned_data.get('password').lower()
            remember_me = form.cleaned_data.get('remember_me')

            user = User.objects.create(phone=phone, is_active=1, is_superuser=0)
            user.set_password(password)
            user.save()

            status, user = login_method(phone, password, remember_me, request)
            if status:
                if request.is_ajax():
                    context = {
                        'message': 'ثبت نام شما با موفقیت انجام شد.',
                        'status': 'OK'
                    }
                    return JsonResponse(context, safe=False)
                else:
                    messages.success(request, 'ثبت نام شما با موفقیت انجام شد.')
                    return redirect('/')
            else:
                if request.is_ajax():
                    form.add_error('phone', 'مشکلی پیش آمده است! دوباره امتحان کنید.')
                    context = {
                        'errors': form.errors,
                        'status': 'Failed'
                    }
                    return JsonResponse(context, safe=False)
                else:
                    form.add_error('phone', 'مشکلی پیش آمده است! دوباره امتحان کنید.')
                    context = {
                        'form': form
                    }
                    return render(request, 'Auth/register.html', context)

        if request.is_ajax():
            context = {
                'errors': form.errors,
                'status': 'Failed'
            }
            return JsonResponse(context, safe=False)
        else:
            context = {
                'form': form
            }
            return render(request, 'Auth/register.html', context)



class Login(CheckLoginMixin, View):
    def get(self, request):
        return render(request, 'Auth/login.html')

    def post(self, request):
        form = LoginForm(data=request.POST or None)

        if form.is_valid():
            phone = form.cleaned_data.get('phone')
            password = form.cleaned_data.get('password').lower()
            remember_me = form.cleaned_data.get('remember_me')

            status, user = login_method(phone, password, remember_me, request)
            if status:
                next = '/'
                if request.GET.get('next'):
                    next = request.GET['next']

                elif user.is_superuser:
                    next = reverse_lazy('admin')

                return redirect(next)

            else:
                messages.error(request, 'شماره موبایل یا رمز عبور صحیح نمیباشد')

        context = {
            'form': form
        }
        return render(request, 'Auth/login.html', context)


class Logout(View):
    def post(self, request):
        logout(request)
        return redirect('/')


class ResetPasswordView(CheckLoginMixin, View):
    def get(self, request):
        return render(request, 'Auth/reset_password.html')

    def post(self, request):
        form = ResetPasswordForm(data=request.POST or None)

        if form.is_valid():
            phone = form.cleaned_data.get('phone')
            user = User.objects.filter(phone=phone).first()

            if user:
                if check_reset_password_sent(user):
                    code = ''.join([str(random.randint(0, 9)) for item in range(5)])

                    if user.sms_reset_password(user.phone, code):
                        PasswordReset.objects.create(code=code, user=user)
                        return redirect(reverse_lazy('password-reset-confirm'))

                    messages.error(request, 'خطایی هنگام ارسال پیامک بازیابی پیش آمده است! لطفا دوباره امتحان کنید.')

                else:
                    messages.error(request,
                                   'درخواست بازیابی رمز عبور برای شما ارسال شده است ، پس از گذشت 15 دقیقه میتوانید دوباره درخواست کنید')

            else:
                messages.error(request, 'کاربری با این شماره موبایل وجود ندارد!')

        context = {
            'form': form
        }
        return render(request, 'Auth/reset_password.html', context)


class ResetPasswordConfirmView(CheckLoginMixin, View):
    def get(self, request):
        return render(request, 'Auth/reset_password_confirm.html')

    def post(self, request):
        form = ResetPasswordConfirmForm(data=request.POST or None)

        if form.is_valid():
            code = form.cleaned_data.get('code')

            if check_reset_password_code_expiration(code):
                request.session['reset_password_code'] = code
                return redirect(reverse_lazy('password-reset-enter'))

            else:
                messages.error(request, 'کد وارد شده معتبر نیست!')

        context = {
            'form': form
        }
        return render(request, 'Auth/reset_password_confirm.html', context)


class ResetPasswordEnterView(CheckLoginMixin, CheckPasswordResetExpirationMixin, View):
    def get(self, request):
        return render(request, 'Auth/reset_password_enter.html')

    def post(self, request):
        form = ResetPasswordEnterForm(data=request.POST or None)

        if form.is_valid():
            if request.session.has_key('reset_password_code'):
                password = form.cleaned_data.get('password')
                code = request.session['reset_password_code']

                password_reset = PasswordReset.objects.filter(code=code).first()
                if password_reset:
                    user = password_reset.user
                    user.set_password(password)
                    user.save()

                    reset_password = user.password_resets.filter(is_used=False).last()
                    reset_password.is_used = True
                    reset_password.save()

                    messages.success(request, 'تغییر رمز عبور شما با موفقیت انجام شد . اکنون میتوانید وارد شوید.')
                    return redirect(reverse_lazy('login'))
            messages.error(request, 'زمان بازیابی رمز عبور منقضی شده است! ، دوباره درخواست کنید')

        context = {
            'form': form
        }
        return render(request, 'Auth/reset_password_enter.html', context)

########################################################################################################

## Login With Code ##
class LoginCodeView(CheckLoginMixin, View):
    def get(self, request):
        return render(request, 'Auth/login_with_code/login_code.html')

    def post(self, request):
        form = LoginCodeForm(data=request.POST or None)

        if form.is_valid():
            phone = form.cleaned_data.get('phone')
            user = User.objects.filter(phone=phone).first()

            if user:
                if check_login_code_sent(user):
                    code = ''.join([str(random.randint(0, 9)) for item in range(5)])

                    if user.sms_disposable_code(user.phone, code):
                        LoginCode.objects.create(code=code, user=user)
                        request.session['login_code_phone'] = user.phone
                        return redirect(reverse_lazy('login-code-confirm'))

                    messages.error(request, 'خطایی هنگام ارسال پیامک حاوی کد یکبار مصرف پیش آمده است! لطفا دوباره امتحان کنید.')

                else:
                    messages.error(request,
                                   'کد یکبار مصرف ورود برای شما ارسال شده است ، پس از گذشت 1 دقیقه میتوانید دوباره درخواست کنید')

            else:
                messages.error(request, 'کاربری با این شماره موبایل وجود ندارد!')

        context = {
            'form': form
        }
        return render(request, 'Auth/login_with_code/login_code.html', context)

class LoginCodeConfirmView(CheckLoginMixin, View):
    def get(self, request):
        return render(request, 'Auth/login_with_code/login_code_confirm.html')

    def post(self, request):
        form = LoginCodeConfirmForm(data=request.POST or None)

        if form.is_valid():
            code = form.cleaned_data.get('code')

            if check_login_code_code_expiration(code):
                phone = request.session['login_code_phone']
                user = get_object_or_404(User , phone=phone)
                status, user = login_method(user.phone, user.password, False, request)
                if status:
                    next = '/'
                    if request.GET.get('next'):
                        next = request.GET['next']

                    elif user.is_superuser:
                        next = reverse_lazy('admin')

                    return redirect(next)

            else:
                messages.error(request, 'کد وارد شده معتبر نیست!')

        context = {
            'form': form
        }
        return render(request, 'Auth/login_with_code/login_code_confirm.html', context)