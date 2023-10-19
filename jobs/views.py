from django.shortcuts import render

# Create your views here.

from django.views.generic.base import TemplateView
 
class ClientHomePage(TemplateView):
    template_name = 'jobs/home.html'

    
