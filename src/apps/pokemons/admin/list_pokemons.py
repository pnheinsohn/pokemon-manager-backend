from typing import List, Optional
from ninja import FilterSchema, ModelSchema, Query
from ninja.pagination import paginate
from pydantic import Field

from apps.pokemons.admin.router import router
from apps.pokemons.models import Pokemon, PokemonLevel, BasePokemonType, BasePokemon


class PokemonLevelSchema(ModelSchema):
    class Meta:
        model = PokemonLevel
        fields = [
            "value",
            "experience",
            "experience_goal",
        ]


class BasePokemonTypeSchema(ModelSchema):
    class Meta:
        model = BasePokemonType
        fields = [
            "id",
            "name",
        ]


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


class PokemonSchema(ModelSchema):
    level: PokemonLevelSchema
    base_pokemon: BasePokemonSchema

    class Meta:
        model = Pokemon
        fields = [
            "id",
            "nickname",
            "level",
            "base_pokemon",
            "hp",
            "attack",
            "defense",
            "special_attack",
            "special_defense",
            "speed",
        ]


class PokemonFilterSchema(FilterSchema):
    id: Optional[int] = None
    nickname: Optional[str] = Field(None, q="nickname__icontains")
    level: Optional[int] = None
    base_pokemon_id: Optional[int] = None
    base_pokemon_name: Optional[str] = Field(None, q="base_pokemon__name__icontains")


@router.get("/base-pokemons/{base_pokemon_id}", response={200: List[PokemonSchema]})
@paginate
def list_pokemons(request, base_pokemon_id: int, filters: Query[PokemonFilterSchema]):
    pokemons = (
        Pokemon.objects.filter(base_pokemon_id=base_pokemon_id)
        .filter(filters.get_filter_expression())
        .select_related("level", "base_pokemon")
        .prefetch_related("base_pokemon__types")
    )

    return list(
        map(
            lambda pokemon: {
                "id": pokemon.id,
                "nickname": pokemon.nickname,
                "level": {
                    "value": pokemon.level.value,
                    "experience": pokemon.level.experience,
                    "experience_goal": pokemon.level.experience_goal,
                },
                "base_pokemon": {
                    "id": pokemon.base_pokemon.id,
                    "name": pokemon.base_pokemon.name,
                    "pokedex_number": pokemon.base_pokemon.pokedex_number,
                    "types": [
                        {"id": t.id, "name": t.name}
                        for t in pokemon.base_pokemon.types.all()
                    ],
                    "base_hp": pokemon.base_pokemon.base_hp,
                    "base_attack": pokemon.base_pokemon.base_attack,
                    "base_defense": pokemon.base_pokemon.base_defense,
                    "base_special_attack": pokemon.base_pokemon.base_special_attack,
                    "base_special_defense": pokemon.base_pokemon.base_special_defense,
                    "base_speed": pokemon.base_pokemon.base_speed,
                },
                "hp": pokemon.hp,
                "attack": pokemon.attack,
                "defense": pokemon.defense,
                "special_attack": pokemon.special_attack,
                "special_defense": pokemon.special_defense,
                "speed": pokemon.speed,
            },
            pokemons,
        )
    )
