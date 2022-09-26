from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.request import Request

from django.shortcuts import get_object_or_404

from contract.models import Contract, Review
from contract.serializers import (
    ContractSerializer,
    ContractCreateSerializer,
    ContractUpdateSerializer,
    ReviewSerializer,
    ReviewUpdateSerializer,
)


class ContractView(ListModelMixin, CreateModelMixin, UpdateModelMixin, GenericAPIView):
    queryset = Contract.objects.order_by("-id")
    serializer_class = ContractSerializer

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs):
        self.serializer_class = ContractCreateSerializer
        return self.create(request, *args, **kwargs)

    def patch(self, request: Request, *args, **kwargs):
        self.serializer_class = ContractUpdateSerializer
        return self.update(request, partial=True, *args, **kwargs)


class ReviewView(UpdateModelMixin, GenericAPIView):
    queryset = Review.objects.order_by("-id")
    serializer_class = ReviewSerializer

    def patch(self, request: Request, contract_id: int, *args, **kwargs):
        self.serializer_class = ReviewUpdateSerializer
        return self.update(request, partial=True, *args, **kwargs)
