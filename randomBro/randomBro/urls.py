from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('appName.urls')), #конструкция переносит юрлпаттерн в другой файл в то место где приложуха
]
