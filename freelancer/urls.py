from django.urls import path
from . import views


app_name ='freelancer'
urlpatterns = [
    path('freelancerfeed/', views.FreelancerHome.as_view(), name="freelancerfeed"),
    # path('createjob/', views.JobCreateView.as_view(), name="createjob"),
    # path('skillcreate/', views.SkillCreateView.as_view(), name="skillcreate"),
    
    # path('jobdetail/<int:pk>', views.JobDetailView.as_view(), name="jobdetail"),
    
    
]