from django.urls import path
from wishlists import views

urlpatterns = [
    path("", views.Wishlists.as_view()),
    path("<int:pk>", views.WishlistDetail.as_view()),
    path("<int:pk>/rooms/<int:room_pk>", views.WishlistRoomToggle.as_view())
]
