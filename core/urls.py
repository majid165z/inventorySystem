from django.urls import path,reverse
from django.contrib.auth import views as auth_views
from django.urls.conf import include
from . import views
urlpatterns = [
    path('',views.home,name='home'),

    # warehouse urls
    path('warehouse/',include('warehouse.urls')),

    # account managements
    # login
    path('accounts/login',auth_views.LoginView.as_view(),name='login'),
    path('accounts/logout',views.logoutuser,name='logout'),
    path('accounts/password_change/',auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change_forms.html',
    ),name='password_change'),
    path('accounts/create-user',views.create_user,name='create_user'),
    path('accounts/user-list',views.user_list,name='user_list'),
    path('accounts/edit-user/<str:username>',views.edit_user,name='edit_user'),
]
