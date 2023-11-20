from faker import Factory
import factory
from accounts.models import *
from cities_light.models import City, Country
from jobs.models import *
import random

# SkillCreateView
faker = Factory.create()

class CountryFactory:
    class Meta:
        model = Country
    name="India"

class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = City
    name = 'Indore'

class FreelancerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Freelancer    
    username = faker.user_name()
    phone_number = faker.random_number(10)
    email = faker.email()
    password = faker.password()
    city = City.objects.filter(name="Indore").first()
    country = Country.objects.filter(name="India").first()
    years_of_experience = random.randint(0,20)

class SelfSkillFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SelfSkills   
    skill_name = faker.word()
    level = random.choice(['INT', 'BEG', "EXP"])
    freelancer = factory.SubFactory(FreelancerFactory)

class ProposalFactory():
    class Meta:
        model = JobProposal