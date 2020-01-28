from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from services import models
from datetime import datetime, timedelta
from django.utils import timezone


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'services/index.html'
    model = models.Post
    paginate_by = 25
    extra_context = {
        'list_header': 'Last 24 hours:',
    }

    def get_queryset(self):
        services_qs = self.request.user.services.filter(active=True)
        yesterday = timezone.now() - timedelta(1)
        queryset = models.Post.objects\
            .filter(service_id__in=services_qs, timestamp__gte=yesterday)

        return queryset


class ServiceView(LoginRequiredMixin, ListView):
    template_name = 'services/list.html'
    model = models.Post
    paginate_by = 25

    def get_queryset(self):
        service = get_object_or_404(
            models.Service,
            user=self.request.user,
            pk=self.kwargs.get('pk')
        )
        self.extra_context = {
            'list_header': service.name,
        }

        queryset = models.Post.objects.filter(service=service)

        return queryset


class LogsView(LoginRequiredMixin, ListView):
    template_name = 'services/logs.html'
    model = models.ScraperRunLog
    paginate_by = 25
    ordering = ['-timestamp_start']
    context_object_name = 'log_list'


class ServiceCreateView(LoginRequiredMixin, CreateView):
    model = models.Service
    fields = ['name', 'url', 'scraper', 'active']

    def form_valid(self, form):
        # set instance's user field to currently logged in user
        form.instance.user = self.request.user
        return super().form_valid(form)
