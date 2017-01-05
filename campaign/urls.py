"""dndblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'campaign'
#campaign/
urlpatterns = [
    url(r'^(?P<campaign_id>\d+)/addchar/(?P<character_id>\d+)/', login_required(views.AddCharToCampaignView.as_view()), name='add_char_to_campaign'),
    url(r'^(?P<campaign_id>\d+)/removechar/(?P<character_id>\d+)/', login_required(views.LeaveCampaignView.as_view()), name='rem_char_from_campaign'),
    url(r'^(?P<campaign_id>\d+)/(?P<story_id>\d+)/delete/', login_required(views.StoryDelete.as_view()), name='delete_story'),
    url(r'^(?P<campaign_id>\d+)/(?P<story_id>\d+)/edit/', login_required(views.StoryEdit.as_view()), name='edit_story'),
    url(r'^(?P<campaign_id>\d+)/(?P<story_id>\d+)/', views.CampaignStoryDetailView.as_view(), name='detail_story'),
    url(r'^(?P<campaign_id>\d+)/createstory/', login_required(views.StoryCreate.as_view()), name='create_story'),
    url(r'^(?P<campaign_id>\d+)/$', views.CampaignStoryListView.as_view(), name='story_list'),

    url(r'^ajax/$', views.AjaxTest.as_view(), name='ajax'),

    url(r'^(?P<id>\d+)/detail/', views.CampaignDetail.as_view(), name='campaign_detail'),
    url(r'^(?P<id>\d+)/end/', login_required(views.CampaignEnd.as_view()), name='campaign_end'),
    url(r'^(?P<id>\d+)/delay/', login_required(views.CampaignDelay.as_view()), name='campaign_delay'),
    url(r'^(?P<id>\d+)/start/', login_required(views.CampaignStart.as_view()), name='campaign_start'),
    url(r'^(?P<id>\d+)/edit/', login_required(views.CampaignEdit.as_view()), name='campaign_edit'),
    url(r'^create/', login_required(views.CampaignCreate.as_view()), name='campaign_create'),
    # url(r'^', include('campaign.urls')),
]
