import json
from django.contrib.auth import get_user_model
from accounts.forms import * 
from django.test import TestCase
from django.urls import reverse
from django.test import Client as test_client
from accounts.models import *
from ..factories import *
from cities_light.models import City, Country

User = get_user_model()

class CreateModelObject(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.country = CountryFactory()
        cls.city = CityFactory(country=cls.country)
        cls.freelancer = FreelancerFactory(username=generate_username() , email=generate_email() ,city=cls.city, country=cls.country)
        cls.client = ClientFactory(username=generate_username() , email=generate_email() , city=cls.city, country=cls.country)
        cls.c = test_client()
        cls.self_skill = SelfSkillFactory(freelancer = cls.freelancer)
        cls.skill = SkillFactory(client = cls.client)
        cls.job  = JobPostFactory( user=cls.client, skill_required=(cls.skill))
        cls.job_proposal = JobProposalFactory(user=cls.freelancer, job=cls.job)
        cls.contract = ContractFactory

    
class SignUpTestCase(CreateModelObject, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.c = test_client()
        cls.client_data = {
            'username':'testuser',
            'email': "email.company@gmail.com" ,
            'password':"password@123" ,
            'country' : Country.objects.filter(name='India'),
            'city': City.objects.filter(name='Indore'),
            'phone_number' :9827893801,
            'confirm_password': "password@123",
            'type':'Community',
            }
        cls.client_credentials = {
            'email': cls.client_data['email'],
            'password': cls.client_data['password'],
             }
        cls.client_wrong_data = {}
        cls.client_wrong_data = cls.client_data
        cls.client_wrong_data['confirm_password']="password@13"

        cls.freelancer_data = {
            'username':'freeuser',
            'email': "email.freeuser@gmail.com" ,
            'password':"password@123" ,
            'country' : Country.objects.filter(name='India'),
            'city': City.objects.filter(name='Indore'),
            'phone_number' :9827893801,
            'confirm_password': "password@123",
            'years_of_experience':3,
        }
        cls.freelancer_crediantials = {
            'email':cls.freelancer_data.get('email'),
            'password':cls.freelancer_data.get('password'),
        }
        cls.freelancer_wrong_data = {}
        cls.freelancer_wrong_data.update(cls.freelancer_data)
        cls.freelancer_wrong_data['country'] = 'ertyuidcvb'

    def test_client_login_success(self):
        response = self.c.post(reverse('register_client'),
                               self.client_data, follow=True)
        self.assertEqual(200, response.status_code)
        response = self.c.post(reverse('login'), self.client_credentials, 
                               follow=True)
        self.test_client_login_success.client = self.c
        self.assertEqual(200, response.status_code)

    def test_client_signup_fail(self):
        response = self.c.post(reverse('register_client'), self.client_wrong_data, follow=True)
        self.assertEqual(False, response.context.get('form').is_valid())

    def test_freelancer_signup_login_success(self):
        response = self.c.post(reverse('register_freelancer'),
                               self.freelancer_data, follow=True)
        self.assertEqual(200, response.status_code)
        response = self.c.post(reverse('login'), self.freelancer_crediantials, 
                               follow=True)
        # function attribute
        self.test_freelancer_signup_login_success.freelancer = self.c
        self.assertEqual(200, response.status_code)
    
    def test_freelancer_signup_fail(self):
        response = self.c.post(reverse('register_freelancer'),
                               self.freelancer_wrong_data, follow=True)
        self.assertEqual(False,response.context.get('form').is_valid())




class SkillCreateViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.country = CountryFactory()
        cls.city = CityFactory(country=cls.country)
        cls.freelancer = FreelancerFactory(city=cls.city, country=cls.country)
        cls.skill =  SelfSkillFactory(freelancer=cls.freelancer)
        
        cls.c = test_client()
        data = {'skill': cls.skill.skill_name,'level':cls.skill.level}
        cls.json_data = json.dumps(data)
        cls.url = reverse(
            'skill', 
             args=(cls.skill.freelancer.id,)
        )

        response = cls.c.post(reverse('login'), cls.c.force_login(user=cls.freelancer))

        response = cls.c.post(cls.url, cls.json_data, content_type='application/json' )
    '''
    def setUp(self):
        self.c = test_client()
        data = {'skill': self.skill.skill_name,'level':self.skill.level}
        self.json_data = json.dumps(data)
        self.url = reverse(
            'skill', 
             args=(self.skill.freelancer.id,)
        )

        response = self.c.post(reverse('login'), self.c.force_login(user=self.freelancer))

        response = self.c.post(self.url, self.json_data, content_type='application/json' )
    '''

    def test_create_method(self):
        response = self.c.post(reverse('login'), self.c.force_login(user=self.freelancer))
        # response = self.client.post(self.url)
        response = self.c.post(self.url, self.json_data, content_type='application/json' )
        self.assertEqual(201, response.status_code)
        
    def test_update_method(self):
        response = self.c.patch(self.url, self.json_data,\
                                 content_type='application/json')
        self.assertEqual(200, response.status_code)

    def test_delete_method(self):
        response = self.c.delete(self.url, self.json_data,\
                                 content_type='application/json')
        self.assertEqual(204, response.status_code)

class CustomUserCreationFormTest(TestCase):
    def test_renew_form_date_field_help_text(self):
        form = CustomUserCreationForm()
        field_valdtr = form.fields['profile_pic'].validators
        self.assertTrue(any(isinstance(validator,FileExtensionValidator) for validator in field_valdtr))

