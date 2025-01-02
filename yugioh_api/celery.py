from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Establecer el módulo de configuración predeterminado de Django para Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yugioh_api.settings.base')

app = Celery('yugioh_api')

# Usar una cadena aquí significa que el worker no tendrá que serializar
# el objeto de configuración para Child processes.
# - namespace='CELERY' significa que todas las claves de configuración relacionadas con Celery
#   deben tener un prefijo `CELERY_`.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Cargar tareas de todos los módulos de aplicaciones registradas de Django.
app.autodiscover_tasks()