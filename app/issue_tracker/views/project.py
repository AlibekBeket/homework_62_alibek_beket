from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from issue_tracker.models import Project

from issue_tracker.forms import ProjectForm, ProjectUserForm


class ProjectListView(ListView):
    template_name = 'project_list_page.html'
    model = Project
    context_object_name = 'projects'
    ordering = ('start_date')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['projects'] = Project.objects.filter(is_deleted=False)
        return context


class ProjectAddView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    template_name = 'project_create_page.html'
    model = Project
    form_class = ProjectForm
    groups = ['Project Manager']
    permission_required = 'project.change_project'

    def get_success_url(self):
        return reverse('projects_list')

    def test_func(self):
        return self.request.user.groups.filter(name__in=self.groups).exists()


class ProjectDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    template_name = 'project_delete_page.html'
    model = Project
    success_url = reverse_lazy('projects_list')
    groups = ['Project Manager']
    permission_required = 'project.change_project'

    def test_func(self):
        return self.request.user.groups.filter(name__in=self.groups).exists()


class ProjectUserUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    template_name = 'project_user_update_page.html'
    model = Project
    form_class = ProjectUserForm
    groups = ['Project Manager', 'Team Lead']
    permission_required = 'project.change_user'

    def get_success_url(self):
        return reverse('projects_list')

    def test_func(self):
        return self.request.user.groups.filter(
            name__in=self.groups).exists() and self.request.user in self.get_object().user.all()
