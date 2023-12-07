from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('', views.home),
    path('register/freelancer', views.freelancer_registeration_view, name='register_freelancer'),
    path('register/client', views.ClientRegistrationView.as_view(), name= 'register_client'),
    path('register/', views.register_view,name='register'),
    path('login/', views.LoginPageView.as_view(), name='login'),
    # bug -on logout our view should redirect to  HttpPermanentRedirect
    path('logout', auth_views.LogoutView.as_view(template_name='accounts/freelancer_profile.html',next_page='/login'), name='logout'),
    path('<int:pk>/freelancer_profile', views.FreeLancerProfileView.as_view(), name = 'freelancer-profile'),
    path('<int:pk>/freelancer_profile_update', views.FreeLancerUpdateView.as_view(), name = 'freelancer-updateprofile'),
    path('<int:pk>/education/', views.education_view,name = 'education'),
    path('<int:pk>/skill/', views.SkillCreateView.as_view(),name = 'skill'),
    path('<int:pk>/clientprofile/', views.ClientProfileView.as_view(),name = 'client-profile'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
    path('social-login-user/', views.HandleSocialLogin.as_view(), name='social_login'),
    

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "accounts/reset_password.html"), name ='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "accounts/password_reset_sent.html"), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "accounts/password_reset_form.html"), name ='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "accounts/password_reset_done.html"), name ='password_reset_complete')
]



    
