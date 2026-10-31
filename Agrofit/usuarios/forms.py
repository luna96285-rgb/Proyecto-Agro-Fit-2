# Hacemos las importaciones necesarias para el archivo de forms

from django import forms #Trae el formulario que trae Django ya con todo (contras Encriptadas y repeticion de contra).

from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm #Trae una herramieta de Django Para crear nuevos usuarios
#  - crea automaticamente las casillas o campos de nombre de usuario, contra y confirmacion de contra y trae el cifrado y las verificacion de contra(osea mas de 7 carecteres y lo demas)

#---------------------------------------------------------------------------------------------------------
#TRAEMOS LAS OPCIONES PARA LOS MENUS QUE DEFINIMOS EN EL MODELS.PY
from .models import ROLES, DEPENDENCIAS, CENTROS_FORMACION

#DEFENIMOS AQUI SOLO LAS OPCIONES DE LOS MENUS DESPLEGABLES 

ROLES_FORM = [('',''),] + list(ROLES) #Aqui aumentamos las impotacion de las opciones de cada menu


DEPENDENCIAS_FORM = [
    ('','--Seleciona una opcion--'),
] + list(DEPENDENCIAS) #Aqui aumentamos las impotacion de las opciones de cada menu


CENTROS_FORM = [
    ('','--Seleciona una opcion--'),
] + list(CENTROS_FORMACION) #Aqui aumentamos las impotacion de las opciones de cada menu


#------------------------------------------------------------------------------------------------------
#--EN ESTA PARTE DEFINIMOS LOS CAMPOS PERSONALIZADOS QUE SE SOLICITARAN EN LA PANTALLLA DE REGISTRO
#  (Esta parte ya incluye los campos, usuario y contra) que tiene las herramienta que importamos: UserCreationForm

class RegistroFormulario(UserCreationForm):
    
    #ESTOS SON LOS CAMPOS QUE SE MUETRAS EN EL FORMULARIO
      #los campos que tiene required=True: son requeridos
      #los campos que tiene required=False: No son requeridos
      #los campos que tiene ChoiceField: son  casillas de tipo menu de opciones
      #los campos que tiene CharField: son casillas de tipo texto 
    
    rol = forms.ChoiceField(
        choices= ROLES_FORM,
        label= "Seleciona tu rol",
        widget= forms.RadioSelect,
        required=True,
        initial='rol_aprendiz'
    )
    
    first_name = forms.CharField(max_length=50, required=True, label="Nombre")
    
    last_name = forms.CharField(max_length=50, required=True, label="Apellido")
    
    email = forms.EmailField(required=True, label="Correo")
    
    numero_ficha = forms.CharField(max_length=12, required=False, label="Numero de ficha (Solo Aprendiz)" )
    
    dependencia = forms.ChoiceField(
        choices= DEPENDENCIAS_FORM,
        required=False,
        label="Dependencia (solo Funcionarios)"
    )
    
    centro_formacion = forms.ChoiceField(
        choices=CENTROS_FORM,
        required=False,
        label= "Centro Formacion (solo Funcionario)"
    )
    
    #-------------------------------------------------------------------------------------------
    
    #ESTA FUNCION ES PARA DECIRLE A DJANGO QUE GUARDE ESTOS CAMPOS EN LA BD DE USUARIOS (auth_user) DE DJANGO
    # PORQUE ESTOS CAMPOS NO ESTAN EN NUESTRO MODELO models.py
    
    class Meta(UserCreationForm.Meta):
        model = User # Aqui especifica que estos campos se van a guaradar a la tabla de (auth_user)
        
        #Aqui le dice que estos campos debe guardar PERO LOS CAMPOS SE DEBEN LLAMAR IGUAL A CADA CAMPO EN LA BASE DE DATOS DE auth_user
        fields = UserCreationForm.Meta.fields + ('first_name','last_name','email')
        
        
    #---------------------------------------------------------------------------------------------
    
    #ESTA FUNCION CLEAN ES PARA REALIZAR UNA VALIDACION A LOS CAMPOS PARA VERIFICAR GUARDAR LA INFORCION
    
    def clean(self):
        
        cleaned_data = super().clean() #Esto se encarga de revisar que todos los campos respeten sus reglas como el (max_length) y demas
        
        #Se usa .Get para que si el usuario no seleciono rol, devuelve None en lugar de romper el codigo
        rol = cleaned_data.get('rol') #'rol': extrae la opcion que seleciono en rol
        ficha = cleaned_data.get('numero_ficha') #Y aqui extrae el numero de ficha que escribio
        dependencia = cleaned_data.get('dependencia') 
        centro_formacion = cleaned_data.get('centro_formacion')
        

        #AQUI PONEMOS REGLAS PARA CADA ROL PARA PODER REGISTRARSE
        
        if rol == 'rol_aprendiz':  #--Regla para Aprendiz
            if not ficha:
                self.add_error('numero_ficha', 'El numero de ficha es obligatorio para aprendizes')
            
            #aqui no le ponemos valor a estos campos porque este rol no los nesecita
            cleaned_data['dependencia'] = ''
            cleaned_data['centro_formacion'] = ''
            
            
        elif rol == 'rol_funcionario':  #--Regla para Funcionario
            if not dependencia:
                self.add_error('dependencia', 'Debe selecionar una dependencia')
            
            if not centro_formacion:
                self.add_error('centro_formacion', 'Debe selecionar un centro de formacion')
                
            #aqui no le ponemos valor a este campo porq no los nesecitan
            cleaned_data['numero_ficha'] = ''
        
        
        return cleaned_data #Retornamos todos los datos ya verificados y listos