from django.urls import path
from users import views

urlpatterns = [
    path("", views.Users.as_view()),
    path("me", views.Me.as_view()),
]
