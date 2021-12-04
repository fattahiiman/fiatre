from django.conf import settings
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import *
from .forms import *


class CouponsList(ListView):
    model = Coupon
    context_object_name = 'coupons'
    paginate_by = settings.PAGINATION_NUMBER
    ordering = ['-created_at']

    def get_template_names(self):
        template_name = 'Admin/Coupons/index.html'
        if self.request.is_ajax():
            template_name = 'Admin/Coupons/partials/list.html'
        return template_name

    def get_queryset(self):
        search_word = self.request.GET.get('search')
        limit = self.request.GET.get('limit')

        object_list = self.model.objects.all()

        if search_word:
            object_list = object_list.filter(code__icontains=search_word)

        if limit:
            self.paginate_by = int(self.request.GET.get('limit'))
        return object_list

class CouponsCreate(CreateView):
    model = Coupon
    form_class = CouponForm
    template_name = 'Admin/Coupons/create.html'
    success_url = reverse_lazy('coupons')

    def post(self, request, *args, **kwargs):
        messages.success(request, 'کد تخفیف مورد نظر مورد نظر با موفقیت ثبت شد.')
        return super().post(request, args, kwargs)

class CouponsUpdate(UpdateView):
    model = Coupon
    form_class = CouponForm
    template_name = 'Admin/Coupons/edit.html'
    success_url = reverse_lazy('coupons')

    def post(self, request, *args, **kwargs):
        messages.success(request, 'کد تخفیف مورد نظر با موفقیت ویرایش شد.')
        return super().post(request, args, kwargs)

class CouponsDelete(DeleteView):
    model = Coupon
    template_name = 'Admin/Coupons/delete.html'
    success_url = reverse_lazy('coupons')

    def dispatch(self, *args, **kwargs):
        resp = super(CouponsDelete, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            return JsonResponse({'status': 'OK'}, safe=False)
        else:
            return resp

##########################################################

class CouponUserList(ListView):
    model = CouponUser
    context_object_name = 'coupon_users'
    paginate_by = settings.PAGINATION_NUMBER
    ordering = ['-created_at']

    def get_template_names(self):
        template_name = 'Admin/Coupon_Users/index.html'
        if self.request.is_ajax():
            template_name = 'Admin/Coupon_Users/partials/list.html'
        return template_name

    def get_queryset(self):
        coupon = self.request.GET.get('coupon')
        search_word = self.request.GET.get('search')
        limit = self.request.GET.get('limit')

        object_list = self.model.objects.all()

        if coupon:
            object_list = object_list.filter(coupon__id=coupon)

        if search_word:
            q = Q(user__phone__icontains=search_word) | Q(coupon__code__icontains=search_word)
            object_list = object_list.filter(q)

        if limit:
            self.paginate_by = int(self.request.GET.get('limit'))
        return object_list