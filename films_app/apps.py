from django.apps import AppConfig


class FilmsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'films_app'
    verbose_name = "Приложение фильмов"
