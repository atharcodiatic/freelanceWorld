from django.contrib import admin

# Register your models here.
from .models import *
from django.contrib import admin


admin.site.register(Contract)
admin.site.register(JobPost)
admin.site.register(Review)
admin.site.register(JobProposal)
