
from __future__ import absolute_import, unicode_literals

# Esto asegurará que Celery se cargue cuando Django se inicie.
from yugioh_api.celery import app as celery_app


__all__ = ('celery_app',)