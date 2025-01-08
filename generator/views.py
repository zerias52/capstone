from django.views.generic import ListView
from .models import GeneratedPost

# Create your views here.
class PostListView(ListView):
    template_name = "generator/post_list.html"
    model = GeneratedPost
    context_object_name = "post_list"

