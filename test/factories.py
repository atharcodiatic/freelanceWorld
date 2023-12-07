from faker import Factory,Faker
import factory
from accounts.models import *
from cities_light.models import City, Country
from jobs.models import *
import random
from django.contrib.auth import get_user_model

FAKER = Faker()

faker = Factory.create()

User = get_user_model()
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


#TODO need Optimization
def generate_email():
    email = faker.email()
    while User.objects.filter(email=email).exists():
        email=faker.email()
    return email
def generate_username():
    username = faker.name()
    while User.objects.filter(username=username).exists():
        email=faker.email()
    return username


class FreelancerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Freelancer    
    username = generate_username()
    phone_number = faker.random_number(10)
    email = generate_email()
    password = 'password123'
    country = factory.SubFactory(CountryFactory)
    city = factory.SubFactory(CityFactory)
    years_of_experience = random.randint(0,20)

class ClientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Client
    username = generate_username()
    phone_number = faker.random_number(10)
    email = generate_email()
    password = faker.password()
    city = factory.SubFactory(CityFactory)
    country = factory.SubFactory(CountryFactory)
    type = random.choice(['Community', 'individual'])
    company_name = faker.name()
    
class SelfSkillFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SelfSkills   
    skill_name = faker.word()
    level = random.choice(['INT', 'BEG', "EXP"])
    freelancer = factory.SubFactory(FreelancerFactory)

class SkillFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Skill
    name = faker.name()
    client = factory.SubFactory(ClientFactory)

#TODO faker.unique.first_name()
class JobPostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = JobPost
    user = factory.SubFactory(ClientFactory)
    # skill_required = factory.SubFactory(SkillFactory)
    description = faker.text()
    experience_required = faker.random_number()
    category = faker.name()
    title = faker.name()
    status = random.choice(['CLOSED', 'OPEN'])
    duration_type = random.choice(['MONTH','DAY','WEEK'])
    duration = faker.random_number(2)
    currency = random.choice(['RS', 'USD'])
    salary = faker.random_number()

    @factory.post_generation
    def skill_required(self, create, extracted, **kwargs):
        if not create or not extracted:
            # Simple build, or nothing to add, do nothing.
            return

        # Add the iterable of groups using bulk addition
        self.skill_required.add(extracted)

class JobProposalFactory(factory.django.DjangoModelFactory):
    
    class Meta:
        model = JobProposal
    job = factory.SubFactory(JobPostFactory)
    user = factory.SubFactory(FreelancerFactory)
    # resume = FAKER.txt_file(raw=True)
    resume = "/media/resumes/resum_1oyKKXO.txt"
    bid = faker.random_number()
    currency = random.choice(['RS', 'USD'])
    message = faker.text()

class ContractFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contract
    proposal = factory.SubFactory(JobProposalFactory)
    total = faker.random_number(3)
    currency = random.choice(['RS', 'USD'])
    remaining = total