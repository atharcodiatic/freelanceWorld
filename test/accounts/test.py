from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from accounts.models import *
from ..factories import *
from django.test import Client as test_client
import json
from accounts.forms import * 


class SkillCreateViewTests(TestCase):
    breakpoint()
    freelancer = FreelancerFactory()
    skill =  SelfSkillFactory(freelancer=freelancer)

    @classmethod
    def setUpTestData(cls):
        cls.freelancer = FreelancerFactory()
        cls.skill =  SelfSkillFactory(freelancer=cls.freelancer)
        # setattr(cls,freelancer,freelancer)
        # setattr(cls,skill,skill)

        cls.c = test_client()
        data = {'skill': cls.skill.skill_name,'level':cls.skill.level}
        cls.json_data = json.dumps(data)
        cls.url = reverse(
            'skill', 
             args=(cls.skill.freelancer.id,)
        )

        response = cls.c.post(reverse('login'), cls.c.force_login(user=cls.freelancer))

        response = cls.c.post(cls.url, cls.json_data, content_type='application/json' )

    # def setUp(self):
    #     self.c = test_client()
    #     data = {'skill': self.skill.skill_name,'level':self.skill.level}
    #     self.json_data = json.dumps(data)
    #     self.url = reverse(
    #         'skill', 
    #          args=(self.skill.freelancer.id,)
    #     )

    #     response = self.c.post(reverse('login'), self.c.force_login(user=self.freelancer))

    #     response = self.c.post(self.url, self.json_data, content_type='application/json' )
        
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
