from django.shortcuts import render
import sys
sys.path.append("..")
from accounts.models import *

from django.views.generic.base import TemplateView
from jobs.forms import *
from jobs.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
import json 

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'common/home.html'

    def get_context_data(self,*args, **kwargs):
        context = super(HomePageView, self).get_context_data(*args,**kwargs)
        freelancers = Freelancer.objects.all().exclude(profile_pic='').distinct()[0:8]
        clients = Client.objects.all().exclude(profile_pic='')[0:8]
        context['freelancer_obj'] = freelancers
        context['client_obj']   = clients
        return context


class RatingView(LoginRequiredMixin,TemplateView):
    """Both Freelancer and Client can Rate each other At this View Page"""
    template_name = 'common/rating.html'
    form = ReviewForm

    def get(self, request, *args , **kwargs):
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args , **kwargs):
        form_data = json.loads(request.body)
        job_id = form_data.get('job_id')
        message_indicator = form_data.get("message_indicator")
        if not message_indicator:
            rating_by_id = form_data.get('rating_by')
            rating_to_id = form_data.get('rating_to')
            star_rating = form_data.get('star_rating')
            rating_by_obj = CustomUser.objects.get(id= rating_by_id)
            rating_to_obj = CustomUser.objects.get(id= rating_to_id)
            job_obj = JobPost.objects.get(id=job_id)
            if not Review.objects.filter(rating_by= request.user.id ,job=job_id).exists():
                Review.objects.create(rating_by=rating_by_obj, rating_to= rating_to_obj, star_rating=star_rating, job=job_obj)
                return JsonResponse({"status":"success"},status=201)
            else:
                return JsonResponse({"status":"success"},status=200)
        
        elif message_indicator:
            message = form_data.get('message')
            review_obj = Review.objects.filter(rating_by=request.user.id, job=job_id).first()
            if review_obj.review_message is None:
                review_obj.review_message = message 
                review_obj.save()
            return JsonResponse({"status":"success"},status=201)

    def get_context_data(self,*args, **kwargs):
        context = super(RatingView, self).get_context_data(*args,**kwargs)
        context['review_rating_form'] = self.form
        return context