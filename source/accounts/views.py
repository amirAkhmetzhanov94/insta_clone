from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import View, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from accounts.forms import RegistrationForm
from accounts.models import Profile


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "login.html")

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        return render(request, "login.html", {"has_error": True})


class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        user = profile.user
        posts = Post.objects.filter(author=user).order_by("created_on")

        followers = profile.followers.all()

        if len(followers) == 0:
            is_following = False

        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False

        number_of_followers = len(followers)

        context = {
            'user': user,
            'profile': profile,
            'posts': posts,
            'number_of_followers': number_of_followers,
            'is_following': is_following,
        }


class AddFollower(LoginRequiredMixin, View):
    def post(self, request, pk , *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        profile.followers.add(request.user)
        return redirect("profile", pk=profile.pk)


class RemoveFollower(LoginRequiredMixin,  View):
    def post(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        profile.followers.remove(request.user)
        return redirect("profile", pk=profile.pk)


class RegisterView(CreateView):
    model = User
    template_name = "register.html"
    form_class = RegistrationForm

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
        login(self.request, user)
        return redirect("index")


class UserDetailView(DetailView):
    model = User
    template_name = "user_detail.html"
    context_object_name = "user_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_detail'] = Profile.objects.all()
        return context


