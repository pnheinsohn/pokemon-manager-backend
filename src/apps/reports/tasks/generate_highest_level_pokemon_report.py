import time
from django.utils import timezone

from config.celery import celery_app
from apps.pokemons.models import Pokemon
from apps.reports.models import Report


@celery_app.task(queue='backend.public.default', exchange='backend.public')
def generate_highest_level_pokemon_report(report_id: int):
    time.sleep(2)

    try:
        report = Report.objects.get(id=report_id)

        # Get top 10 highest level Pokemon
        highest_level_pokemon = (
            Pokemon.objects.all()
            .order_by('-level__value')[:10]
        )

        # Format results
        results = []
        for idx, pokemon in enumerate(highest_level_pokemon, 1):
            results.append({
                'rank': idx,
                'pokemon_id': pokemon.id,
                'pokemon_nickname': pokemon.nickname,
                'base_pokemon_name': pokemon.base_pokemon.name,
                'base_pokemon_pokedex_number': pokemon.base_pokemon.pokedex_number,
                'level': pokemon.level.value,
                'experience': pokemon.level.experience,
                'experience_goal': pokemon.level.experience_goal,
            })

        report.data = results
        report.status = 'completed'
        report.completed_at = timezone.now()
        report.save()

    except Exception as e:
        if report:
            report.status = 'failed'
            report.failed_at = timezone.now()
            report.save()

        raise e
