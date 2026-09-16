from django.contrib import admin
from core.models import Comment
# Register your models here.
class Commentadmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = '-empty-'
    list_display = ('title','author','status','published_date','created_date')
    list_filter = ('status','author')
    #ordering = ['published_date']
    search_fields = ['title','content']
admin.site.register(Comment,Commentadmin)

# Register your models here.
