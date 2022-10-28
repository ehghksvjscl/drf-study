from typing import List
import strawberry


@strawberry.type
class Movie:
    pk: int
    title: str
    year: int
    rating: int


mock_db = [Movie(pk=1, title="Inception", year=2010, rating=5)]


def movies() -> List[Movie]:
    return mock_db


def movie(movie_pk: int) -> Movie:
    return mock_db[movie_pk - 1]


@strawberry.type
class Query:
    movies: List[Movie] = strawberry.field(resolver=movies)
    movie: Movie = strawberry.field(resolver=movie)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_movie(self, title: str, year: int, rating: int) -> Movie:
        movie = Movie(pk=mock_db[-1].pk + 1, title=title, year=year, rating=rating)
        mock_db.append(movie)
        return movie


schema = strawberry.Schema(query=Query, mutation=Mutation)
