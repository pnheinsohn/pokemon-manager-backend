from ninja import Schema

from apps.pokemons.admin.router import router
from apps.pokemons.models import BasePokemonType


class CreateBasePokemonTypeResponseSchema(Schema):
    success: bool
    error: str | None = None


class CreateBasePokemonTypePayloadSchema(Schema):
    name: str


@router.post("/base-pokemon-types", response={200: CreateBasePokemonTypeResponseSchema})
def create_base_pokemon_type(request, payload: CreateBasePokemonTypePayloadSchema):
    try:
        BasePokemonType.objects.create(name=payload.name)
        return CreateBasePokemonTypeResponseSchema(success=True)
    except Exception as e:
        return CreateBasePokemonTypeResponseSchema(success=False, error=str(e))
