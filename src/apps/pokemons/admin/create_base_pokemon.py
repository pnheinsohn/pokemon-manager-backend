from typing import List
from ninja import Schema

from apps.pokemons.admin.router import router
from apps.pokemons.models import BasePokemon, BasePokemonType


class CreateBasePokemonResponseSchema(Schema):
    success: bool
    error: str | None = None


class CreateBasePokemonPayloadSchema(Schema):
    name: str
    pokedex_number: int
    type_ids: List[int]
    base_hp: int
    base_attack: int
    base_defense: int
    base_special_attack: int
    base_special_defense: int
    base_speed: int


@router.post("/base-pokemons", response={200: CreateBasePokemonResponseSchema})
def create_base_pokemon(request, payload: CreateBasePokemonPayloadSchema):
    base_pokemon = BasePokemon.objects.create(
        name=payload.name,
        pokedex_number=payload.pokedex_number,
        base_hp=payload.base_hp,
        base_attack=payload.base_attack,
        base_defense=payload.base_defense,
        base_special_attack=payload.base_special_attack,
        base_special_defense=payload.base_special_defense,
        base_speed=payload.base_speed
    )

    types = BasePokemonType.objects.filter(id__in=payload.type_ids)
    base_pokemon.types.set(types)

    return CreateBasePokemonResponseSchema(success=True)
