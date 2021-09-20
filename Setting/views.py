from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import *
from .forms import *


class SettingsList(ListView):
    model = Setting
    context_object_name = 'settings'
    paginate_by = settings.PAGINATION_NUMBER
    ordering = ['-created_at']

    def get_template_names(self):
        template_name = 'Admin/Settings/index.html'
        if self.request.is_ajax():
            template_name = 'Admin/Settings/partials/list.html'
        return template_name

    def get_queryset(self):
        search_word = self.request.GET.get('search')
        limit = self.request.GET.get('limit')

        object_list = self.model.objects.all()

        if search_word:
            object_list = object_list.filter(key__icontains=search_word)

        if limit:
            self.paginate_by = int(self.request.GET.get('limit'))

        return object_list


class SettingsCreate(CreateView):
    model = Setting
    form_class = SettingForm
    template_name = 'Admin/Settings/create.html'
    success_url = reverse_lazy('settings')

    def post(self, request, *args, **kwargs):
        messages.success(request, 'تنظیمات مورد نظر با موفقیت ثبت شد.')
        return super().post(request, args, kwargs)


class SettingsUpdate(UpdateView):
    model = Setting
    form_class = SettingForm
    template_name = 'Admin/Settings/edit.html'
    success_url = reverse_lazy('settings')

    def post(self, request, *args, **kwargs):
        messages.success(request, 'تنظیمات مورد نظر با موفقیت ویرایش شد.')
        return super().post(request, args, kwargs)


class SettingsDelete(DeleteView):
    model = Setting
    template_name = 'Admin/Settings/delete.html'
    success_url = reverse_lazy('settings')

    def dispatch(self, *args, **kwargs):
        resp = super(SettingsDelete, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            return JsonResponse({'status': 'OK'}, safe=False)
        else:
            return resp
