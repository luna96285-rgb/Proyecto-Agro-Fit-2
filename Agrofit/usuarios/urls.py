from django.urls import path
from usuarios import views


urlpatterns = [
    
    path('registro/', views.registro_usuario, name="Registro"),

]

