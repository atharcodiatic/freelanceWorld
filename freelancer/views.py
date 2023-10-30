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
    switch = None

    def get_context_data(self,*args,**kwargs):

        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        edu_names = None
        skill_names = None
        fl_obj = Freelancer.objects.get(id = user_id)
        experience = fl_obj.years_of_experience
        res =None
        if Education.objects.filter(freelancer = user_id).exists():
            edu_names = Education.objects.filter(freelancer = user_id).values_list('course',flat=True)
            
        if SelfSkills.objects.filter(freelancer = user_id).exists():
            skill_names = SelfSkills.objects.filter(freelancer = user_id).values_list('skill_name', flat=True)

        # recomended jobs for feed 
        if edu_names and skill_names: 
            if JobPost.objects.filter(Q(experience_required__lte=experience) & Q(Q(category__in = edu_names) | Q(skill_required__name__in = skill_names) ) ).exists():
                res = JobPost.objects.filter(Q(experience_required__lte=experience) & Q(Q(category__in = edu_names) | Q(skill_required__name__in = skill_names) ) ).distinct()
                
        # jobs for all_job panel, freelancer can browse
        all_jobs = JobPost.objects.all()
        
        if self.switch == "all_job":
            context['result'] = all_jobs
        else:
            context['result'] = res
        return context
    
    def post(self,request,*args,**kwargs):
        
        data = request.body
        data  = json.loads(data)
        if data['showFeed']:
            self.switch = 'showFeed'
        else:
            self.switch = 'all_job'
            
        context = self.get_context_data(self.args,self.kwargs)
        # d = super(FreelancerHome,self).get(request,*args,**kwargs)
        return JsonResponse({'status':'success'},status=200)

    
class FreelancerPropsalView(TemplateView):
    template_name = 'freelancer/my_proposal.html'

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)
        user_proposal = None
        if JobProposal.objects.filter(user=self.request.user.id).exists():
            user_proposal = JobProposal.objects.filter(user=self.request.user.id)
        context["my_proposal"] = user_proposal
        context['proposal_form'] = ''
        return context
    


