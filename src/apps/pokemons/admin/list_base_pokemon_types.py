from typing import List, Optional
from ninja import FilterSchema, Query, ModelSchema
from ninja.pagination import paginate
from pydantic import Field

from apps.pokemons.admin.router import router
from apps.pokemons.models import BasePokemonType


class BasePokemonTypeSchema(ModelSchema):
    class Meta:
        model = BasePokemonType
        fields = ["id", "name"]


class TypeFilterSchema(FilterSchema):
    id: Optional[int] = None
    name: Optional[str] = Field(None, q="name__icontains")


@router.get("/base-pokemon-types", response={200: List[BasePokemonTypeSchema]})
@paginate
def list_base_pokemon_types(request, filters: Query[TypeFilterSchema]):
    return BasePokemonType.objects.all().filter(filters.get_filter_expression())
