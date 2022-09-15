from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.request import Request

from contract.models import Contract
from contract.serializers import (
    ContractSerializer,
    ContractCreateSerializer,
    ContractUpdateSerializer
)


class ContractView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Contract.objects.order_by("-id")
    serializer_class = ContractSerializer

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs):
        self.serializer_class = ContractCreateSerializer
        return self.create(request, *args, **kwargs)


class ContractUpdateView(UpdateModelMixin, GenericAPIView):
    queryset = Contract.objects.order_by("-id")
    serializer_class = ContractUpdateSerializer

    def patch(self, request: Request, *args, **kwargs):
        return self.update(request, partial=True, *args, **kwargs)
