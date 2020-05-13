from django.shortcuts import render
from django.http import HttpResponse
from .models import Event, User
from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

def logout_request(request):
    logout(request)
    return redirect("index")


class SearchView(generic.ListView):
    model = Event
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        # lookup which events contain user as attendee
        if 'search' in self.kwargs:
            context = super().get_context_data(**kwargs)
            searched_events = Event.objects.filter(name__contains=self.kwargs['search'])
            context["searched"] = searched_events
            context["search"] = self.kwargs['search']
            return context

    def post(self, request):
        return HttpResponseRedirect("/search/" + request.POST.get('search_request', ''))



class IndexView(generic.ListView):
    # TODO add date also in search
    template_name = "index.html"
    context_object_name = "latest_event_list"

    def get_queryset(self):
        return Event.objects.order_by("-start_datetime")


class DetailView(generic.DetailView):
    login_url = "/login/"
    model = Event
    template_name = "detail.html"


class ProfileView(generic.DetailView):
    login_url = "/login/"
    model = User
    # if context name is "user", it messes with the login display becuase it also uses context name user
    context_object_name = "profile_user"
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        # lookup which events contain user as attendee
        context = super().get_context_data(**kwargs)
        profile_events = Event.objects.filter(attendees=context["profile_user"])
        context["profile_events"] = profile_events
        return context


class SignUp(generic.CreateView):
    # TODO: don't sign up if logged in
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"


class EditProfile(LoginRequiredMixin, generic.UpdateView):
    model = User
    fields = [
        "discord",
        "email",
        "info",
        "email_notifications",
        "discord_notifications",
    ]
    template_name = "edit_profile.html"

    def get_object(self, queryset=None):
        return self.request.user


def join(request, event_id):
    # TODO: check authentication and if joined or not
    event = Event.objects.get(pk=event_id)
    user = User.objects.get(username=request.user)
    event.attendees.add(user)
    return redirect("info", pk=event.id)


def leave(request, event_id):
    event = Event.objects.get(pk=event_id)
    user = User.objects.get(username=request.user)
    event.attendees.remove(user)
    return redirect("info", pk=event.id)
