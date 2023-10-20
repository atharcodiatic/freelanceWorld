from django.shortcuts import render
from django.views import View
from .forms import *
# Create your views here.
from django.http import HttpResponse, JsonResponse


from django.views.generic.base import TemplateView
 
class ClientHomePage(TemplateView):
    template_name = 'jobs/home.html'

    
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
        breakpoint()
        form = self.form(request.POST)
        
        if form.is_valid():
            form = form.save(commit=False)
            client_obj = Client.objects.get(id = self.user_id)
            form.user = client_obj
            form.save()
        
            return HttpResponse('creation sucessfull')
        

class SkillCreateView(View):
    """
    This View adds skill data to skill model, skills added by job poster.
    """
    template_name = 'jobs/create_job.html'
    # form = SkillForm

    # def get(self,request,*args,**kwargs):
    #     context= {}
    #     context ['skill_form'] = SkillForm()
    #     return render(request, self.template_name, context)

    def post(self,request,*args,**kwargs):
        breakpoint()
        form = self.form(request.POST)
        
        if form.is_valid():
            form = form.save(commit=False)
            client_obj = Client.objects.get(id = self.user_id)
            form.client = client_obj
            form.save()
        
            return JsonResponse({'status':'creation sucessfull'}, status=200)


    
