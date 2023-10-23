from django.shortcuts import render
import sys
sys.path.append("..")
from accounts.models import *


from django.views.generic.base import TemplateView

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'common/home.html'

    def get_context_data(self,*args, **kwargs):
        context = super(HomePageView, self).get_context_data(*args,**kwargs)

        freelancers = Freelancer.objects.all().exclude(profile_pic='').distinct()[0:8]
        clients = Client.objects.all().exclude(profile_pic='')[0:8]
        
        context['freelancer_obj'] = freelancers
        context['client_obj']   = clients

        return context

