from django.contrib import admin

# Register your models here.
from .models import File, Prompts

admin.site.register(File)
admin.site.register(Prompts)
