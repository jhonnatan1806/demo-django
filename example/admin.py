from django.contrib import admin
from .models import CV
from .models import ScrapeResult
from .models import JobResult
# Register your models here.
admin.site.register(CV)
admin.site.register(ScrapeResult)
admin.site.register(JobResult)