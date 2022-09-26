from django.urls import path

from contract.views import ContractView, ReviewView

urlpatterns = [
    path("contracts/", ContractView.as_view()),
    path("contracts/<int:pk>/", ContractView.as_view()),
    path("contracts/<int:contract_id>/reviews/<int:pk>/", ReviewView.as_view()),
]
