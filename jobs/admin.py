from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Contract)
admin.site.register(JobPost)
admin.site.register(Review)
admin.site.register(JobProposal)
