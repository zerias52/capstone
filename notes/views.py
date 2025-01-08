from django.views.generic import ListView
from .models import Note

# Create your views here.
class ListNoteView(ListView):
    template_name = "notes/list_note.html"
    model = Note