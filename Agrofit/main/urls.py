from django.urls import path

#importamos el archivo views pues del archivo de pages
from main import views

urlpatterns = [
    path('inicio/', views.inicio, name="Base"),
]