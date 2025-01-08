from django.urls import path
from .views import ListNoteView

urlpatterns = [
    path("", ListNoteView.as_view(), name = "list_note")
]