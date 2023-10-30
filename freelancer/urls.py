from django.urls import path
from . import views
from django.views.generic.base import TemplateView

app_name ='freelancer'
urlpatterns = [
    path('freelancerfeed/', views.FreelancerHome.as_view(), name="freelancerfeed"),
    path('myproposal/', views.FreelancerPropsalView.as_view(), name="myproposal"),
    # path('skillcreate/', views.SkillCreateView.as_view(), name="skillcreate"),
    # path('jobdetail/<int:pk>', views.JobDetailView.as_view(), name="jobdetail"),
]