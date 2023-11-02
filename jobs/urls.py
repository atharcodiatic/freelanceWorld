from django.urls import path
from . import views


app_name ='jobs'
urlpatterns = [
    path('clienthome/', views.ClientHomePage.as_view(), name="clienthome"),
    path('createjob/', views.JobCreateView.as_view(), name="createjob"),
    path('skillcreate/', views.SkillCreateView.as_view(), name="skillcreate"),
    
    path('jobdetail/<int:pk>', views.JobDetailView.as_view(), name="jobdetail"),
    path('jobproposal/', views.JopProposalView.as_view(), name="job-proposal"),
    path('createcontract/<int:pk>', views.CreateContract.as_view(), name="create-contract"),
    path('browse_freelancer/', views.FreelancerView.as_view(),name='browse-freelancer'),
    path('myhire/', views.MyHireView.as_view(),name='my-hire'),
    # path('browsefreelancer/',views.BrowseFreelancer.as_view(),name='browse-freelancer')
    
]