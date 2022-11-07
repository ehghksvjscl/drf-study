import strawberry

from rooms import schema as rooms_schema
from rooms import mutaitons as rooms_mutations


@strawberry.type
class Query(rooms_schema.Query):
    pass


@strawberry.type
class Mutation(rooms_mutations.Mutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
