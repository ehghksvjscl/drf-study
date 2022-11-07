import strawberry
from typing import List, Optional
from . import types
from . import queries
from common.permissions import OnlyLoggedIn


@strawberry.mutation
class Mutation:
    create_room: types.RoomType = strawberry.field(resolver=queries.create_room)
