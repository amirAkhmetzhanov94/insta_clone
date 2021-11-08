from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic import View, CreateView, DetailView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from accounts.forms import UserRegistrationForm, ProfileRegistrationForm, UserChangeForm, ProfileChangeForm, SearchForm
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
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(settings.LOGOUT_REDIRECT_URL)


class FollowGateway(LoginRequiredMixin, View):
    user_obj = None

    def dispatch(self, request, *args, **kwargs):
        self.user_obj = get_object_or_404(Profile, user_id=kwargs.get('pk'))
        self.user_followings = get_object_or_404(Profile, user_id=self.request.user.pk)
        return super(FollowGateway, self).dispatch(request, *args, **kwargs)

    def set_follow(self):
        self.user_obj.followers.add(self.request.user)
        self.user_followings.following.add(self.user_obj.user)

    def remove_follow(self):
        self.user_obj.followers.remove(self.request.user)
        self.user_followings.following.remove(self.user_obj.user)

    def post(self, request, *args, **kwargs):
        if request.user in self.user_obj.followers.all():
            self.remove_follow()
        else:
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
        result = super().form_valid(user_form)
        profile_form.instance.user = self.object
        profile_form.save()
        login(self.request, self.object)
        return result

    def form_invalid(self, user_form, profile_form):
        context = self.get_context_data(user_form=user_form, profile_form=profile_form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        if "profile_form" not in kwargs:
            kwargs["profile_form"] = self.get_profile_form()
            kwargs["user_form"] = self.form_class()
        return kwargs

    def get_success_url(self):
        return reverse("index")


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "user_detail.html"
    context_object_name = "user_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts_list"] = self.object.posts.all().order_by("-created_on")
        return context


class UserChangeView(UserPassesTestMixin, UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = "edit_profile.html"
    context_object_name = "user_obj"

    def test_func(self):
        return self.request.user == self.get_object() or \
               self.request.user.is_superuser or self.request.user.groups.filter(name="admins")

    def get_profile_form(self):
        form_kwargs = {"instance": self.object.profile}
        if self.request.method == "POST":
            form_kwargs["data"] = self.request.POST
            form_kwargs["files"] = self.request.FILES
        return ProfileChangeForm(**form_kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_form = self.get_form()
        profile_form = self.get_profile_form()
        if user_form.is_valid() and profile_form.is_valid():
            return self.form_valid(user_form, profile_form)
        else:
            return self.form_invalid(user_form, profile_form)

    def form_valid(self, user_form, profile_form):
        result = super().form_valid(user_form)
        profile_form.save()
        return result

    def form_invalid(self, user_form, profile_form):
        context = self.get_context_data(
            user_form=user_form,
            profile_form=profile_form
        )
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        if "profile_form" not in kwargs:
            kwargs["profile_form"] = self.get_profile_form()
            kwargs["user_form"] = self.get_form()
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse("profile", kwargs={"pk": self.object.pk})


class SearchResultsView(LoginRequiredMixin, ListView):
    model = User
    context_object_name = "users"
    template_name = "search_result.html"

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["search_form"] = self.form
        if self.search_value:
            context["query"] = urlencode({"q": self.search_value})
            if len(context["users"]) == 0:
                context["message"] = "Nothing found"
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(username__icontains=self.search_value) | Q(first_name__icontains=self.search_value) | Q(email__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data["q"]