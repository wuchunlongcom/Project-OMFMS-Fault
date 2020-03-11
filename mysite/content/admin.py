from django.contrib import admin
from content.models import Content, Type

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):    
    list_display = ('id','title','level')
   
@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):    
    list_display = ('id','name',)

