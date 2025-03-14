from typing import List, Optional
from ninja import FilterSchema, Query, ModelSchema
from ninja.pagination import paginate
from pydantic import Field

from apps.pokemons.admin.router import router
from apps.pokemons.models import BasePokemon, BasePokemonType


class BasePokemonTypeSchema(ModelSchema):
    class Meta:
        model = BasePokemonType
        fields = ["id", "name"]


class BasePokemonSchema(ModelSchema):
    types: List[BasePokemonTypeSchema]

    class Meta:
        model = BasePokemon
        fields = [
            "id",
            "name",
            "pokedex_number",
            "types",
            "base_hp",
            "base_attack",
            "base_defense",
            "base_special_attack",
            "base_special_defense",
            "base_speed",
        ]


class BasePokemonFilterSchema(FilterSchema):
    id: Optional[int] = None
    name: Optional[str] = Field(None, q="name__icontains")
    pokedex_number: Optional[int] = None
    type_id: Optional[int] = Field(None, q="types__id")
    type_name: Optional[str] = Field(None, q="types__name__icontains")
    base_hp: Optional[int] = None
    base_attack: Optional[int] = None
    base_defense: Optional[int] = None
    base_special_attack: Optional[int] = None
    base_special_defense: Optional[int] = None
    base_speed: Optional[int] = None


@router.get("/base-pokemons", response={200: List[BasePokemonSchema]})
@paginate
def list_base_pokemons(request, filters: Query[BasePokemonFilterSchema]):
    return BasePokemon.objects.all().filter(filters.get_filter_expression())
