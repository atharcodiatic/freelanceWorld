from django.test import TestCase
from jobs.models import *
from accounts.models import *
import unittest
from cities_light.models import City, Country
from django.test import RequestFactory, TestCase
from .views import JobDetailView
from django.test import Client as test_client
import factory

class JobPostTestCase(TestCase):
    def setUp(self):
        country_obj = Country.objects.create(name="India")
        city_obj = City.objects.create(name="Indore", country=country_obj)
        client_obj = Client.objects.create(email="ebestpeers@gmail.com",
                                           country=country_obj,
                                           city=city_obj,
                                           phone_number="9823789309",
                                           first_name='bestpeers',
                                           last_name= 'infosystem',
                                           username= 'bestpeersinfosystem',
                                           )
        skill_obj_1= Skill.objects.create(name="python",client=client_obj)
        skill_obj_2 = Skill.objects.create(name="React",client=client_obj)
        for i in range(10):
            job_obj = JobPost.objects.create(title="Django Job",
                                category="IT",
                                user = client_obj,
                                experience_required=3,
                                description='Candidate must be able to write test cases',
                                duration_type='year',
                                duration=2,
                                currency='RS',
                                salary=4000,
                                    )
            job_obj.skill_required.add(skill_obj_1,skill_obj_2)


    def test_count(self):
        self.assertEqual(JobPost.objects.all().count(),10)



class JobDetailViewTestCase(TestCase):
    def setUp(self):
        country_obj = Country.objects.create(name="India")
        city_obj = City.objects.create(name="Indore", country=country_obj)
        client_obj = Client.objects.create(email="ebestpeers@gmail.com",
                                           country=country_obj,
                                           city=city_obj,
                                           phone_number="9823789309",
                                           first_name='bestpeers',
                                           last_name= 'infosystem',
                                           username= 'bestpeersinfosystem',
                                           password='password@123',
                                           )
        self.client_obj = client_obj
    
    def test_view(self):
        c = test_client()
        breakpoint()
        response = c.post(reverse('login'), c.force_login(user=self.client_obj))
        self.assertEqual(response.status_code,200)
        r = reverse("jobs:jobdetail",kwargs={'pk':14})
        response = c.get(reverse("jobs:jobdetail",kwargs={'pk':14}))
        con = response.content

    