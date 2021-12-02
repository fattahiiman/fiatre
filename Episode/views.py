from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from .models import *
from .forms import *
from django.conf import settings
from django.views.generic import ListView, DeleteView, CreateView, UpdateView
from django.views import View


class EpisodesList(ListView):
    model = Episode
    context_object_name = 'episodes'
    paginate_by = settings.PAGINATION_NUMBER
    ordering = ['-created_at']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.objects.all()
        return context

    def get_template_names(self):
        template_name = 'Admin/Episodes/index.html'
        if self.request.is_ajax():
            template_name = 'Admin/Episodes/partials/list.html'
        return template_name

    def get_queryset(self):
        search_word = self.request.GET.get('search')
        limit = self.request.GET.get('limit')
        category = self.request.GET.get('category')

        object_list = self.model.objects.all()

        if category:
            object_list = object_list.filter(category__slug=category)

        if search_word:
            object_list = object_list.filter(title__icontains=search_word)

        if limit:
            self.paginate_by = int(self.request.GET.get('limit'))
        return object_list


class EpisodesCreate(CreateView):
    model = Episode
    template_name = 'Admin/Episodes/create.html'
    form_class = EpisodeForm
    success_url = reverse_lazy('episodes')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['categories'] = Category.objects.all()
        return data

    def post(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.POST['slug'] = slugify(request.POST['slug'] , allow_unicode=True)

        messages.success(request, 'ویدیو مورد نظر با موفقیت ثبت شد.')
        return super().post(request, args, kwargs)


class EpisodesUpdate(UpdateView):
    model = Episode
    form_class = EpisodeForm
    template_name = 'Admin/Episodes/edit.html'
    success_url = reverse_lazy('episodes')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['categories'] = Category.objects.all()
        return data

    def post(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.POST['slug'] = slugify(request.POST['slug'] , allow_unicode=True)

        messages.success(request, 'ویدیو مورد نظر با موفقیت ویرایش شد.')
        return super().post(request, args, kwargs)


class EpisodesDelete(DeleteView):
    model = Episode
    template_name = 'Admin/Episodes/delete.html'
    success_url = reverse_lazy('episodes')

    def dispatch(self, *args, **kwargs):
        resp = super(EpisodesDelete, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            return JsonResponse({'status': 'OK'}, safe=False)
        else:
            return resp

#####################################################################

class DeleteEpisodeVideo(View):
    def delete(self, request, pk):
        episode = get_object_or_404(Episode, pk=pk)
        episode.video.delete(save=True)

    def dispatch(self, *args, **kwargs):
        resp = super(DeleteEpisodeVideo, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            return JsonResponse({'status': 'OK'}, safe=False)
        else:
            return resp
