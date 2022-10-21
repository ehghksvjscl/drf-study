from django.urls import path
from medias import views

urlpatterns = [
    path("photos/<int:pk>", views.PhotosDetail.as_view()),
]
