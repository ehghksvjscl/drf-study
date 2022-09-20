from django.urls import path

from contract.views import ContractView, ContractUpdateView

urlpatterns = [
    path("contracts/", ContractView.as_view()),
    path("contracts/<int:pk>/", ContractUpdateView.as_view()),
    path("contracts/<int:pk>/reviews/<int:review_id>/", ContractUpdateView.as_view()),
]
