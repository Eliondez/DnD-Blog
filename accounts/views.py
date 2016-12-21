from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )
from django.shortcuts import render, redirect
from django.http import request, HttpResponse
from .forms import UserLoginForm, UserRegisterForm
from accounts.models import Profile
from django.contrib.auth.decorators import login_required
from campaign.models import Campaign
from character.models import Character


@login_required
def home_view(request):
    char_list = Character.objects.filter(owner=request.user.profile).select_related('campaign')
    campaign_list = Campaign.objects.filter(master=request.user.profile)
    campaigns = Campaign.objects.filter(started__isnull=False)
    context = {
        'char_list': char_list,
        'campaign_list': campaign_list,
        'active_campaign_list': campaigns,
    }
    return render(request, 'accounts/home.html', context)

def login_view(request):
    campaigns = Campaign.objects.filter(started__isnull=False)
    if request.method == 'POST':
        title = 'Вход на сайт'
        button_text = 'Войти'
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if not user:
                return HttpResponse('Invalid login')
            login(request, user)
            return redirect('/account')
        context = {
            'form': form,
            'title': title,
            'btn_text': button_text,
            'active_campaign_list': campaigns,
        }
        return render(request, 'accounts/form.html', context)
    elif request.method == 'GET':
        title = 'Вход на сайт'
        button_text = 'Войти'
        form = UserLoginForm()
        context = {
            'form': form,
            'title': title,
            'btn_text': button_text,
            'active_campaign_list': campaigns,
        }
        return render(request, 'accounts/form.html', context)

def register_view(request):
    campaigns = Campaign.objects.filter(started__isnull=False)
    title = 'Создание нового аккаунта'
    button_text = 'Создать'
    form = UserRegisterForm(request.POST or None)
    context = {
        'form': form,
        'title': title,
        'btn_text': button_text,
        'active_campaign_list': campaigns,
    }
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = form.save(commit=False)
            # Set the chosen password
            new_user.set_password(form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            profile = Profile.objects.create(user=new_user)
            login(request, new_user)
            return redirect('/')
    else:
        form = UserRegisterForm()
        context = {
            'form': form,
            'title': title,
            'btn_text': button_text,
            'active_campaign_list': campaigns,
        }
    return render(request, 'accounts/form.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')
