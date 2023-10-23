from typing import Any
from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from .forms import *
from .models import *
# Create your views here.
from django.http import HttpResponse, JsonResponse,HttpResponseForbidden
import json 
from django.http import QueryDict

from django.views.generic.base import TemplateView 
from django.views.generic import DetailView
from django.views.generic.edit import ModelFormMixin
 
class ClientHomePage(TemplateView):
    template_name = 'jobs/home.html'

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)
    
        job = JobPost.objects.filter(user = self.request.user.id)
        context['client_jobs'] = job 
        return context

    
class JobCreateView(View):
    template_name = 'jobs/create_job.html'
    form = JobPostForm
    
    def dispatch(self, request, *args, **kwargs):
        # self.user_id
        setattr(self, 'user_id', request.user.id) 
        return super().dispatch(request, *args, **kwargs)
        
    def get(self,request,*args,**kwargs):
        context= {}
        context ['job_form'] = self.form()
        context ['skill_form'] = SkillForm()
        return render(request, self.template_name, context)
    
    def post(self,request,*args,**kwargs):
        form = self.form(request.POST)
        
        if form.is_valid():
            form_obj = form.save(commit=False)
            
            client_obj = Client.objects.get(id = self.user_id)
            form_obj.user = client_obj
            form_obj.save()
            form.save_m2m()
            # print(form.skill_required.all())
            # print(form.__dict__)
        
            return redirect(reverse('jobs:clienthome'))
        return HttpResponse('failed', status=500)
        

class SkillCreateView(View):
    """
    This View adds skill data to skill model, skills added by job poster.
    """
    template_name = 'jobs/create_job.html'
    form = SkillForm

    # def get(self,request,*args,**kwargs):
    #     context= {}
    #     context ['skill_form'] = SkillForm()
    #     return render(request, self.template_name, context)

    def post(self,request,*args,**kwargs):
        data = json.loads(request.body)
        skill = data.get('skill')
        
        
        client_obj = Client.objects.get(id = request.user.id)
        skill_obj = Skill.objects.create(name=skill, client=client_obj)
        skill_obj.save()
        
        return JsonResponse({'status':'success', 'id':skill_obj.id}, status=200)
    

class JobDetailView(ModelFormMixin, DetailView):

    """
    ModelFormMixin provides form to update the jobpost and handles form data with post method , 
    DetailView shows the detail of JobPost with pk.
    """
    model = JobPost
    template_name = 'jobs/job_detail.html'
    form_class = JobPostForm
    

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)
        context ['job_form'] = self.get_form()
        return context
    
    def get_success_url(self):
        return reverse("jobs:jobdetail", kwargs={"pk": self.object.pk})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def form_valid(self, form):
        return super().form_valid(form)
    

    def get_initial(self):
        obj = self.get_object()
        return {  'job_id': obj.title }


        
    


    
