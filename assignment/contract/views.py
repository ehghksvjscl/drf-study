from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.request import Request

from contract.models import Contract, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "type"
        ]


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = [
            "id",
            "title",
        ]


class ContractCreateSerializer(serializers.ModelSerializer):
    manager = serializers.HiddenField(default=serializers.CurrentUserDefault())
    reviews = ReviewSerializer(many=True, required=False)

    class Meta:
        model = Contract
        fields = [
            "id",
            "title",
            "manager",
            "is_reviewed",
            "reviews",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "is_reviewed": {"read_only": True},
        }


class ContractUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = [
            "id",
            "title",
            "is_legal_team_confirmed",
            "legal_team_manager",
            "is_finance_team_confirmed",
            "finance_team_manager",
            "is_security_team_confirmed",
            "security_team_manager",
            "is_reviewed",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "is_reviewed": {"read_only": True},
        }




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
