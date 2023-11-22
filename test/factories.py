from faker import Factory
import factory
from accounts.models import *
from cities_light.models import City, Country
from jobs.models import *
import random

# SkillCreateView
faker = Factory.create()

class CountryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Country
    name = faker.country()
    # continent = "AS"

class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = City
    name = faker.city()
    country = factory.SubFactory(CountryFactory)

class FreelancerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Freelancer    
    username = faker.user_name()
    phone_number = faker.random_number(10)
    email = faker.email()
    password = 'password123'
    country = factory.SubFactory(CountryFactory)
    city = factory.SubFactory(CityFactory)
    years_of_experience = random.randint(0,20)

class ClientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Client
    username = faker.user_name()
    phone_number = faker.random_number(10)
    email = faker.email()
    password = faker.password()
    # city = City.objects.filter(name="Indore").first()
    # country = Country.objects.filter(name="India").first()
    type = random.choice(['Community', 'individual'])
    company_name = faker.name()
    
class SelfSkillFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SelfSkills   
    skill_name = faker.word()
    level = random.choice(['INT', 'BEG', "EXP"])
    freelancer = factory.SubFactory(FreelancerFactory)

class ProposalFactory():
    class Meta:
        model = JobProposal