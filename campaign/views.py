from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.views.generic.base import ContextMixin
from django.views.generic import ListView, TemplateView

from datetime import date

from character.models import Character
from .models import Story, Campaign


from .forms import CampaignForm, StoryForm

class MainContext(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(MainContext, self).get_context_data(**kwargs)
        context['active_campaign_list'] = Campaign.objects.filter(started__isnull=False)
        return context

class MainView(TemplateView, MainContext):
    template_name = 'base.html'

def main_view(request):
    campaigns = Campaign.objects.filter(started__isnull=False)
    context = {
        'active_campaign_list': campaigns,
    }
    return render(request, 'base.html', context)

def campaign_detail(request, id=0):
    campaigns = Campaign.objects.filter(started__isnull=False)
    campaign = get_object_or_404(Campaign, id=id)
    chars = campaign.character_set.all()
    available_chars = Character.objects.filter(campaign__isnull=True)
    can_edit = (request.user == campaign.master.user)
    panel = request.GET.get('panel', '1')
    context = {
        'panel': panel,
        'active_campaign_list': campaigns,
        'campaign': campaign,
        'chars': chars,
        'available_chars': available_chars,
        'can_edit': can_edit
    }
    return render(request, 'campaign/campaign_detail.html', context)

def campaign_edit(request, id=0):
    campaigns = Campaign.objects.filter(started__isnull=False)
    campaign = get_object_or_404(Campaign, id=id)
    if request.user != campaign.master.user:
        return redirect('/')
    title = 'Редактирование кампании'
    button_text = 'Обновить'
    if request.method == 'POST':
        form = CampaignForm(request.POST, instance=campaign)
        if form.is_valid():
            # Create a new user object but avoid saving it yet
            form.save()
            return redirect('home')
    else:
        form = CampaignForm(instance=campaign)
        context = {
            'active_campaign_list': campaigns,
            'form': form,
            'title': title,
            'btn_text': button_text,
        }
    return render(request, 'campaign/campaign_create.html', context)

def campaign_create(request):
    campaigns = Campaign.objects.filter(started__isnull=False)
    title = 'Создание новой кампании'
    button_text = 'Создать'
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            # Create a new user object but avoid saving it yet
            campaign = form.save(commit=False)
            # Set the chosen password
            campaign.master = request.user.profile
            campaign.save()
            # Create the user profile
            return redirect('home')
    else:
        form = CampaignForm()
        context = {
            'active_campaign_list': campaigns,
            'form': form,
            'title': title,
            'btn_text': button_text,
        }
    return render(request, 'campaign/campaign_create.html', context)


def campaign_start(request, id=0):
    campaign = get_object_or_404(Campaign, id=id)
    if request.user != campaign.master.user:
        return redirect('/')
    if campaign.started:
        return redirect('/')
    campaign.started = date.today()
    campaign.save()
    return redirect('home')


def campaign_end(request, id=0):
    campaign = get_object_or_404(Campaign, id=id)
    if request.user != campaign.master.user:
        return redirect('/')
    if campaign.ended:
        return redirect('/')
    campaign.ended = date.today()
    campaign.save()
    return redirect('home')


def add_char_to_campaign(request, campaign_id=0, character_id=0):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    char = get_object_or_404(Character, id=character_id)
    if char.campaign:
        return redirect('/')
    if request.user != campaign.master.user:
        return redirect('/')
    char.campaign = campaign
    char.save()
    url = reverse('campaign_detail', kwargs={'id': campaign.id}) + '?panel=2'
    return HttpResponseRedirect(url)


def rem_char_from_campaign(request, campaign_id=0, character_id=0):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    char = get_object_or_404(Character, id=character_id)
    if request.user != campaign.master.user:
        return redirect('/')
    if char.campaign == campaign:
        char.campaign = None
        char.save()
    url = reverse('campaign_detail', kwargs={'id': campaign.id}) + '?panel=2'
    return HttpResponseRedirect(url)


class CampaignStoryListView(ListView, MainContext):
    template_name = 'campaign/story_list.html'
    context_object_name = 'stories'
    # paginate_by = 2
    campaign = None

    def get(self, request, *args, **kwargs):
        self.campaign = Campaign.objects.get(pk = self.kwargs['campaign_id'])
        return super(CampaignStoryListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CampaignStoryListView, self).get_context_data(**kwargs)
        context['campaign'] = self.campaign
        return context

    def get_queryset(self):
        return Story.objects.filter(campaign=self.campaign).order_by('-ingamedate').select_related('campaign', 'campaign__master', 'campaign__master__user')


class CampaignStoryDetailView(TemplateView):
    template_name = 'campaign/story_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CampaignStoryDetailView, self).get_context_data(**kwargs)
        try:
            context['pn'] = self.request.GET['page']
        except:
            context['pn'] = 1

        context['story'] = get_object_or_404(Story, pk = kwargs['story_id'])
        context['active_campaign_list'] = Campaign.objects.filter(started__isnull=False)
        return context


def create_story(request, campaign_id=0):
    campaigns = Campaign.objects.filter(started__isnull=False)
    title = 'Новая история'
    button_text = 'Создать'
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            # Create a new user object but avoid saving it yet
            story = form.save(commit=False)
            # Set the chosen password
            campaign = Campaign.objects.get(id=campaign_id)
            story.campaign = campaign
            story.save()
            # Create the user profile
            return redirect('story_list', campaign_id=campaign.id)
    else:
        form = StoryForm()
        context = {
            'active_campaign_list': campaigns,
            'form': form,
            'title': title,
            'btn_text': button_text,
        }
    return render(request, 'campaign/story_create.html', context)

def edit_story(request, campaign_id=0, story_id=0):
    campaigns = Campaign.objects.filter(started__isnull=False)
    story = get_object_or_404(Story, id=story_id)
    campaign = get_object_or_404(Campaign, id=campaign_id)
    title = 'Ректирование истории'
    button_text = 'Обновить'
    if request.method == 'POST':
        form = StoryForm(request.POST, instance=story)
        if form.is_valid():
            form.save()
            return redirect('story_list', campaign_id=campaign.id)
    else:
        form = StoryForm(instance=story)
        context = {
            'active_campaign_list': campaigns,
            'form': form,
            'title': title,
            'btn_text': button_text,
        }
    return render(request, 'campaign/story_create.html', context)

class CreateStory(CreateView):
    template_name = 'campaign/story_create.html'
    model = Story
    fields = ['title']

class DeleteStory(ListView):
    pass

class EditStory(ListView):
    pass