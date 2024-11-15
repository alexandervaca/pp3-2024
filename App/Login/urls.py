from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('login/', views.loginPage, name='login' ),
    path('registrarse/', views.registrarse, name='registrarse' ),
    path('logout', views.logoutUser, name='logout'),
    path('reset_password/',
    auth_views.PasswordResetView.as_view(template_name = "pass_reset/1-reset.html" ), 
    name='reset_password'),
    path('reset_password_sent/', 
    auth_views.PasswordResetDoneView.as_view(template_name = "pass_reset/2-done.html", 
    ), name= 'password_reset_done'),    
    path('reset/<uidb64>/<token>', 
    auth_views.PasswordResetConfirmView.as_view(template_name = "pass_reset/4-confirm.html"), name= 'password_reset_confirm'),
    path('reset_password_complete/',
     auth_views.PasswordResetCompleteView.as_view(template_name = "pass_reset/5-complete.html"), name= 'password_reset_complete'),
]

