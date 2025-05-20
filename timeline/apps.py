from django.apps import AppConfig
from django.db import connection


class TimelineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'timeline'

    def ready(self):
        with connection.cursor() as cursor:
            cursor.execute('PRAGMA journal_mode=WAL;')