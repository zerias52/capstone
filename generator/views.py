from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import GeneratedPost
from .forms import GeneratePostForm, SearchFilterForm
from .services import generate_social_post

# Create your views here.
class PostListView(LoginRequiredMixin, ListView):
    template_name = "generator/post_list.html"
    model = GeneratedPost
    context_object_name = "post_list"
    paginate_by = 10

    def get_queryset(self):
        queryset = GeneratedPost.objects.filter(user=self.request.user)

        # Search functionality
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(content_topic__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(key_points__icontains=search_query)
            )

        # Filter by platform
        platform = self.request.GET.get('platform', '')
        if platform:
            queryset = queryset.filter(platform=platform)

        # Filter by brand voice
        voice = self.request.GET.get('voice', '')
        if voice:
            queryset = queryset.filter(brand_voice=voice)

        # Filter by date range
        date_from = self.request.GET.get('date_from', '')
        date_to = self.request.GET.get('date_to', '')
        if date_from:
            queryset = queryset.filter(created_on__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_on__lte=date_to)

        # Sort functionality
        sort_by = self.request.GET.get('sort', '-created_on')
        queryset = queryset.order_by(sort_by)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchFilterForm(self.request.GET)
        return context

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

        # Save the post
        self.object = form.save()

        return redirect('generator:post-detail', pk=self.object.pk)

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


class PostCloneView(LoginRequiredMixin, CreateView):
    model = GeneratedPost
    form_class = GeneratePostForm
    template_name = 'generator/post_clone.html'
    success_url = reverse_lazy('generator:post-list')

    def get_initial(self):
        # Get the original post
        original_post = GeneratedPost.objects.get(pk=self.kwargs['pk'])
        # Pre-populate the form with original post's data
        return {
            'platform': original_post.platform,
            'content_topic': original_post.content_topic,
            'brand_voice': original_post.brand_voice,
            'target_audience': original_post.target_audience,
            'call_to_action': original_post.call_to_action,
            'key_points': original_post.key_points,
            'post_length': original_post.post_length,
        }

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

        form.instance.content = generated_content
        self.object = form.save()

        return redirect('generator:post-detail', pk=self.object.pk)