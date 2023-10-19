from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name ='common'
urlpatterns = [
    path('', views.HomePageView.as_view(), name="home"),

]