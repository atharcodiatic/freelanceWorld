from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic.base import TemplateView
from accounts.models import *
from jobs.models import *
from jobs.forms import *
from django.db.models import Q
from django.http import JsonResponse
import json 
from django.views.generic.edit import ModelFormMixin , DeletionMixin
from django.http import HttpResponseForbidden
from django.contrib.postgres.search import SearchVector 
from django.views.generic import ListView

class FreelancerHome(TemplateView):
    template_name = 'freelancer/feed.html'
    #bugs -> fixed
    def get(self, request, *args, **kwargs):
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
        all_jobs = JobPost.objects.all().order_by('-created_at')
        context={}
        feed = request.GET.get('feed')
        all_job = request.GET.get('showall')
        freel_search = request.GET.get('search')

        if freel_search :
            job_search = JobPost.objects.annotate(search=SearchVector("title", "skill_required__name")).filter(
            search=freel_search)
            context['result'] = job_search
        elif feed:
            context['result'] = res
        else:
            context['result'] = all_jobs
        return render(request,self.template_name,context)
    

    # def post(self,request,*args,**kwargs):
    #     data = request.body
    #     data  = json.loads(data)
    #     if data['showFeed']:
    #         self.switch = 'showFeed'
    #     else:
    #         self.switch = 'all_job'  
    #     context = self.get_context_data(self.args,self.kwargs)
    #     # d = super(FreelancerHome,self).get(request,*args,**kwargs)
    #     return JsonResponse({'status':'success'},status=200)

    
class FreelancerPropsalView(TemplateView):
    """
    This View Show all the proposals.
    """
    template_name = 'freelancer/my_proposal.html'

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)
        user_proposal = None
        if JobProposal.objects.filter(user=self.request.user.id).exists():
            user_proposal = JobProposal.objects.filter(user=self.request.user.id)
        context["my_proposal"] = user_proposal
        context['proposal_form'] = JobProposalForm()
        return context
    
class ProposalEditView(ModelFormMixin, View,):
    """
    We use ModelFormMixin(post) to update the proposal of freelancer 
    View - we can not use ModelFormMixin Directly , so we inherit view
    DeletionMixin will not work because deletemixin also has post , so
    conflict between  modelformMixin Post Method 
    """
    model = JobProposal
    form_class = JobProposalForm
     
    def get_success_url(self):
        return reverse("freelancer:myproposal")
    
    def post(self, request, *args, **kwargs):
        breakpoint()
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
    
    def delete(self,request,*args,**kwargs):
        self.model.objects.filter(id=kwargs['pk']).delete()
        return JsonResponse({"status":"deleted successfully"}, status=204)
    
class MyJobsView(TemplateView):
    template_name = 'freelancer/my_jobs.html'

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)
        user_jobs = None
        queryset = JobProposal.objects.filter(user=self.request.user.id, status="ACCEPTED")
        if queryset.exists():
            user_jobs = queryset
        context["my_jobs"] = user_jobs
        return context

class BrowseView(ListView):
    paginate_by = 4
    template_name = "freelancer/browse.html"
    model = Client 
    extra_context = None 

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get("q")
        if query:
            '''doubt - how to filter object by average_rating '''
            client_obj = Client.objects.annotate(search=SearchVector("username","bio","company_name","jobpost__skill_required__name")).filter(
            search=query)
            return client_obj.distinct("username")
        else:
            return Client.objects.all().distinct()


    