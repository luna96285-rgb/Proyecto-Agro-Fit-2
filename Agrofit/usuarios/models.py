from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#-------------------------------------------------------------------------------------
#Opciones para las opciones de los menus desplagables 

ROLES = [
    # Llave: se guarada en la base de datos y contenido: se muestar al usuario
    ('rol_aprendiz','Aprendiz'),
    ('rol_funcionario','Funcionario'),
]

DEPENDENCIAS = [
    ('depe_1','Instructor Gym'),
    ('depe_2','Instructor sena'),
    ('depe_3','Coordinador'),
]

CENTROS_FORMACION = [
    ('centro_1','Centro Agropecuario'),
    ('centro_2','Ctpi'),
]
#------------------------------------------------------------------------------------

class Perfil_Usuario(models.Model): #Esta clase representa la tabla en la base de datos
    
    #Todas estas variables representan un campo en la BD de la tabla de Perfil_Usuario (osea de la class)
    
    #Aqui me va guardar este campo como id_usuario 
    usuario = models.OneToOneField(User, on_delete=models.CASCADE) # models.OneToOneField: Significa que un usuario solo puede tener un Perfil, y un Perfil pertenece a un solo usuario
    
    
    rol = models.CharField(
        max_length=20, 
        choices=ROLES #Aqui reutilizamos los datos de la varibale de ROLES y esto los muestra tipo menu de opciones
        )
    
    
    #Estos otros campos que permiten estar nulos al momento del registro 
      # blank=True (permite enviarlo vacío desde el formulario)
      # null=True (permite guardar un valor nulo en la base de datos)
    
    numero_ficha = models.CharField(
        max_length=12,
        blank=True,
        null=True,
    )
    
    dependecia = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    
    centro_formacion = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    
    
    #Texo que idetifica al perfil en el panel de administracion : osea esto no muestra en el panel de django SOLO el username y su rol
    def __str__(self):
        return f"{self.usuario.username} - {self.rol}" 