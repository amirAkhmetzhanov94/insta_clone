from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import ModelFormMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from webapp.models import Post, Comment
from webapp.forms import PostForm, CommentForm


class LikeGateway(LoginRequiredMixin, View):
    post_obj = None

    def dispatch(self, request, *args, **kwargs):
        self.post_obj = get_object_or_404(Post, pk=kwargs.get('pk'))
        return super(LikeGateway, self).dispatch(request, *args, **kwargs)

    def set_like(self):
        self.post_obj.likes.add(self.request.user)

    def remove_like(self):
        self.post_obj.likes.remove(self.request.user)

    def post(self, request, *args, **kwargs):
        if request.user in self.post_obj.likes.all():
            self.remove_like()
        else:
            self.set_like()
        return redirect(request.META.get('HTTP_REFERER'))


class IndexView(LoginRequiredMixin, ListView, ModelFormMixin):
    model = Post
    template_name = "index.html"
    ordering = "-created_on"
    form_class = CommentForm
    object = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts_list = []
        for post in Post.objects.all().order_by("-created_on"):
            if post.author in self.request.user.profile.following.all():
                posts_list.append(post)
        context['posts_list'] = posts_list
        return context

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, **kwargs):
        post_id = request.POST.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        self.form = self.get_form(self.form_class)
        if self.form.is_valid():
            post.comments.create(author=request.user, text=self.form.clean().get("text"))
            return redirect("detail_post", pk=post.pk)
        else:
            return render(request, "detail_post.html", {"error": self.form.errors, "post": post,
                                                        "form": self.form_class})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "create_post.html"
    form_class = PostForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return redirect("index")


class PostDetailView(LoginRequiredMixin, DetailView, ModelFormMixin):
    model = Post
    template_name = "detail_post.html"
    form_class = CommentForm

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        return DetailView.get(self, request, *args, **kwargs)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "update.html"
    form_class = PostForm

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.get_object().pk})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "delete_post.html"
    success_url = reverse_lazy("user_detail")


class PostCommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ["text"]

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return redirect("detail_post", kwargs={"pk": post.pk})
