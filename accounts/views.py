from typing import Any
from django import http
from django.shortcuts import render

# Create your views here.
from .forms import *
from django.contrib.auth import login ,authenticate
from django.shortcuts import redirect 
from django.contrib.auth import get_user_model
from django.views.generic import View , DetailView,ListView
from django.urls import reverse , reverse_lazy
from django.shortcuts import HttpResponseRedirect
import datetime
''' HttpResponseRedirect for firefox'''
from django.views.generic.edit import CreateView , UpdateView 
from django.contrib.auth import get_user_model
from django.http import JsonResponse , HttpResponseForbidden
from django.core.serializers import serialize
import json
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import  Permission
from django.contrib.contenttypes.models import ContentType
from django.views.generic.edit import ModelFormMixin
from jobs.forms import ReviewForm
from django.forms import modelform_factory
from cities_light.models import City,Country
User =  get_user_model()

def freelancer_registeration_view(request):
    ''' This view handles Freelancer User Registration '''
    if request.method =='POST':
        form = FreelancerProfile(request.POST, request.FILES)
        if form.is_valid():
            pass_word = form['password'].data
            user = form.save()
            user.set_password(pass_word)
            user.save()
            breakpoint()
            content_type = ContentType.objects.get_for_model(Freelancer)
            is_fl_permission = Permission.objects.get(content_type=content_type , codename='is_freelancer')
            user.user_permissions.add(is_fl_permission)
            user_id = user.id

            return redirect("/login/")
    else:
        form = FreelancerProfile()
        form.order_fields(['email', 'username', 'firstname', 'lastname'])
    return render(request, 'accounts/freelancer_register.html', {'form': form })


def load_cities(request):
    country_id = request.GET.get('country_id')
    cities = City.objects.filter(country=country_id).all()
    return render(request, 'accounts/city_dropdown_list_options.html', {'cities': cities})

def register_view(request):
    return render(request,'accounts/register.html')

class LoginPageView(View):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    
    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})
        
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                user_id = request.user.id
                if user.has_perm('accounts.is_client'):
                    return redirect(reverse("jobs:clienthome"))
                else:
                    return redirect("/"+ str(user_id)+'/freelancer_profile')
                    
        message = 'Login failed!'
        return render(request, self.template_name, context={'form': form, 'message': message})
    

class ClientRegistrationView(CreateView):
    ''' This view is responsible for creating  instance of Client Model  '''

    model = Client
    form_class = ClientProfile
    template_name = 'accounts/client_register.html'
    success_url = '/login/'

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        pass_word = form['password'].data
        if form.is_valid():
            user = form.save()
            user.set_password(pass_word)
            user.save()
            content_type = ContentType.objects.get_for_model(Client)
            cl_permission = Permission.objects.get(content_type=content_type , codename='is_client')
            user.user_permissions.add(cl_permission)
            return self.form_valid(form)
        else:
            return self.form_invalid(form) 
 
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin

class ClientOwnPer(PermissionRequiredMixin):
    permission_required = 'accounts.is_client'
    def has_permission(self):
        """
        Override this method to customize the way permissions are checked.
        """
        user = self.request.user
        perms = self.get_permission_required()
        if not self.request.user.is_authenticated:
            raise PermissionDenied('not allowed')
        if (user.has_perms("accounts.is_client") and self.kwargs['pk']==user.id)\
              or user.has_pemrs("accounts.is_freelancer"):
            return self.request.user.has_perms(perms)
    

class FreeLancerProfileView(LoginRequiredMixin, DetailView):
    """
    This view shows the Profile Details of FreelancerInstance 
    and uses pk
    """
    template_name = 'accounts/freelancer_profile.html'
    model = Freelancer

    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated and request.user.id == int(kwargs['pk']):
    #         return super().dispatch(request, *args, **kwargs)
    #     raise PermissionDenied("Not Allowed")
        # return HttpResponseRedirect('/register/')

    def get_context_data(self, *args, **kwargs):
        context = super(FreeLancerProfileView,
             self).get_context_data(*args, **kwargs)
        
        # add extra field   
        pk  = self.object.pk
        self_skill = SelfSkills.objects.filter(freelancer__id = pk )
        education = Education.objects.filter(freelancer__id = pk)
        all_skills = Skill.objects.all()[0:9]
        context['self_skills'] = self_skill
        context['education'] = education
        context['edu_form'] = EducationForm()
        context['standard_skills'] = all_skills
        context['add_skillform'] = SelfSkillForm()
        return context

