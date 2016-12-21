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
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
#from bolders import views
from character.views import char_edit, char_create, char_detail, char_delete
from campaign import views
from accounts.views import login_view, register_view, logout_view, home_view

urlpatterns = [
    url(r'^character/(?P<id>\d+)/edit/$', char_edit, name='char_edit'),
    url(r'^character/(?P<id>\d+)/delete/$', char_delete, name='char_delete'),
    url(r'^character/(?P<id>\d+)/$', char_detail, name='char_detail'),
    url(r'^character/create/', char_create, name='char_create'),

    # url(r'^campaign/(?P<campaign_id>\d+)/addchar/(?P<character_id>\d+)/', views.add_char_to_campaign, name='add_char_to_campaign'),
    # url(r'^campaign/(?P<campaign_id>\d+)/removechar/(?P<character_id>\d+)/', views.rem_char_from_campaign, name='rem_char_from_campaign'),
    # url(r'^campaign/(?P<id>\d+)/detail/', views.campaign_detail, name='campaign_detail'),
    # url(r'^campaign/(?P<id>\d+)/end/', views.campaign_end, name='campaign_end'),
    # url(r'^campaign/(?P<id>\d+)/start/', views.campaign_start, name='campaign_start'),
    # url(r'^campaign/(?P<id>\d+)/edit/', views.campaign_edit, name='campaign_edit'),
    # url(r'^campaign/create/', views.campaign_create, name='campaign_create'),
    url(r'^campaign/', include('campaign.urls')),

    url(r'^bolders/', include('bolders.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^account/', home_view, name='home'),
    url(r'^login/', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^register/', register_view, name='register'),
    url(r'^$', views.MainView.as_view(), name='mainview'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

