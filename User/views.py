from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy

from Subscription.models import Type
from .forms import *
from django.views.generic import ListView, DeleteView
from django.views import View
from django.shortcuts import get_object_or_404
from django.conf import settings


class UsersList(ListView):
    model = User
    context_object_name = 'users'
    paginate_by = settings.PAGINATION_NUMBER
    ordering = ['-date_joined']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['subscriptions'] = Type.objects.all()
        return context

    def get_template_names(self):
        template_name = 'Admin/Users/index.html'
        if self.request.is_ajax():
            template_name = 'Admin/Users/partials/list.html'
        return template_name

    def get_queryset(self):
        search_word = self.request.GET.get('search')
        limit = self.request.GET.get('limit')

        object_list = self.model.objects.all()

        if search_word:
            object_list = object_list.filter(phone__icontains=search_word)

        if limit:
            self.paginate_by = int(self.request.GET.get('limit'))
        return object_list


class UsersCreate(View):
    def get(self, request, *args, **kwargs):
        context = {
            'form': UserForm()
        }
        return render(request, 'Admin/Users/create.html', context)

    def post(self, request, *args, **kwargs):
        form = UserForm(data=request.POST or None, type='CREATE')

        if form.is_valid():
            user = User.objects.create(phone=form.cleaned_data.get('phone'),
                                       is_superuser=form.cleaned_data.get('is_superuser'))
            user.set_password(form.cleaned_data.get('password'))
            user.save()

            messages.success(request, 'کاربر مورد نظر با موفقیت ثبت شد.')
            return redirect(reverse_lazy('users'))

        else:
            context = {
                'form': form
            }
            return render(request, 'Admin/Users/create.html', context)


class UsersUpdate(View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = UserForm(initial={'phone': user.phone, 'is_superuser': user.is_superuser})
        context = {
            'form': form,
            'user_id': user.id
        }

        return render(request, 'Admin/Users/edit.html', context)

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = UserForm(data=request.POST or None, type='EDIT', user=user)

        if form.is_valid():
            user.phone = form.cleaned_data.get('phone')
            user.is_superuser = form.cleaned_data.get('is_superuser')

            if form.cleaned_data.get('password'):
                user.set_password(form.cleaned_data.get('password'))
            user.save()

            messages.success(request, 'کاربر مورد نظر با موفقیت ویرایش شد.')
            return redirect(reverse_lazy('users'))

        else:
            context = {
                'form': form,
                'user_id': user.id
            }
            return render(request, 'Admin/Users/edit.html', context)


class UsersDelete(DeleteView):
    model = User
    template_name = 'Admin/Users/delete.html'
    success_url = reverse_lazy('users')

    def dispatch(self, *args, **kwargs):
        resp = super(UsersDelete, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            return JsonResponse({'status': 'OK'}, safe=False)
        else:
            return resp
