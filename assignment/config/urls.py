from django.urls import path

from contract.views import ContractView, ContractUpdateView

urlpatterns = [
    path("contracts/", ContractView.as_view()),
    path("contracts/<int:pk>/update/", ContractUpdateView.as_view()),
]
