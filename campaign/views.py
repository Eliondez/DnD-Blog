from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import ContextMixin, RedirectView
from django.views.generic import ListView, TemplateView, DetailView, View
from django.utils import formats
from django.http import JsonResponse
from django.db.models import Count
from datetime import date

from character.models import Character
from .models import Story, Campaign, CampaignMap
import logging

logger = logging.getLogger(__name__)

class MainContext(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(MainContext, self).get_context_data(**kwargs)
        context['active_campaign_list'] = Campaign.objects.filter(started__isnull=False)
        return context


class MainView(TemplateView, MainContext):
    template_name = 'base.html'


class CampaignDetail(TemplateView, MainContext):
    template_name = 'campaign/campaign_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CampaignDetail, self).get_context_data(**kwargs)
        context['panel'] = self.request.GET.get('panel', '1')
        context['campaign'] = get_object_or_404(Campaign, id=kwargs['id'])
        context['chars'] = context['campaign'].character_set.all()
        context['available_chars'] = Character.objects.filter(campaign__isnull=True)
        context['can_edit'] = (self.request.user == context['campaign'].master.user)
        context['maps'] = CampaignMap.objects.filter(campaign=context['campaign'])
        return context


class CampaignCreate(CreateView, MainContext):
    model = Campaign
    template_name = 'campaign/campaign_create.html'
    fields = ['title', 'rp_system', 'description']

    def form_valid(self, form):
        campaign = form.save(commit=False)
        campaign.master = self.request.user.profile
        campaign.save()
        return redirect(campaign)


class CampaignEdit(UpdateView, MainContext):
    model = Campaign
    template_name = 'campaign/campaign_create.html'
    pk_url_kwarg = 'id'
    fields = ['title', 'rp_system', 'description']

    def get(self, request, *args, **kwargs):
        if request.user != Campaign.objects.get(id=self.kwargs['id']).master.user:
            return redirect('accounts:home')
        return super(CampaignEdit, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user != Campaign.objects.get(id=self.kwargs['id']).master.user:
            return redirect('accounts:home')
        return super(CampaignEdit, self).post(request, *args, **kwargs)


class CampaignStart(View):
    def post(self, *args, **kwargs):
        campaign = get_object_or_404(Campaign, pk=kwargs['id'])
        if self.request.user != campaign.master.user or campaign.started:
            return JsonResponse({
            'status': 'fail',
            })
        print(self.request.user.username)
        campaign.started = date.today()
        campaign.save()
        return JsonResponse({
            'status': 'ok',
            'date': formats.date_format(date.today(), "DATE_FORMAT")
        })


class CampaignEnd(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        campaign = get_object_or_404(Campaign, id=kwargs['id'])
        if self.request.user != campaign.master.user or campaign.started:
            return redirect('accounts:home')
        campaign.ended = date.today()
        campaign.save()
        return reverse('accounts:home')

class CampaignDelay(View):
    def post(self, *args, **kwargs):
        campaign = get_object_or_404(Campaign, pk=kwargs['id'])
        if self.request.user != campaign.master.user:
            return JsonResponse({}, status=500)
        if not campaign.ended:
            campaign.ended = date.today()
            campaign.save()
            return JsonResponse({
            'status': 'delayed',
            'date': formats.date_format(date.today(), "DATE_FORMAT")
            })
        if campaign.ended:
            campaign.ended = None
            campaign.save()
            return JsonResponse({
            'status': 'resumed',
            })


class AddCharToCampaignView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        campaign = get_object_or_404(Campaign, id=kwargs['campaign_id'])
        char = get_object_or_404(Character, id=kwargs['character_id'])
        if char.campaign:
            return redirect('/')
        if not self.request.user == campaign.master.user:
            return redirect('/')
        char.campaign = campaign
        char.save()
        my_url = reverse('campaign:campaign_detail', kwargs={'id': campaign.id}) + '?panel=2'
        return my_url


class LeaveCampaignView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        campaign = get_object_or_404(Campaign, id=kwargs['campaign_id'])
        char = get_object_or_404(Character, id=kwargs['character_id'])
        if not char.campaign:
            return redirect('/')
        if not self.request.user == campaign.master.user or not self.request.user == char.owner.user:
            return redirect('/')
        char.campaign = None
        char.save()
        my_url = reverse('campaign:campaign_detail', kwargs={'id': campaign.id}) + '?panel=2'
        return my_url


class CampaignStoryListView(ListView, MainContext):
    template_name = 'campaign/story_list.html'
    context_object_name = 'stories'
    paginate_by = 5
    campaign = None

    def get(self, request, *args, **kwargs):
        self.campaign = Campaign.objects.get(pk = self.kwargs['campaign_id'])
        return super(CampaignStoryListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CampaignStoryListView, self).get_context_data(**kwargs)
        context['campaign'] = self.campaign
        return context

    def get_queryset(self):
        stories = Story.objects.filter(campaign=self.campaign).select_related('campaign', 'campaign__master', 'campaign__master__user').prefetch_related('tagged_items__tag')
        try:
            stories = stories.filter(tags__name = self.request.GET['tag'])
        except:
            pass
        return stories


class CampaignStoryDetailView(TemplateView, MainContext):
    template_name = 'campaign/story_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CampaignStoryDetailView, self).get_context_data(**kwargs)
        context['pn'] = self.request.GET.get('page', '1')
        context['story'] = get_object_or_404(Story.objects.select_related('campaign', 'campaign__master', 'campaign__master__user').prefetch_related('tagged_items__tag'), id=kwargs['story_id'])
        return context


class StoryCreate(CreateView, MainContext):
    model = Story
    template_name = 'campaign/story_create.html'
    fields = ['title', 'content', 'ingamedate', 'tags']

    def form_valid(self, form):
        campaign = get_object_or_404(Campaign, pk=self.kwargs['campaign_id'])
        if campaign.master != self.request.user.profile:
            return redirect('accounts:home')
        story = form.save(commit = False)
        story.campaign = campaign
        story.save()
        if not campaign.started:
            campaign.started = story.posted
        campaign.ended = story.posted
        campaign.save()
        return redirect(story)


class StoryEdit(UpdateView, MainContext):
    model = Story
    template_name = 'campaign/story_create.html'
    fields = ['title', 'content', 'ingamedate', 'tags']
    pk_url_kwarg = 'story_id'

    def post(self, request, *args, **kwargs):
        if not request.user == Story.objects.get(id=self.kwargs['story_id']).campaign.master.user:
            return redirect('accounts:home')
        # return redirect('campaign:story_list', campaign_id=self.kwargs['campaign_id'])
        return super(StoryEdit, self).post(request, *args, **kwargs)

class StoryDelete(DeleteView):
    model = Story
    pk_url_kwarg = 'story_id'

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_object(self, queryset=None):
        obj = super(StoryDelete, self).get_object()
        if not obj.campaign.master == self.request.user.profile:
            return redirect('accounts:home')
        return obj

    def get_success_url(self):
        return reverse('campaign:story_list', kwargs={'campaign_id': self.kwargs['campaign_id']})
