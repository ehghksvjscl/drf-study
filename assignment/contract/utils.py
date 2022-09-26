from typing import List
from contract.models import Contract, Review


def create_contract_review(
    review_teams: List, contract: Contract, is_clear: bool = False
):
    """create contract reivew"""

    if is_clear:
        contract.review_set.clear()

    reviews = []
    for team in review_teams:
        reviews.append(Review(team=team, contract=contract))

    Review.objects.bulk_create(reviews)
