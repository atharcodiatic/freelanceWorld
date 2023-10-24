from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic.base import TemplateView
from accounts.models import *
from jobs.models import *
from django.db.models import Q

class FreelancerHome(TemplateView):
    template_name = 'freelancer/feed.html'


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
    
        res = JobPost.objects.filter(Q(experience_required__lte=experience) & Q(Q(category__in = edu_names) | Q(skill_required__name__in = skill_names) ) ).distinct()
        
        print('***********', res )

        
        context ['result'] = res  
        return context

    
