from django.contrib import admin

from apps.research.models import ResearchArea, Publication

# Register your models here.
class ResearchAreaAdmin(admin.ModelAdmin):
	list_display = ('area', 'created_on')
	prepopulated_fields = {'slug': ('area',)}

class PublicationAdmin(admin.ModelAdmin):
	list_display = ('title', 'journal', 'pub_date', 'doi')
	list_filter = ('author',)
	search_fields = ['title', 'abstract', 'full_description']
	prepopulated_fields = {'slug': ('title',)}

admin.site.register(ResearchArea, ResearchAreaAdmin)
admin.site.register(Publication, PublicationAdmin)
