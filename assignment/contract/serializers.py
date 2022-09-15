from rest_framework import serializers

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
            "review_types",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "is_reviewed": {"read_only": True},
            "review_types": {"read_only": True},
        }

        def create(self, validated_data):
            print(validated_data)


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



