from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic.base import TemplateView
from accounts.models import *
from jobs.models import *
from django.db.models import Q
from django.http import JsonResponse
import json 

class FreelancerHome(TemplateView):
    template_name = 'freelancer/feed.html'

    switch = "all_job"
    
    def get_context_data(self,*args,**kwargs):
        
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        edu_names = None
        skill_names = None
        fl_obj = Freelancer.objects.get(id = user_id)
        experience = fl_obj.years_of_experience
        if Education.objects.filter(freelancer = user_id).exists():
            edu_names = Education.objects.filter(freelancer = user_id).values_list('course',flat=True)
            
        if SelfSkills.objects.filter(freelancer = user_id).exists():
            skill_names = SelfSkills.objects.filter(freelancer = user_id).values_list('skill_name', flat=True)

        # recomended jobs for feed 
        res = JobPost.objects.filter(Q(experience_required__lte=experience) & Q(Q(category__in = edu_names) | Q(skill_required__name__in = skill_names) ) ).distinct()
        # jobs for all_job panel, freelancer can browse
        all_jobs = JobPost.objects.all()

        context['result'] = res  
        context['all_jobs'] = all_jobs
        context['switch'] = self.switch
        return context
    
    def post(self,request,*args,**kwargs):
        breakpoint()
        data = request.body
        data  = json.loads(data)
        if data['showFeed']:
            self.switch = 'showFeed'
        else:
            self.switch = 'all_job'
        print(self.switch,"*********")
        return JsonResponse({'status':'success'},status=200)

    
