from django.shortcuts import render

# Create your views here.
from .forms import *
from django.contrib.auth import login ,authenticate
from django.shortcuts import redirect 
from django.contrib.auth import get_user_model
from django.views.generic import View , DetailView
from django.urls import reverse 
from django.shortcuts import HttpResponseRedirect

''' HttpResponseRedirect for firefox'''

from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model

def userchangeview(request):
    context ={}
    context ['form']= FreelancerProfile()

    return render(request, 'accounts/changeforms.html', context)

User =  get_user_model()

def freelancer_registeration_view(request):

    ''' This view handles Freelancer User Registration '''

    if request.method =='POST':
        form = FreelancerProfile(request.POST, request.FILES)
        if form.is_valid():
            pass_word = form['password'].data
            print(pass_word)
            user = form.save()
            user.set_password(pass_word)
            user.save()
            return redirect(reverse('home'))

    else:
        form = FreelancerProfile()
        form.order_fields(['email', 'username', 'firstname', 'lastname'])

    return render(request, 'accounts/freelancer_register.html', {'form': form })

def home(request):
    return render(request,'accounts/home.html')

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
                redirect_url = reverse('home')
                return redirect(redirect_url)
            
        
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
            return self.form_valid(form)
        else:
            return self.form_invalid(form) 
 
# class SkillView(View):
#     form_class = SkillForm

        
#     def post(self, request):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             print(form['name'].data)
#             form.save()

#             return redirect(reverse("register_freelancer"))

    
class FreeLancerProfileView(DetailView):
    template_name = 'accounts/freelancer_profile.html'
    model = Freelancer

    def get_context_data(self, *args, **kwargs):
        context = super(FreeLancerProfileView,
             self).get_context_data(*args, **kwargs)
        # add extra field   
        return context
