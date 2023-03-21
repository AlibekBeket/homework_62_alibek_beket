from django.urls import path

from issue_tracker.views.issue_tracker import IssueTrackerView, IssueDetailView, IssueUpdateView, IssueAddView, \
    IssueDeleteView

from issue_tracker.views.project import ProjectListView, ProjectAddView, ProjectDeleteView, ProjectUserUpdateView

urlpatterns = [
    path('', ProjectListView.as_view()),
    path('project/', ProjectListView.as_view(), name='projects_list'),
    path('project/add', ProjectAddView.as_view(), name='project_add'),
    path('project/<int:project_pk>', IssueTrackerView.as_view(), name='project_detail'),
    path('project/<int:pk>/delete', ProjectDeleteView.as_view(), name='project_delete'),
    path('project/<int:pk>/user_update', ProjectUserUpdateView.as_view(), name='project_user_update'),
    path('project/<int:project_pk>/add', IssueAddView.as_view(), name='project_issue_add'),
    path('project/<int:project_pk>/<int:pk>', IssueDetailView.as_view(), name='project_issue_detail'),
    path('project/<int:project_pk>/<int:pk>/delete', IssueDeleteView.as_view(), name='project_issue_delete'),
    path('project/<int:project_pk>/<int:pk>/update', IssueUpdateView.as_view(), name='project_issue_update'),
]
