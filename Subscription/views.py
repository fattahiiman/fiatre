from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View

from .forms import *
from .models import *
from django.views.generic import ListView, DeleteView, CreateView, UpdateView
from django.conf import settings


## Subscriptions_Types ##

class Subscriptions_Types_List(ListView):
    model = Type
    context_object_name = 'types'
    paginate_by = settings.PAGINATION_NUMBER
    ordering = ['-created_at']

    def get_template_names(self):
        template_name = 'Admin/Subscriptions_Types/index.html'
        if self.request.is_ajax():
            template_name = 'Admin/Subscriptions_Types/partials/list.html'
        return template_name

    def get_queryset(self):
        search_word = self.request.GET.get('search')
        limit = self.request.GET.get('limit')

        object_list = self.model.objects.all()

        if search_word:
            object_list = object_list.filter(name__icontains=search_word)

        if limit:
            self.paginate_by = int(self.request.GET.get('limit'))
        return object_list


class Subscriptions_Types_Create(CreateView):
    model = Type
    template_name = 'Admin/Subscriptions_Types/create.html'
    form_class = SubscriptionTypeForm
    success_url = reverse_lazy('types')

    def post(self, request, *args, **kwargs):
        messages.success(request, 'اشتراک مورد نظر با موفقیت ثبت شد.')
        return super().post(request, args, kwargs)


class Subscriptions_Types_Update(UpdateView):
    model = Type
    form_class = SubscriptionTypeForm
    template_name = 'Admin/Subscriptions_Types/edit.html'
    success_url = reverse_lazy('types')

    def post(self, request, *args, **kwargs):
        messages.success(request, 'اشتراک مورد نظر با موفقیت ویرایش شد.')
        return super().post(request, args, kwargs)


class Subscriptions_Types_Delete(DeleteView):
    model = Type
    template_name = 'Admin/Subscriptions_Types/delete.html'
    success_url = reverse_lazy('types')

    def dispatch(self, *args, **kwargs):
        resp = super(Subscriptions_Types_Delete, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            return JsonResponse({'status': 'OK'}, safe=False)
        else:
            return resp


###########################################################################################################

## Subscriptions_Users ##

class Subscriptions_Create(CreateView):
    model = Subscription
    template_name = 'Admin/Subscriptions/create.html'
    form_class = SubscriptionForm
    success_url = reverse_lazy('users')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.GET.get('phone'):
            form.initial = { 'user' : User.objects.get(phone=self.request.GET.get('phone')) }
        return form

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['users'] = User.objects.all()
        data['types'] = Type.objects.all()
        return data

    def post(self, request, *args, **kwargs):
        messages.success(request, 'اشتراک مورد نظر با موفقیت به کاربر الحالق شد.')
        return super().post(request, args, kwargs)


class Subscriptions_Update(UpdateView):
    model = Subscription
    form_class = SubscriptionForm
    template_name = 'Admin/Subscriptions/edit.html'
    success_url = reverse_lazy('users')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['users'] = User.objects.all()
        data['types'] = Type.objects.all()
        return data

    def post(self, request, *args, **kwargs):
        messages.success(request, 'اشتراک کاربر مورد نظر با موفقیت ویرایش شد.')
        return super().post(request, args, kwargs)


class Subscriptions_Delete(DeleteView):
    model = Subscription
    template_name = 'Admin/Subscriptions/delete.html'
    success_url = reverse_lazy('users')

    def dispatch(self, *args, **kwargs):
        resp = super(Subscriptions_Delete, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            return JsonResponse({'status': 'OK'}, safe=False)
        else:
            return resp
