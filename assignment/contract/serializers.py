from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from contract.models import Contract, Review
from users.models import User
from contract.utils import create_contract_review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["team"]


class ReviewUpdateSerializer(ReviewSerializer):
    def update(self, instance, validated_data):
        is_confirmed = validated_data.get("is_confirmed")
        if is_confirmed is not None:
            if self.context["request"].user != instance.manager:
                raise PermissionDenied()

        return super().update(instance, validated_data)

    class Meta:
        model = Review
        fields = [
            "id",
            "manager",
            "is_confirmed",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
        }


class ContractSerializer(serializers.ModelSerializer):
    manager = serializers.HiddenField(default=serializers.CurrentUserDefault())
    reviews = ReviewSerializer(source="review_set", many=True, read_only=True)

    class Meta:
        model = Contract
        fields = [
            "id",
            "title",
            "is_private",
            "manager",
            "reviews",
        ]

        extra_kwargs = {
            "id": {"read_only": True},
        }


class ContractCreateSerializer(ContractSerializer):
    review_teams = serializers.MultipleChoiceField(
        choices=User.TeamChoices.choices,
        write_only=True,
    )

    class Meta:
        model = Contract
        fields = ContractSerializer.Meta.fields + ["review_teams"]

    def create(self, validated_data):
        review_teams = validated_data.pop("review_teams")
        contract = Contract.objects.create(**validated_data)

        create_contract_review(review_teams, contract)

        return contract


class ContractUpdateSerializer(ContractSerializer):
    review_teams = serializers.MultipleChoiceField(
        choices=User.TeamChoices.choices, write_only=True, required=False
    )

    def update(self, instance, validated_data):
        if self.context["request"].user != instance.manager:
            raise PermissionDenied()

        review_teams = validated_data.get("review_teams")
        if review_teams is not None:
            create_contract_review(review_teams, instance, is_clear=True)

        return super().update(instance, validated_data)

    class Meta:
        model = Contract
        fields = [
            "id",
            "title",
            "review_teams",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
        }
