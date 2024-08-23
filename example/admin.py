from django.contrib import admin
from .models import CV
from .models import ScrapeResult

# Register your models here.
admin.site.register(CV)
admin.site.register(ScrapeResult)
