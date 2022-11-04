from django.urls import path
from experiences import views

urlpatterns = [
    path("perks", views.Perks.as_view()),
    path("perks/<int:pk>", views.PerkDetail.as_view()),
    path("", views.Experiences.as_view()),
    path("<int:pk>", views.ExperienceDetail.as_view()),
    path("<int:pk>/bookings", views.Bookings.as_view()),
    path("<int:pk>/bookings/<int:booking_pk>", views.BookingDetail.as_view()),
]
