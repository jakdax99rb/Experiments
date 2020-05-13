from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("editprofile", views.EditProfile.as_view(), name="editprofile"),
    path("event/<int:event_id>/join", views.join, name="join"),
    path("event/<int:event_id>/leave", views.leave, name="leave"),
    path("event/<int:pk>/", views.DetailView.as_view(), name="info"),
    path(
        "login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="logout.html"),
        name="logout",
    ),
    path("profile/<int:pk>/", views.ProfileView.as_view(), name="profile"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("search/<str:search>/", views.SearchView.as_view(), name="search_request"),
    path("signup/", views.SignUp.as_view(), name="signup"),
]
