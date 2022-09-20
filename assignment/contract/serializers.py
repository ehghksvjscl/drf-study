from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from contract.models import Contract, Review, TEAM_LIST


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "team"
        ]


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
    review_teams = serializers.MultipleChoiceField(choices=TEAM_LIST, write_only=True)

    class Meta:
        model = Contract
        fields = ContractSerializer.Meta.fields + ["review_teams"]

    def create(self, validated_data):
        review_teams = validated_data.pop("review_teams")
        contract = Contract.objects.create(**validated_data)

        reviews = []
        for team in review_teams:
            reviews.append(Review(team=team, contract=contract))

        Review.objects.bulk_create(reviews)

        return contract



class ContractUpdateSerializer(ContractSerializer):

    def update(self, instance, validated_data):
        if self.context['request'].user != instance.manager:
            raise PermissionDenied()
            
        return super().update(instance, validated_data)

    class Meta:
        model = Contract
        fields = [
            "id",
            "title",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
        }