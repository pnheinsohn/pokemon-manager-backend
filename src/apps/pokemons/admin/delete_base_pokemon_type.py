from ninja import Schema
from django.db import transaction
from django.forms import ValidationError

from apps.pokemons.admin.router import router
from apps.pokemons.models import BasePokemonType


class DeleteBasePokemonTypeResponseSchema(Schema):
    success: bool
    error: str | None = None


@router.delete("/base-pokemon-types/{type_id}", response={200: DeleteBasePokemonTypeResponseSchema})
@transaction.atomic
def delete_base_pokemon_type(request, type_id: int):
    pokemon_type = BasePokemonType.objects.get(id=type_id)

    if pokemon_type.base_pokemons.exists():
        return DeleteBasePokemonTypeResponseSchema(
            success=False,
            error=f"Cannot delete type because it is being used by one or more Pokémon"
        )

    try:
        pokemon_type.delete()
        return DeleteBasePokemonTypeResponseSchema(success=True)
    except BasePokemonType.DoesNotExist:
        return DeleteBasePokemonTypeResponseSchema(success=False, error="Base pokemon type not found")
