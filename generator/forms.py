from django import forms
from .models import GeneratedPost


class GeneratePostForm(forms.ModelForm):
    # Override text fields to use textarea widget with custom sizes
    content_topic = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control',
            'placeholder': 'What is the main subject or theme of your post?'
        })
    )

    target_audience = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 2,
            'class': 'form-control',
            'placeholder': 'Who is the intended audience for this post?'
        })
    )

    key_points = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'class': 'form-control',
            'placeholder': 'Enter key points or keywords to include (one per line)'
        })
    )

    call_to_action = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Optional: What action should readers take?'
        })
    )

    class Meta:
        model = GeneratedPost
        fields = [
            'platform',
            'content_topic',
            'brand_voice',
            'target_audience',
            'call_to_action',
            'key_points',
            'post_length'
        ]
        widgets = {
            'platform': forms.Select(attrs={'class': 'form-control'}),
            'brand_voice': forms.Select(attrs={'class': 'form-control'}),
            'post_length': forms.RadioSelect()
        }
        labels = {
            'platform': 'Target Platform',
            'content_topic': 'Content Topic/Theme',
            'brand_voice': 'Brand Voice/Tone',
            'target_audience': 'Target Audience',
            'call_to_action': 'Call to Action',
            'key_points': 'Key Points/Keywords',
            'post_length': 'Post Length'
        }

class SearchFilterForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Search posts...'
    }))
    platform = forms.ChoiceField(
        choices=[('', 'All Platforms')] + GeneratedPost.PLATFORM_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    voice = forms.ChoiceField(
        choices=[('', 'All Voices')] + GeneratedPost.VOICE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    sort = forms.ChoiceField(
        choices=[
            ('-created_on', 'Newest First'),
            ('created_on', 'Oldest First'),
            ('content_topic', 'Topic A-Z'),
            ('-content_topic', 'Topic Z-A'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )