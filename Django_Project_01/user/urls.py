from django.urls import path
from . import views

urlpatterns = [
    path('reg_ok', views.about_registration, name='reg_ok'),
    path('users', views.show_user_view, name='all_users'),
    # path("profile/<username>", views.profile_update_view, name="profile-view"),
    path("profile", views.profile_update_view, name="profile-view"),
    path('profile_ok', views.about_profile, name='profile_ok'),
]
