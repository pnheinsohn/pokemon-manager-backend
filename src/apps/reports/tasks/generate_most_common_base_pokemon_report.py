import time
from django.utils import timezone
from django.db.models import Count

from config.celery import celery_app
from apps.pokemons.models import Pokemon
from apps.reports.models import Report


@celery_app.task(queue='backend.public.default', exchange='backend.public')
def generate_most_common_base_pokemon_report(report_id: int):
    time.sleep(2)

    try:
        report = Report.objects.get(id=report_id)

        # Get counts of Pokemon grouped by their base_pokemon
        base_pokemon_counts = (
            Pokemon.objects.filter(base_pokemon__isnull=False)
                .values('base_pokemon__name', 'base_pokemon')
                .annotate(count=Count('id'))
                .order_by('-count')[:10]
        )

        # Format results
        results = []
        for idx, entry in enumerate(base_pokemon_counts, 1):
            results.append({
                'rank': idx,
                'base_pokemon_name': entry['base_pokemon__name'],
                'base_pokemon_id': entry['base_pokemon'],
                'count': entry['count']
            })

        report.data = results
        report.status = Report.Status.COMPLETED
        report.completed_at = timezone.now()
        report.save()

    except Exception as e:
        if report:
            report.status = Report.Status.FAILED
            report.failed_at = timezone.now()
            report.save()
        raise e
