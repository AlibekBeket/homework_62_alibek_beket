from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.views.generic import TemplateView, ListView, UpdateView, DetailView, DeleteView, CreateView
from issue_tracker.models import Issue, Status, Type, Project

from issue_tracker.forms import IssueForm

from issue_tracker.forms import SearchForm


class IssueTrackerView(ListView):
    template_name = 'issue_tracker_list_page.html'
    model = Issue
    context_object_name = 'issues'
    ordering = ('created_at')
    paginate_by = 10
    paginate_orphans = 1

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        self.project_pk = kwargs['project_pk']
        return super().get(request, *args, **kwargs)

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None

    def get_queryset(self):
        queryset = super().get_queryset().filter(project=self.project_pk)
        if self.search_value:
            query = Q(summary__icontains=self.search_value) | Q(description__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        context['project'] = Project.objects.get(id=self.project_pk)
        if self.search_value:
            context['query']: urlencode({'search': self.search_value})
        if len(context.get('issues')) == 0:
            context['404_error'] = True
        return context


class IssueDetailView(DetailView):
    template_name = 'issue_detail_page.html'
    model = Issue


class IssueUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    template_name = 'issue_update_page.html'
    form_class = IssueForm
    model = Issue
    groups = ['Project Manager', 'Team Lead', 'Developer']
    permission_required = 'issue_tracker.change_issue'

    def get_success_url(self):
        return reverse('project_issue_detail', kwargs={'project_pk': self.object.project.pk, 'pk': self.object.pk})

    def test_func(self):
        return self.request.user.groups.filter(
            name__in=self.groups).exists() and self.request.user in Project.objects.get(
            id=self.kwargs['project_pk']).user.all()


class IssueAddView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    template_name = 'issue_create_page.html'
    model = Issue
    form_class = IssueForm
    groups = ['Project Manager', 'Team Lead', 'Developer']
    permission_required = 'issue_tracker.change_issue'

    def get(self, request, *args, **kwargs):
        self.project_pk = kwargs['project_pk']
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(id=self.project_pk)
        return context

    def get_success_url(self):
        return reverse('project_issue_detail', kwargs={'project_pk': self.object.project.pk, 'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save()
            issue.project = Project.objects.get(id=kwargs['project_pk'])
            issue.save()
            return redirect(reverse('project_issue_detail', kwargs={'project_pk': issue.project.pk, 'pk': issue.pk}))
        return render(request, 'issue_create_page.html',
                      context={'form': form, 'project': Project.objects.get(id=kwargs['project_pk'])})

    def test_func(self):
        return self.request.user.groups.filter(
            name__in=self.groups).exists() and self.request.user in Project.objects.get(
            id=self.kwargs['project_pk']).user.all()


class IssueDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    template_name = 'issue_delete_page.html'
    model = Issue
    groups = ['Project Manager', 'Team Lead']
    permission_required = 'issue_tracker.change_issue'

    def get_success_url(self):
        return reverse('project_detail', kwargs={'project_pk': self.object.project.pk})

    def test_func(self):
        return self.request.user.groups.filter(
            name__in=self.groups).exists() and self.request.user in Project.objects.get(
            id=self.kwargs['project_pk']).user.all()
