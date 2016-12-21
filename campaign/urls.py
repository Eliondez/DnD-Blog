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

#campaign/
urlpatterns = [
    url(r'^(?P<campaign_id>\d+)/addchar/(?P<character_id>\d+)/', views.add_char_to_campaign, name='add_char_to_campaign'),
    url(r'^(?P<campaign_id>\d+)/removechar/(?P<character_id>\d+)/', views.rem_char_from_campaign, name='rem_char_from_campaign'),
    url(r'^(?P<campaign_id>\d+)/deletestory/(?P<story_id>\d+)/', views.DeleteStory.as_view(), name='delete_story'),
    url(r'^(?P<campaign_id>\d+)/editstory/(?P<story_id>\d+)/', views.edit_story, name='edit_story'),
    url(r'^(?P<campaign_id>\d+)/createstory/', views.create_story, name='create_story'),
    url(r'^(?P<campaign_id>\d+)/$', views.CampaignStoryListView.as_view(), name='story_list'),
    url(r'^(?P<id>\d+)/detail/', views.campaign_detail, name='campaign_detail'),
    url(r'^(?P<id>\d+)/end/', login_required(views.campaign_end), name='campaign_end'),
    url(r'^(?P<id>\d+)/start/', login_required(views.campaign_start), name='campaign_start'),
    url(r'^(?P<id>\d+)/edit/', views.campaign_edit, name='campaign_edit'),
    url(r'^create/', login_required(views.campaign_create), name='campaign_create'),
    # url(r'^', include('campaign.urls')),
]
