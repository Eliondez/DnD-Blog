from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, TemplateView, DetailView, View
from django.http import JsonResponse

from .models import Character
from .forms import CharacterForm
from campaign.models import Campaign
from campaign.views import MainContext



class CharacterDetail(TemplateView, MainContext):
    template_name = 'character/char_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CharacterDetail, self).get_context_data(**kwargs)
        context['panel'] = self.request.GET.get('panel', '1')
        context['char'] = get_object_or_404(Character, id=kwargs['id'])
        context['available_chars'] = Character.objects.filter(campaign__isnull=True)
        context['owner'] = (self.request.user == context['char'].owner.user)
        if context['char'].campaign:
            context['master'] = (self.request.user == context['char'].campaign.master.user)
        return context
#
# def char_detail(request, id=0):
#     campaigns = Campaign.objects.filter(started__isnull=False)
#     #chars = Character.objects.all()
#     panel = request.GET.get('panel', '1')
#     context = {
#         'active_campaign_list': campaigns,
#         'panel': panel,
#         'char': char,
#     }
#     return render(request, 'character/char_detail.html', context)


class UpdatePrivateStats(View):
    def post(self, *args, **kwargs):
        char = get_object_or_404(Character, pk=kwargs['id'])
        usr = self.request.user
        if usr != char.owner.user or usr != char.campaign.master.user:
            return JsonResponse({}, status=500)
        char.private_stats = self.request.POST['text']
        char.save()
        return JsonResponse({
            'id': char.id,
            'text': char.private_stats,
        })

class UpdateDMNotes(View):
    def post(self, *args, **kwargs):
        char = get_object_or_404(Character, pk=kwargs['id'])
        usr = self.request.user
        if usr != char.campaign.master.user:
            return JsonResponse({}, status=500)
        char.masters_notes = self.request.POST['text']
        char.save()
        return JsonResponse({
            'id': char.id,
            'text': char.masters_notes,
        })

def char_edit(request, id=0):
    campaigns = Campaign.objects.filter(started__isnull=False)
    char = get_object_or_404(Character, id=id)
    if request.user != char.owner.user:
        return redirect('/')
    title = 'Редактирование персонажа'
    button_text = 'Обновить'
    if request.method == 'POST':
        form = CharacterForm(request.POST, request.FILES, instance=char)
        if form.is_valid():
            form.save()
            return redirect('accounts:home')

    form = CharacterForm(instance=char)
    context = {
        'active_campaign_list': campaigns,
        'form': form,
        'title': title,
        'btn_text': button_text,
    }
    return render(request, 'character/char_create.html', context)

def char_delete(request, id=0):
    char = get_object_or_404(Character, id=id)
    if request.user != char.owner.user:
        return redirect('/')
    char.delete()
    return redirect('accounts:home')

def char_create(request):
    campaigns = Campaign.objects.filter(started__isnull=False)
    title = 'Создание нового персонажа'
    button_text = 'Создать'
    if request.method == 'POST':
        form = CharacterForm(request.POST, request.FILES)
        if form.is_valid():
            char = form.save(commit=False)
            char.owner = request.user.profile
            char.exp = 0
            char.save()
            # Create the user profile
            return redirect('accounts:home')
    else:
        form = CharacterForm()
        context = {
            'active_campaign_list': campaigns,
            'form': form,
            'title': title,
            'btn_text': button_text,
        }
    return render(request, 'character/char_create.html', context)

# Create your views here.
