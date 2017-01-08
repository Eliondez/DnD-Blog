from django.contrib import admin
from .models import Campaign, Story

class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'rp_system', 'description', 'started', 'ended')
    search_fields = ['title', 'started']
    class Meta:
        model = Campaign

class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'ingamedate', 'posted', 'campaign')
    search_fields = ['title', 'content']
    list_editable = ['ingamedate']
    list_filter = ['campaign']
    actions_on_bottom = True
    #fields = (('title','ingamedate'), 'content', ('tags', 'campaign'))
    class Meta:
        model = Story

admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Story, StoryAdmin)

