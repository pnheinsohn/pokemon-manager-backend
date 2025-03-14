from typing import Optional
from ninja import Schema
from django.db import transaction

from apps.pokemons.admin.router import router
from apps.pokemons.models import Pokemon


class DeletePokemonResponseSchema(Schema):
    success: bool
    error: Optional[str] = None


@router.delete("/pokemons/{pokemon_id}", response={200: DeletePokemonResponseSchema})
@transaction.atomic
def delete_pokemon(request, pokemon_id: int):
    try:
        Pokemon.objects.get(id=pokemon_id).delete()
        return DeletePokemonResponseSchema(success=True)
    except Pokemon.DoesNotExist:
        return DeletePokemonResponseSchema(success=False, error="Pokemon not found")
