from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import View, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from accounts.forms import UserRegistrationForm, ProfileRegistrationForm
from accounts.models import Profile
from instagram import settings
from webapp.models import Post


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


class LogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect(settings.LOGOUT_REDIRECT_URL)


class FollowGateway(View):
    user_obj = None

    def dispatch(self, request, *args, **kwargs):
        self.user_obj = get_object_or_404(Profile, pk=kwargs.get('pk'))
        return super(FollowGateway, self).dispatch(request, *args, **kwargs)

    def set_follow(self):
        self.user_obj.followers.add(self.request.user)

    def remove_follow(self):
        self.user_obj.followers.remove(self.request.user)

    def post(self, request, *args, **kwargs):
        if request.user in self.user_obj.followers.all():
            print(1)
            self.remove_follow()
        else:
            print(2)
            self.set_follow()
        return redirect(request.META.get('HTTP_REFERER'))


class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "register.html"
    context_object_name = "users_obj"

    def get_profile_form(self):
        form_kwargs = {}
        if self.request.method == "POST":
            form_kwargs["data"] = self.request.POST
            form_kwargs["files"] = self.request.FILES
        return ProfileRegistrationForm(**form_kwargs)

    def post(self, request, *args, **kwargs):
        user_form = self.get_form()
        profile_form = self.get_profile_form()
        if user_form.is_valid() and profile_form.is_valid():
            return self.form_valid(user_form, profile_form)
        else:
            return self.form_invalid(user_form, profile_form)

    def form_valid(self, user_form, profile_form):
        result = super(RegisterView, self).form_valid(user_form)
        profile_form.instance.user = self.object
        profile_form.save()
        return result

    def form_invalid(self, user_form, profile_form):
        context = self.get_context_data(user_form=user_form, profile_form=profile_form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        if "profile_form" not in kwargs:
            kwargs["profile_form"] = self.get_profile_form()
            kwargs["user_form"] = self.form_class()
        return super(RegisterView, self).get_context_data(**kwargs)

    def get_success_url(self):
        return reverse("index")


class UserDetailView(DetailView):
    model = User
    template_name = "user_detail.html"
    context_object_name = "user_obj"


