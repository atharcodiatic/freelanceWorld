from typing import Any
from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from .forms import *
from .models import *
from accounts.models import *
# Create your views here.
from django.http import HttpResponse, JsonResponse,HttpResponseForbidden,\
HttpResponseRedirect
import json 
from django.http import QueryDict
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView 
from django.views.generic import DetailView
from django.views.generic.edit import ModelFormMixin, CreateView
from django.db.models import Q
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from .utility import *
 
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

    def setup(self,request,*args,**kwargs):
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        setattr(self, 'user_id', request.user.id) 
        return super().dispatch(request, *args, **kwargs)
        
    def get(self,request,*args,**kwargs):
        
        print(kwargs)
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
        context['proposal_form'] = JobProposalForm()
        user_id = self.request.user.id
        context['proposal_exist'] = JobProposal.objects.filter(job= self.object.pk, user=user_id).exists()
        job_prop = JobProposal.objects.filter(job= self.object.pk).exists()
        if job_prop:
            proposals = JobProposal.objects.filter(job= self.object.pk)
            context['job_proposols']  =  proposals
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
        """ 
        This method is passing initial data in form Passing Initial Data in Form
        """
        obj = self.get_object()
        return {  'job_id': obj.title }


class JopProposalView(CreateView):
    """
    this view creates a job proposal
    """
    form_class = JobProposalForm
    model = JobProposal
    job_id = None
    def dispatch(self, request, *args, **kwargs):
        setattr(JopProposalView, 'user_id', request.user.id) 
        return super().dispatch(request, *args, **kwargs)
    

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """ 
        form = self.get_form()
        if form.is_valid():
            form_obj = form.save(commit=False)
            user_obj = Freelancer.objects.get(id=request.user.id)
            # bug  -> job id can be extracted from Http referrer
            # bug fixed -> status ok
            self.job_id = request.META.get('HTTP_REFERER').split('/')[-1]
            job_obj = JobPost.objects.get(id = self.job_id)
            if not JobProposal.objects.filter(job=self.job_id,user=self.user_id).exists():
                form_obj.user = user_obj
                form_obj.job = job_obj
                form_obj.save()
                return self.form_valid(form)
            else:
                url = reverse_lazy("jobs:jobdetail", kwargs={"pk":self.job_id})
                return HttpResponseRedirect(url)
        else:
            return self.form_invalid(form)
    
    def get_success_url(self):
        
        return reverse_lazy("jobs:jobdetail", kwargs={"pk":self.job_id})
    

class CreateContract(View):
    """
    This View Create contract (payment details) 
    """
    
    """
    this get method is for testing purpose -> breakpoint
    def get(self, request, *args, **kwargs):
        proposal_id = kwargs['pk']
        prop_obj = JobProposal.objects.get(id = proposal_id)
    """

    def post(self, request, *args, **kwargs):
        
        
        proposal_id = kwargs['pk']
        prop_obj = JobProposal.objects.get(id = proposal_id)
        # freelancer Info - bid and currency (prop_obj.user)
        bid = prop_obj.bid
        freelancer_currency = prop_obj.currency
        # Client Info - bid and currency (client= prop_obj.job)
        job_currency = prop_obj.job.currency
        duration_type = prop_obj.job.duration_type
        duration = prop_obj.job.duration
        # currency and calculation
        converter = currency_converter(job_currency, bid, freelancer_currency)
        total = calculate_total(duration, duration_type, converter[0])
        contract_currency = converter[1]
        redirect_address = request.META.get("HTTP_REFERER")
        
        Contract.objects.create(proposal = prop_obj, total=total, currency=contract_currency)

        job = JobPost.objects.get(id=prop_obj.job.id)
        job.status = 'CLOSED'
        job.save()

        prop_obj.status = 'ACCEPTED'
        prop_obj.save()

        response = HttpResponseRedirect(redirect_to = redirect_address)
        response.content = 'Contract Created Successfully'
        response.status = 201
        return response
    

class FreelancerView(ListView):
    paginate_by = 4
    template_name = "jobs/browse_freelancer.html"
    model = Freelancer  
    queryset = Freelancer.objects.all().order_by('-selfskills__freelancer_id').distinct()

    def get(self, request, *args, **kwargs):
        skill = request.GET.get("skill")
        education = request.GET.get("education")
        level = request.GET.get("level")
        experience = request.GET.get("experience")
        if request.GET.get("freelancer") or skill or experience or education or level:
            object_list = self.get_queryset()
            user_search = request.GET.get("freelancer")
            search_data = ''
            
            referer = request.META.get("HTTP_REFERER").split('/')[-1].split('=')[-1]
            if '+' in referer:
                referer = referer.replace('+', ' ')
            breakpoint()
            if user_search:
                education = Freelancer.objects.filter(education__course__icontains=user_search)
                if Freelancer.objects.filter(Q(username__icontains=user_search) | Q(selfskills__skill_name__icontains=user_search ) | Q(education__course__icontains=user_search)).exists():
                    search_data = Freelancer.objects.filter(Q(username__icontains=user_search) | Q(selfskills__skill_name__icontains=user_search)|Q(education__course__icontains=user_search)).distinct()
            else:
                search_data = Freelancer.objects.filter(Q(username__icontains=referer) | Q(selfskills__skill_name__icontains=referer)|Q(education__course__icontains=referer)).distinct()
            
            context = super(FreelancerView, self).get_context_data(object_list=object_list, *args, **kwargs)
            print(context)
            context['object_list'] = search_data
            if skill or education or level or experience:
                if ',' in skill:
                    skill = skill.split(',')
                if not experience:
                    experience = 0
                search_data = search_data.filter(Q(Q(selfskills__skill_name__in = skill) and Q(selfskills__level__icontains=level))\
                                    | Q(education__course__icontains=education)| Q(years_of_experience = experience))
                
                context['object_list'] = search_data

            return render(request, self.template_name, context)
        else:
            return super().get(request,args,kwargs)
    
