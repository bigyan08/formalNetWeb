from . import views
from django.urls import path,include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.index,name='index'),

    path('register/',views.register_page,name='register'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logoutUser,name='logout'),

    path('profile/<str:pk>/',views.profile_view,name='user-profile'),

    path('prompt/delete/<int:prompt_id>/',views.delete_prompt,name='delete-prompt'),

    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]