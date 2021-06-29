from django.urls import path
from .views import *
from .utilities import check_recaptcha
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', index, name='index'),
    path('event/<int:pk>/', detail_event, name='detail'),
    path('event/follow/<int:pk>/<str:status>', follow_event, name='follow_event'),
    path('accounts/login/', Login.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(template_name='main/logout.html'), name='logout'),
    path('accounts/profile/change', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/change_password/', UserPasswordChangeView.as_view(), name='password_change'),
    path('accounts/password/reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/password/reset/', PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/password/confirm/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('accounts/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/registration', check_recaptcha(register_volunteer), name='registration'),
]
