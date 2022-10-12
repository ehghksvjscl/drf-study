from django.urls import path
from categories import views

urlpatterns = [
    path("", views.CategoriesView.as_view()),
    path("<int:pk>", views.CategoryDetailView.as_view()),
]
