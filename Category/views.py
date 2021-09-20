from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.template.defaultfilters import slugify
from .forms import *
from .models import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


class CategoriesList(ListView):
    model = Category
    context_object_name = 'categories'
    paginate_by = settings.PAGINATION_NUMBER
    ordering = ['-created_at']

    def get_template_names(self):
        template_name = 'Admin/Categories/index.html'
        if self.request.is_ajax():
            template_name = 'Admin/Categories/partials/list.html'
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


class CategoriesCreate(CreateView):
    model = Category
    template_name = 'Admin/Categories/create.html'
    form_class = CategoryForm
    success_url = reverse_lazy('categories')

    def post(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.POST['slug'] = slugify(request.POST['slug'], allow_unicode=True)

        messages.success(request, 'دسته بندی مورد نظر با موفقیت ثبت شد.')
        return super().post(request, args, kwargs)


class CategoriesUpdate(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'Admin/Categories/edit.html'
    success_url = reverse_lazy('categories')

    def post(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.POST['slug'] = slugify(request.POST['slug'], allow_unicode=True)

        messages.success(request, 'دسته بندی مورد نظر با موفقیت ویرایش شد.')
        return super().post(request, args, kwargs)


class CategoriesDelete(DeleteView):
    model = Category
    template_name = 'Admin/Categories/delete.html'
    success_url = reverse_lazy('categories')

    def dispatch(self, *args, **kwargs):
        resp = super(CategoriesDelete, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            return JsonResponse({'status': 'OK'}, safe=False)
        else:
            return resp
