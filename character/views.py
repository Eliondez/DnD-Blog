from django.shortcuts import render, get_object_or_404, redirect

from .models import Character
from .forms import CharacterForm
from campaign.models import Campaign
from campaign.views import MainContext



def char_detail(request, id=0):
    campaigns = Campaign.objects.filter(started__isnull=False)
    char = get_object_or_404(Character, id=id)
    #chars = Character.objects.all()
    panel = request.GET.get('panel', '1')
    print(panel)
    context = {
        'active_campaign_list': campaigns,
        'panel': panel,
        'char': char,
        #'section': 'chars'
    }
    return render(request, 'character/char_detail.html', context)

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
            # Create a new user object but avoid saving it yet
            form.save()
            return redirect('home')
    else:
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
    return redirect('home')

def char_create(request):
    campaigns = Campaign.objects.filter(started__isnull=False)
    title = 'Создание нового персонажа'
    button_text = 'Создать'
    if request.method == 'POST':
        form = CharacterForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new user object but avoid saving it yet
            char = form.save(commit=False)
            # Set the chosen password
            char.owner = request.user.profile
            char.exp = 0
            char.save()
            # Create the user profile
            return redirect('home')
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
