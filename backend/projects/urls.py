from django.urls import path

from projects.views import DashboardView
from projects.views.board_columns import (
    APIBoardColumnCreateView,
    APIBoardColumnDeleteView,
    APIBoardColumnModifyView,
)
from projects.views.boards import (
    BoardView,
    APIBoardCreateView,
    APIBoardDeleteView,
    APIBoardModifyView,
)
from projects.views.project_members import (
    APIProjectMemberCreateView,
    APIProjectMemberDeleteView,
    APIProjectMemberEvaluateView,
    APIProjectMemberModifyView,
)
from projects.views.projects import (
    ProjectView,
    ProjectListView,
    APIProjectCreateView,
    APIProjectDeleteView,
    APIProjectModifyView,
)
from projects.views.tasks import (
    APITaskArchiveView,
    APITaskCreateView,
    APITaskDeleteView,
    APITaskModifyView,
    APITaskRestoreView,
)
from projects.views.tasks.comments import (
    APITaskCommentCreateView,
    APITaskCommentListView,
)

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('projects/<int:project_pk>/', ProjectView.as_view(), name='project'),
    path('projects/<int:project_pk>/boards/<int:pk>/', BoardView.as_view(), name='board'),
    path('projects/', ProjectListView.as_view(), name='projects'),
    path(
        'api/projects/create/',
        APIProjectCreateView.as_view(),
        name='api-project-create',
    ),
    path(
        'api/projects/<int:project_pk>/delete/',
        APIProjectDeleteView.as_view(),
        name='api-project-delete',
    ),
    path(
        'api/projects/<int:project_pk>/modify/',
        APIProjectModifyView.as_view(),
        name='api-project-modify',
    ),
    path(
        'api/projects/<int:project_pk>/members/create/',
        APIProjectMemberCreateView.as_view(),
        name='api-project-member-create',
    ),
    path(
        'api/projects/<int:project_pk>/members/<int:pk>/delete/',
        APIProjectMemberDeleteView.as_view(),
        name='api-project-member-delete',
    ),
    path(
        'api/projects/<int:project_pk>/members/<int:pk>/evaluate/',
        APIProjectMemberEvaluateView.as_view(),
        name='api-project-member-evaluate',
    ),
    path(
        'api/projects/<int:project_pk>/members/<int:pk>/modify/',
        APIProjectMemberModifyView.as_view(),
        name='api-project-member-modify',
    ),
    path(
        'api/projects/<int:project_pk>/boards/create/',
        APIBoardCreateView.as_view(),
        name='api-board-create',
    ),
    path(
        'api/projects/<int:project_pk>/boards/<int:pk>/delete/',
        APIBoardDeleteView.as_view(),
        name='api-board-delete',
    ),
    path(
        'api/projects/<int:project_pk>/boards/<int:pk>/modify/',
        APIBoardModifyView.as_view(),
        name='api-board-modify',
    ),
    path(
        'api/projects/<int:project_pk>/boards/<int:board_pk>/columns/create/',
        APIBoardColumnCreateView.as_view(),
        name='api-board-column-create',
    ),
    path(
        'api/projects/<int:project_pk>/boards/<int:board_pk>/columns/<int:pk>/delete/',
        APIBoardColumnDeleteView.as_view(),
        name='api-board-column-delete',
    ),
    path(
        'api/projects/<int:project_pk>/boards/<int:board_pk>/columns/<int:pk>/modify/',
        APIBoardColumnModifyView.as_view(),
        name='api-board-column-modify',
    ),
    path(
        'api/projects/<int:project_pk>/boards/<int:board_pk>/tasks/create/',
        APITaskCreateView.as_view(),
        name='api-task-create',
    ),
    path(
        'api/projects/<int:project_pk>/boards/<int:board_pk>/tasks/<int:pk>/delete/',
        APITaskDeleteView.as_view(),
        name='api-task-delete',
    ),
    path(
        'api/projects/<int:project_pk>/boards/<int:board_pk>/tasks/<int:pk>/modify/',
        APITaskModifyView.as_view(),
        name='api-task-modify',
    ),
    path(
        'api/projects/<int:project_pk>/boards/<int:board_pk>/tasks/<int:pk>/archive/',
        APITaskArchiveView.as_view(),
        name='api-task-archive',
    ),
    path(
        'api/projects/<int:project_pk>/boards/<int:board_pk>/tasks/<int:pk>/restore/',
        APITaskRestoreView.as_view(),
        name='api-task-restore',
    ),
    path(
        'api/projects/<int:project_pk>/boards/<int:board_pk>/tasks/<int:task_pk>/comments/',
        APITaskCommentListView.as_view(),
        name='api-task-comment-list',
    ),
    path(
        'api/projects/<int:project_pk>/boards/<int:board_pk>/tasks/<int:task_pk>/comments/create/',
        APITaskCommentCreateView.as_view(),
        name='api-task-comment-create',
    ),
]
