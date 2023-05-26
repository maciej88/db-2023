from dataclasses import dataclass


# {'cast_id': 102, 'character': 'Ambient Room Tech / Troupe', 'credit_id': '52fe48019251416c750acb6f', 'gender': 1, 'id': 42286, 'name': 'Julene Renee', 'order': 82}

@dataclass
class CastEntry:
    movie_index: int  # dodane... rząd w csv-ie
    cast_id: int
    character: str
    credit_id: str
    gender: int
    id: int  # id of ... the actor?
    name: str
    order: int


@dataclass
class MovieActor:
    movie_id: int  # dodane... rząd w csv-ie
    actor_id: int  # id of the actor
    cast_id: int
    character: str
    credit_id: str
    gender: int
    order_: int

# {'credit_id': '573c8e2f9251413f5d000094', 'department': 'Crew', 'gender': 1, 'id': 1621932, 'job': 'Stunts', 'name': 'Min Windle'}

@dataclass
class CrewEntry:
    movie_index: int
    credit_id: str  # unique?
    department: str
    gender: int
    id: int  # id of ... the person?
    job: str
    name: str


@dataclass
class Movie:
    movie_id: int
    title: str


@dataclass
class Actor:
    actor_id: int
    name: str


# "[{""id"": 28, ""name"": ""Action""}, {""id"": 12, ""name"": ""Adventure""}, {""id"": 14, ""name"": ""Fantasy""}, {""id"": 878, ""name"": ""Science Fiction""}]"
@dataclass
class Genre:
    genre_id: int
    name: str


@dataclass(frozen=True)
class MovieGenre:
    movie_id: int
    genre_id: int


@dataclass
class PCountry:
    iso_3166_1: str
    name: str

@dataclass
class MoviePCountry:
    movie_id: int
    iso_3166_1: str

@dataclass(frozen=True)
class Crew:
    crew_id: int  # unique
    gender: int # do zmiany
    name: str


@dataclass
class MovieCrew:
    movie_id: int
    crew_id: int
    gender: int
    name: str
    credit_id: str  # id of ... the person?
    job: str
    department: str

@dataclass
class EntryOfCrew:
    movie_id: int
    id: int
    credit_id: str
    department: str
    gender: int
    job: str
    name: str

@dataclass(unsafe_hash=True)
class Keyword:
    keyword_id: int
    name: str

@dataclass(unsafe_hash=True)
class MovieKeyword:
    movie_id: int
    keyword_id: int


@dataclass
class Language:
    lang_id: int
    lang: str

@dataclass
class MovieLanguage:
    movie_id: int
    lang_id: int

@dataclass
class CompanyEntry:
    movie_index: int
    id: int #company
    name: str

@dataclass
class Company:
    id: int
    name: str

@dataclass
class Pcompany:
    company_id: int
    name: str

@dataclass
class MovieCompany:
    movie_id: int
    company_id: int