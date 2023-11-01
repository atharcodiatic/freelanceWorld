from django.urls import path
from . import views
from django.views.generic.base import TemplateView


"""
myproposal/ - Path for Freelancer own Proposal Panel (can view his own proposal) 
"""
app_name = 'freelancer'
urlpatterns = [
    path('freelancerfeed/', views.FreelancerHome.as_view(), name="freelancerfeed"),
    path('myproposal/', views.FreelancerPropsalView.as_view(), name="myproposal"),
    path('proposaledit/<int:pk>', views.ProposalEditView.as_view(), name="proposal-edit"),
    # path('jobdetail/<int:pk>', views.JobDetailView.as_view(), name="jobdetail"),
]