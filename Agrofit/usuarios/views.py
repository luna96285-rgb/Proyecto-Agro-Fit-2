from django.shortcuts import render, redirect #importamos redirect para redirigir al usuario a otras paginas
from django.contrib import messages # Esto es 
from .forms import RegistroFormulario #importamos el formulario para registro
from .models import Perfil_Usuario  #importamos el modelo del perfil de usuario

# Create your views here.

#FUNCION DONDE ESTA LA LOGICA OSEA LO QUE NOS PERMITE REGISTRAR AL USUARIO

def registro_usuario(request):
    
    #Este condicional es Si el usuario ya envio el formulario osea ya presiono REGISTRARME
    if request.method == 'POST':
        formulario = RegistroFormulario(request.POST)
        
        #Otro condicional para verificar que los DATOS sean seguros y cumplan todos sus condiciones
        if formulario.is_valid():
            
            #Si es valido se guarda en la BD en la tabla de auth_user 
            usuario_guardado = formulario.save()
            
            
            #Extraemos los datos especificos de (cleaned_data) osea CLEAN donde estan los datos ya verificados y listos
            rol = formulario.cleaned_data.get('rol')
            ficha = formulario.cleaned_data.get('numero_ficha')
            dependecia = formulario.cleaned_data.get('dependencia')
            centro_formacion = formulario.cleaned_data.get('centro_formacion')    
            
            
            # Aqui introducimos todos los datos a la tabla que creamos en el MODELOS
              # Pero aqui ya entran todos los datos que ya estas verificados y son correctos los datos de (cleaned_data)
              
            Perfil_Usuario.objects.create(
                # [Nombre de cada campo de models.py] = [Variable con cada dato verificado]
                usuario = usuario_guardado,
                rol = rol,
                ficha = ficha,
                dependencia = dependecia,
                centro = centro_formacion
            )
            
            # SI SALIO CORRECTO MOSTRAMOS UN MENSAJE DE CONFIRMACION Y REDERIGIMOS AL INICIO DE SESION
            messages.success(request, 'Registro Exitoso')
            return redirect('')
        
    #Si el usario apenas abrio la pagina (metodo GET)
    else:
        formulario = RegistroFormulario() #Le entregamos al usuario el formulario
        
    
    #Renderizamos la plantilla HTML pasandole la variable formulario_entrada
    #El render: es el puente que conecta las logicas con el HTML y mostrarlos
    return render(request, 'usuarios/.html', {'formulario':formulario}) 
        
