from typing import Optional
from ninja import Schema
from django.db import transaction

from apps.pokemons.admin.router import router
from apps.pokemons.models import Pokemon, BasePokemon, PokemonLevel


class CreatePokemonResponseSchema(Schema):
    success: bool
    error: str | None = None


class CreatePokemonPayloadSchema(Schema):
    nickname: Optional[str] = None
    level: int = PokemonLevel.MIN_LEVEL


@router.post("/base-pokemons/{base_pokemon_id}", response={200: CreatePokemonResponseSchema})
@transaction.atomic
def create_pokemon(request, base_pokemon_id: int, payload: CreatePokemonPayloadSchema):
    base_pokemon = BasePokemon.objects.get(id=base_pokemon_id)
    level = PokemonLevel.objects.create(value=payload.level)

    Pokemon.objects.create(
        base_pokemon=base_pokemon,
        level=level,
        nickname=payload.nickname,
        hp=int(base_pokemon.base_hp * (1 + ((level.value - 1) * 0.1))),
        attack=int(base_pokemon.base_attack * (1 + ((level.value - 1) * 0.1))),
        defense=int(base_pokemon.base_defense * (1 + ((level.value - 1) * 0.1))),
        special_attack=int(base_pokemon.base_special_attack * (1 + ((level.value - 1) * 0.1))),
        special_defense=int(base_pokemon.base_special_defense * (1 + ((level.value - 1) * 0.1))),
        speed=int(base_pokemon.base_speed * (1 + ((level.value - 1) * 0.1))),
    )

    return CreatePokemonResponseSchema(success=True)
