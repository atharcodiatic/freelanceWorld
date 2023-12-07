from django.test import TestCase
from django.test import Client as test_client
import unittest
from django.test import RequestFactory, TestCase
from cities_light.models import City, Country
from jobs.views import JobDetailView
from jobs.models import *
from accounts.models import *
import factory
from faker import Factory
from ..accounts.test import CreateModelObject
from unittest import mock
from django.db.models.signals import  post_save
faker = Factory.create()

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
        
    # def test_false_data(self):
    #     self.assertEqual("value too long for type character varying(10)")


class JobDetailViewTestCase(TestCase):
    """ Test case for job detail view """
    def setUp(self):
        country_obj = Country.objects.create(name="India")
        city_obj = City.objects.create(name="Indore", country=country_obj)
        self.client_obj = Client.objects.create(email="ebestpeers@gmail.com",
                                           country=country_obj,
                                           city=city_obj,
                                           phone_number="9823789309",
                                           first_name='bestpeers',
                                           last_name= 'infosystem',
                                           username= 'bestpeersinfosystem',
                                           )
        skill_obj_1= Skill.objects.create(name="python",client=self.client_obj)
        skill_obj_2 = Skill.objects.create(name="React",client=self.client_obj)
        for i in range(10):
            job_obj = JobPost.objects.create(title="Django Job",
                                category="IT",
                                user = self.client_obj,
                                experience_required=3,
                                description='Candidate must be able to write test cases',
                                duration_type='year',
                                duration=2,
                                currency='RS',
                                salary=4000,
                                    )
        
    def test_view(self):
        c = test_client()
        
        response = c.post(reverse('login'), c.force_login(user=self.client_obj))
        self.assertEqual(response.status_code,200)
        for i in range(1,10):
            r = reverse("jobs:jobdetail",kwargs={'pk':i})
            response = c.get(reverse("jobs:jobdetail",kwargs={'pk':i}))
            con = response.content
            # bug -> assertIn return None
            self.assertIn('proposal_form', response.context)
            self.assertEqual(response.status_code,200)

from unittest.mock import patch
class TestCreateContractProposal(CreateModelObject, TestCase):
    @classmethod
    def setUpTestData(cls):
        super(TestCreateContractProposal, cls).setUpTestData()
        
    def testview(self):
        with mock.patch('jobs.signals.send_email_otp', autospec=True) as mocked_handler:
            post_save.connect(mocked_handler, sender=Contract,)
            self.assertEquals(mocked_handler.call_count, 1)

        self.contract(proposal= self.job_proposal)
        self.assertEqual(True,True)

        
    