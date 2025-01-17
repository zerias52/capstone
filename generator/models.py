from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

# Create your models here.
class GeneratedPost(models.Model):
    # Stores generated social media posts and their parameters
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_on = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    PLATFORM_CHOICES = [
        ('LI', 'LinkedIn'),
        ('TW', 'Twitter'),
        ('IG', 'Instagram'),
        ('FB', 'Facebook'),
    ]
    platform = models.CharField(max_length=2, choices=PLATFORM_CHOICES)

    VOICE_CHOICES = [
        ('PRO', 'Professional'),
        ('CAS', 'Casual'),
        ('HUM', 'Humorous'),
        ('EDU', 'Educational'),
        ('INS', 'Inspirational'),
    ]
    brand_voice = models.CharField(max_length=3, choices=VOICE_CHOICES)

    target_audience = models.TextField()
    content_topic = models.TextField()
    call_to_action = models.CharField(max_length=25, blank =True)
    key_points = models.TextField()

    LENGTH_CHOICES = [
        ('S', 'Short'),
        ('M', 'Medium'),
        ('L', 'Long'),
    ]
    post_length = models.CharField(max_length=1, choices=LENGTH_CHOICES)

    ai_response = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['created_on']

    def parse_claude_response(self):
        """Format the content for display with line breaks and emojis preserved"""
        if not self.content:
            return ''
        return mark_safe(self.content.replace('\n', '<br>'))

    def __str__(self):
        return f"{self.get_platform_display()} post by {self.user.username} on {self.created_on.date()}"