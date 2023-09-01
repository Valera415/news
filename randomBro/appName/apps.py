from django.apps import AppConfig


class AppnameConfig(AppConfig):     #конфигурация приложухи
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appName'
    verbose_name = 'Новасти' #где то в админке видно будет
