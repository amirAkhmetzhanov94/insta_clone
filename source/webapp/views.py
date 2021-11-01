from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from webapp.models import Post, Comment
from webapp.forms import PostForm


class IndexView(ListView):
    model = Post
    template_name = "index.html"


class PostCreateView(CreateView):
    model = Post
    template_name = "create_post.html"
    form_class = PostForm


class PostDetailView(DetailView):
    model = Post
    template_name = "detail_post.html"


class PostUpdateView(UpdateView):
    model = Post
    template_name = "update.html"
    form_class = PostForm

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.get_object().pk})


class PostDeleteView(DeleteView):
    model = Post
    template_name = "delete_post.html"
    success_url = reverse_lazy("user_detail")


class PostCommentCreateView(CreateView):
    model = Comment
    fields = ["text"]

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return redirect("user_detail", kwargs={"pk": post.pk})