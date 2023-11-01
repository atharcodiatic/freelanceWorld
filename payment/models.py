from django.db import models
from jobs.models  import * 
# Create your models here.

class Transaction(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.PROTECT)
    amount = models.PositiveIntegerField()
    created_at =  models.DateTimeField(auto_now_add = True)

    def __str__(self) -> str:
        return self.contract.proposal.job.user.username
    