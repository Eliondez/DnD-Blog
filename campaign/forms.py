from django import forms
from .models import Campaign, Story

class CampaignForm(forms.ModelForm):
    title = forms.CharField(label='Название', widget=forms.TextInput(attrs={'class': 'form-control'}))
    PR_SYSTEM_CHOICES = (
        ('no', 'None'),
        ('gp', 'GURPS'),
        ('d5e', 'DnD 5e'),
    )
    rp_system = forms.CharField(label='Ролевая система', widget=forms.Select(choices=PR_SYSTEM_CHOICES))
    description = forms.CharField(label='Описание', widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Campaign
        fields = [
            'title',
            'rp_system',
            'description',
        ]

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = [
            'title',
            'content',
            'ingamedate',
        ]
        widgets = {
            'ingamedate': forms.SelectDateWidget(),
        }
