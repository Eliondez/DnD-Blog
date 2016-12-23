from django import forms
from .models import Campaign, Story

class CampaignForm(forms.ModelForm):
    PR_SYSTEM_CHOICES = (
        ('no', 'None'),
        ('gp', 'GURPS'),
        ('d5e', 'DnD 5e'),
    )
    class Meta:
        model = Campaign
        fields = [
            'title',
            'rp_system',
            'description',
        ]
        labels = {
            'title': 'Название',
            'rp_system': 'Ролевая система',
            'description': 'Описание',
        }

class StoryForm(forms.ModelForm):

    class Meta:
        YEARS = [i for i in range(1, 2300)]
        model = Story
        fields = [
            'title',
            'content',
            'ingamedate',
        ]
        labels = {
            'title': 'Название',
            'content': 'Текст',
            'ingamedate': 'Дата',
        }
        widgets = {
            'ingamedate': forms.SelectDateWidget(years=YEARS),
        }
