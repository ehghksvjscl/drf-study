from django.urls import path

from contract.views import ContractListView, ContractCreateView, ContractUpdateView

urlpatterns = [
    path("contracts/", ContractListView.as_view()),
    path("contracts/create/", ContractCreateView.as_view()),
    path("contracts/<int:pk>/update/", ContractUpdateView.as_view()),
]
