from django.db import models

# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=80)
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"