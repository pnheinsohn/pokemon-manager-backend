from ninja import NinjaAPI
from config.settings import DEBUG
from apps.pokemons.admin import router as pokemon_router
from apps.reports.admin import router as report_router

admin_api = NinjaAPI(
  title="API",
  urls_namespace="admin",
  openapi_url="/openapi.json" if DEBUG else None,
  docs_url="/docs" if DEBUG else None,
)

admin_api.add_router("/pokemons", pokemon_router)
admin_api.add_router("/reports", report_router)
