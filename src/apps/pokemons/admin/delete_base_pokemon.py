from ninja import Schema
from django.db import transaction

from apps.pokemons.admin.router import router
from apps.pokemons.models import BasePokemon


class DeleteBasePokemonResponseSchema(Schema):
    success: bool
    error: str | None = None


@router.delete("/base-pokemons/{base_pokemon_id}", response={200: DeleteBasePokemonResponseSchema})
@transaction.atomic
def delete_base_pokemon(request, base_pokemon_id: int):
    base_pokemon = BasePokemon.objects.get(id=base_pokemon_id)

    if base_pokemon.instances.exists():
        return DeleteBasePokemonResponseSchema(
            success=False,
            error=f"Cannot delete because it has Pokemon instances"
        )

    try:
        base_pokemon.delete()
        return DeleteBasePokemonResponseSchema(success=True)
    except BasePokemon.DoesNotExist:
        return DeleteBasePokemonResponseSchema(success=False, error="Base pokemon not found")
