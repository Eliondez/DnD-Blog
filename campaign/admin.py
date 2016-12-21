from django.contrib import admin
from .models import Campaign, Story

class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'rp_system', 'description', 'started', 'ended')
    search_fields = ['title', 'started']
    class Meta:
        model = Campaign

admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Story)

