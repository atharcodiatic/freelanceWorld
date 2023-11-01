from django.db import models

# Create your models here.
from accounts.models import Client , Freelancer ,CustomUser , Skill
from django.core.validators import FileExtensionValidator


# class JobSkill(models.Model):
#     name = models.CharField(max_length=40)
#     created_at = models.DateTimeField(auto_now_add = True)
#     updated_at = models.DateTimeField(auto_now=True)

class JobPost(models.Model):

    '''
    Client can Post multiple jobs , This Model stores info about jobs.
    '''
    JOB_STATUS = [
        ('OPEN', 'OPEN'),
        ('CLOSED', 'CLOSED'),
    ]

    DURATION_CHOICES = [
                       ('DAY' , 'DAY'), 
                       ('WEEK' , 'WEEK'),
                       ('MONTH' , 'MONTH'),
                       
                       ] 
    CURRENCY_CHOICES = [
        ('RS','RUPPEES'),
        ('USD','DOLLAR')
    ]

    title = models.CharField(max_length=200)

    category = models.CharField(max_length=50)
    experience_required = models.PositiveIntegerField()

    description = models.TextField()

    user = models.ForeignKey(Client, on_delete = models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add = True)
    status = models.CharField(max_length = 10, choices = JOB_STATUS,  default=JOB_STATUS[1][0])
    duration_type = models.CharField( max_length=10, choices = DURATION_CHOICES,)
    duration = models.PositiveIntegerField(null=True, help_text = 'duration must be an integer')
    currency = models.CharField(max_length=3,choices=CURRENCY_CHOICES)
    salary = models.PositiveIntegerField(help_text = 'job salary per hour')
    skill_required = models.ManyToManyField(Skill)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)

    
    class Meta:
        verbose_name = 'Post'

    def __str__(self):
        return self.title
    

     
    
class JobProposal(models.Model):
    '''
    This model store data of JobProposal , User can send to client to get job
    '''

    PROPASAL_STATUS =[
        ('ACCEPTED' , 'ACCEPTED'),
        ('INPROCESS' , 'INPROCESS'),
        ('DENIED' , 'DENIED'),
    ]
    CURRENCY_CHOICES = [
        ('RS','RUPPEES'),
        ('USD','DOLLAR'),
    ]

    job = models.ForeignKey(JobPost , on_delete = models.CASCADE)
    user = models.ForeignKey(Freelancer , on_delete = models.CASCADE)
    status = models.CharField(max_length = 10, choices = PROPASAL_STATUS,
                                       default=PROPASAL_STATUS[1][0])
    resume = models.FileField(upload_to='certificates/',
                        validators=[FileExtensionValidator(
                        allowed_extensions = ['pdf','txt','doc'],
                        message = 'only pdf, txt, doc extensions allowed')])
    
    bid  = models.PositiveIntegerField()
    currency = models.CharField(max_length=3,choices=CURRENCY_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.status
    

class Contract(models.Model):

    '''
    Contract model stores payment details , job payment deals between 
    client and freelancer

    '''
    proposal = models.OneToOneField(JobProposal, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add = True)
    
    total = models.PositiveIntegerField()
    currency = models.CharField(max_length=7)
    remaining = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.proposal.job.user.username} - {self.proposal.user.username}"  

class Transaction(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.PROTECT)
    amount = models.PositiveIntegerField()
    

'''
logic model not useful for project 
class ClientReviews(models.Model):

    
    rating_from  = models.ForeignKey(Freelancer, on_delete = models.CASCADE)
    rating_to = models.OneToOneField(JobPost , on_delete=models.CASCADE)
    review_rating  = models.IntegerField(max_length = 25)
    review_message = models.TextField()

    def __str__(self):
        return self.review_rating
    class Meta:
        managed = False
        
'''
    
class Review(models.Model):
    """
    Clients can review Freelancer and Freelancer can review Client 
    """
    rating_by = models.ForeignKey(CustomUser , on_delete = models.CASCADE, related_name='rated_by')
    rating_to = models.ForeignKey(CustomUser , on_delete = models.CASCADE, related_name='rating_to')
    star_rating = models.PositiveIntegerField(default = 0)
    review_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)
    job = models.OneToOneField(JobPost,on_delete = models.CASCADE)
    # connect with job

    def __str__(self) -> str:
        return str(self.star_rating) 
    

