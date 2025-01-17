from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import GeneratedPost
from .forms import GeneratePostForm
from .services import generate_social_post

# Create your views here.
class PostListView(ListView):
    template_name = "generator/post_list.html"
    model = GeneratedPost
    context_object_name = "post_list"
    paginate_by = 10

    def get_queryset(self):
        return GeneratedPost.objects.filter(user=self.request.user).order_by('-created_on')

class PostCreateView(LoginRequiredMixin, CreateView):
    model = GeneratedPost
    form_class = GeneratePostForm
    template_name = 'generator/post_create.html'
    success_url = reverse_lazy('generator:post-list')

    def form_valid(self, form):
        form.instance.user = self.request.user

        generated_content = generate_social_post(
            platform=form.instance.get_platform_display(),
            content_topic=form.instance.content_topic,
            brand_voice=form.instance.get_brand_voice_display(),
            target_audience=form.instance.target_audience,
            call_to_action=form.instance.call_to_action,
            key_points=form.instance.key_points,
            post_length=form.instance.get_post_length_display()
        )

        # Set the generated content
        form.instance.content = generated_content

        return super().form_valid(form)

class PostDetailView(LoginRequiredMixin, DetailView):
    model = GeneratedPost
    template_name = 'generator/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return GeneratedPost.objects.filter(user=self.request.user)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = GeneratedPost
    template_name = 'generator/post_delete.html'
    success_url = reverse_lazy('generator:post-list')
    context_object_name = 'post'

    def get_queryset(self):
        return GeneratedPost.objects.filter(user=self.request.user)