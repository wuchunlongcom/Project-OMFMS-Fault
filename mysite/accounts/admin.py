from django.contrib import admin
from .models import  Project, Contact

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):    
    list_display = ('id','name','description')
   
@admin.register(Contact)
class ContacttAdmin(admin.ModelAdmin):    
    list_display = ('id','name','email')

