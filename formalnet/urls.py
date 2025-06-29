from . import views
from django.urls import path

urlpatterns = [
    path('',views.index,name='index'),
    path('contact/',views.contact,name='contact'),

    # path('login/',views.loginPage,name='login'),
    # path('logout/',views.logoutUser,name='logout'),
    # path('register/',views.registerPage,name='register'),
]