class FreeLancerUpdateView(UpdateView):
    '''
    Freelancer can edit his profile with this view
    '''
    form_class = FreelancerProfileUpdate
    model = Freelancer
    url_id = None
    template_name = 'accounts/freelancer_profile_update.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.id == int(kwargs['pk']):
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect('/register/')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('freelancer-profile', kwargs={'pk': self.object.pk})


def education_view(request, pk):
    """
    This View is responsible for adding freelancer education
    """
    if request.method == 'POST':
        type = request.POST.get('type')
        degree = request.POST.get('degree')
        course = request.POST.get('course')
        end_date = request.POST.get('end_date').split(',')
        start_date = request.POST.get('start_date').split(',')
        end_date_obj = datetime.date(int(end_date[0]),int(end_date[1]),int(end_date[2]))
        start_date_obj = datetime.date(int(start_date[0]),int(start_date[1]),int(start_date[2]))
        college_name = request.POST.get('college_name')
        freelancer_obj = Freelancer.objects.get(id=pk)
        Education.objects.create(type=type, degree_name = degree, course=course, 
                                 college_name = college_name , start_date = start_date_obj ,
                                 end_date = end_date_obj, freelancer = freelancer_obj)
    elif request.method == "GET":
        education = Education.objects.filter(freelancer__id=int(pk))
        education = [education.last()]
        serialized_data = serialize("json", education)
        serialized_data = json.loads(serialized_data)
        return JsonResponse(serialized_data, safe=False , status=200) 
    return JsonResponse({"status": 'Success'}) 


class SkillCreateView(View):
    """
    This view adds FreeLancer skills
    """
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        user_id = int(request.user.id)
        request = json.loads(request.body)
        skill_name = request.get('skill')
        level = request.get('level')
        """
        we can handle this validation in forntend, just for learning purpsoes
        """
        choices = ['INT', 'BEG', "EXP"]
        if level not in choices:
            return JsonResponse({'status':"failed" ,'message': 'Please select a valid level '})
        # check if skill exist or not 
        skillpresent = SelfSkills.objects.filter(freelancer=user_id, skill_name = skill_name).exists()
        if not skillpresent:
            freelancer = Freelancer.objects.get(id=user_id)
            model_obj = SelfSkills.objects.create(skill_name = skill_name, freelancer=freelancer, level = level)
        return JsonResponse({'status':"success" }, status=201)
    
    def get(self,request,*args,**kwargs):
        pk = kwargs['pk']
        skill = SelfSkills.objects.filter(freelancer__id=int(pk))
        serialized_data = serialize("json", skill)
        serialized_data = json.loads(serialized_data)
        return JsonResponse(serialized_data, safe=False , status=200) 
    
    def patch(self,request,*args,**kwargs):
        pk = kwargs['pk']
        request = json.loads(request.body)
        skill_name = request.get('skill')
        skill_level = request.get('level')
        skill_obj = SelfSkills.objects.filter(freelancer=pk, 
                                                 skill_name = skill_name)[0]
        skill_obj.level = skill_level
        skill_obj.save()
        return JsonResponse({'status':"success" }, status=200)
    
    def delete(self,request,*args,**kwargs):
        pk = kwargs['pk']
        request = json.loads(request.body)
        skill_name = request.get('skill')
        skill_obj = SelfSkills.objects.filter(freelancer=pk, skill_name = skill_name)
        skill_obj.delete()
        return JsonResponse({'status':"success" }, status=204)

        
class ClientProfileView(ClientOwnPer,ModelFormMixin, DetailView):
    """
    Client DetailView , ModelFormMixin to edit the ClientProfile
    """
    model = Client
    template_name = "accounts/client_profile.html"
    form_class = ClientProfileUpdate

    def get_context_data(self, *args, **kwargs):
        context = super(ClientProfileView,
             self).get_context_data(*args, **kwargs)
        context ['update_client_form'] = self.get_form()
        context ['review_form'] = ReviewForm
        return context
    def get_success_url(self):
        return reverse_lazy("client-profile", kwargs={"pk":self.object.pk})
    
    def get_initial(self):
        """ This method pass initial data in form"""
        obj = self.get_object()
        return {  'user_id': obj.username }
    
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









    

    
