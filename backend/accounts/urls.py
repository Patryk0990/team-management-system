from django.urls import path

from accounts.views import (
    IndexView,
    LogoutView
)
from accounts.views.users import (
    UserListView,
    APIUserCreateView,
    APIUserDeleteView,
    APIUserModifyView,
    CustomPasswordResetCompleteView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetDoneView,
    CustomPasswordResetView,
    EmailVerifyView,
    UserProfileView,
    UserModifyView,
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # Account related
    path('accounts/password-reset/', CustomPasswordResetView.as_view(), name='password-reset'),
    path('accounts/password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password-reset-done'),
    path('accounts/password-reset/<str:uidb64>/<str:token>/', CustomPasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('accounts/password-reset/complete/', CustomPasswordResetCompleteView.as_view(), name='password-reset-complete'),
    path('accounts/email-verify/<str:uidb64>/<str:token>/', EmailVerifyView.as_view(), name='email-verify'),
    path('users/', UserListView.as_view(), name='users'),
    path(
        'api/users/create/',
        APIUserCreateView.as_view(),
        name='api-user-create',
    ),
    path(
        'api/users/<int:pk>/delete/',
        APIUserDeleteView.as_view(),
        name='api-user-delete',
    ),
    path(
        'api/users/<int:pk>/modify/',
        APIUserModifyView.as_view(),
        name='api-user-modify',
    ),
    path('users/<int:pk>/profile/', UserProfileView.as_view(), name='user-profile'),
    path('users/<int:pk>/modify/', UserModifyView.as_view(), name='user-modify'),
]
