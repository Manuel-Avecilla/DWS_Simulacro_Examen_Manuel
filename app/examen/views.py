# ============================================================
# region Importaciones
# ============================================================

from django.shortcuts import render, redirect
from examen.models import *
from examen.forms import *

from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.decorators import permission_required

from django.utils import timezone
from django.db.models import Q
from datetime import datetime

from django.contrib.auth.models import Group
from django.contrib import messages


from django.shortcuts import render
from django.views.defaults import page_not_found

# endregion
# ============================================================

#---HOME---
def home(request):
    return render(request, 'pages/home.html')


#region---USUARIO---

#region --- Detalles Usuario ---
#@permission_required('examen.view_usuario', raise_exception=True)
def dame_usuario(request, id_usuario):
    
    usuario = (
        Usuario.objects
        .get(id=id_usuario)
    )
    
    return render(request, 'models/usuario/detalles_usuario.html',{'Usuario_Mostrar':usuario})
# endregion

#region --- Lista Usuario ---
#@permission_required('examen.view_usuario', raise_exception=True)
def usuarios_listar(request):
    
    usuarios = (
        Usuario.objects
        .all()
    )
    
    return render(request, 'models/usuario/lista_usuario.html',{'Usuarios_Mostrar':usuarios})
# endregion

# endregion


#region---Organizador---

#region --- Detalles Organizador ---
#@permission_required('examen.view_organizador', raise_exception=True)
def dame_organizador(request, id_organizador):
    
    organizador = (
        Organizador.objects
        .select_related('usuario')
        .get(id=id_organizador)
    )
    
    return render(request, 'models/organizador/detalles_organizador.html',{'Organizador_Mostrar':organizador})
# endregion

#region --- Lista Organizador ---
#@permission_required('examen.view_organizador', raise_exception=True)
def organizadores_listar(request):
    
    organizadores = (
        Organizador.objects
        .select_related('usuario')
        .all()
    )
    
    return render(request, 'models/organizador/lista_organizador.html',{'Organizadores_Mostrar':organizadores})
# endregion

# endregion


#region---Evento---

#region --- Detalles Evento ---
@permission_required('examen.view_evento', raise_exception=True)
def dame_evento(request, id_evento):
    
    evento = (
        Evento.objects
        .select_related('categoria','sala','creador')
        .get(id=id_evento)
    )
    
    return render(request, 'models/evento/detalles_evento.html',{'Evento_Mostrar':evento})
# endregion

#region --- Lista Evento ---
@permission_required('examen.view_evento', raise_exception=True)
def eventos_listar(request):
    
    eventos = (
        Evento.objects
        .select_related('categoria','sala','creador')
        .all()
    )
    
    #---Segun-la-Sesion---
    
    mensaje=""
    
    if (request.user.rol == 2): # Organizador
        
        mensaje += "· Lista de (Todos los Eventos del Sistema)"
        
    else:
        fechaHoy = timezone.now()
        eventos = eventos.filter(fecha_final__gt = fechaHoy)
        mensaje += "· Lista de (Eventos Activos)"

    
    return render(request, 'models/evento/lista_evento.html',{'Eventos_Mostrar':eventos, 'Mensaje_Busqueda':mensaje})
# endregion

# endregion



# ============================================================
# region CRUD (Create, Read, Update, Delete)
# ============================================================

#region --- CREATE ---
@permission_required('examen.add_evento', raise_exception=True)
def evento_create(request): #Metodo que controla el tipo de formulario
        
    # Si la petición es GET se creará el formulario Vacío
    # Si la petición es POST se creará el formulario con Datos.
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    formulario = EventoForm(datosFormulario)
    
    if (request.method == "POST"):
        
        evento_creado = crear_evento_modelo(formulario, request.user)
        
        if(evento_creado):
            messages.success(request, 'Se ha creado el Evento: [ '+formulario.cleaned_data.get('titulo')+" ] correctamente.")
            return redirect('eventos_listar')

    return render(request, 'models/evento/crud/create_evento.html',{'formulario':formulario})

def crear_evento_modelo(formulario, usuario): #Metodo que interactua con la base de datos
    
    evento_creado = False
    # Comprueba si el formulario es válido
    if formulario.is_valid():
        try:
            # Almacena el Evento
            evento = formulario.save(commit=False)

            # asignar creador SIEMPRE
            evento.creador = usuario.Organizador

            # Guarda el Evento en la base de datos
            evento.save()
            
            evento_creado = True
            
        except Exception as error:
            print(error)
    return evento_creado
#endregion

#region --- READ ---
@permission_required('examen.view_evento', raise_exception=True)
def evento_buscar_avanzado(request): #Busqueda Avanzada
    
    if(len(request.GET) > 0):
        formulario = EventoBuscarAvanzada(request.GET, request=request)
        if formulario.is_valid():
            mensaje_busqueda = 'Filtros Aplicados:\n'
            QsEvento = Evento.objects
            
            #Obtenemos los filtros
            texto_contiene = formulario.cleaned_data.get('texto_contiene')
            fecha_desde = formulario.cleaned_data.get('fecha_desde')
            fecha_hasta = formulario.cleaned_data.get('fecha_hasta')
            salas = formulario.cleaned_data.get('salas')
            
            #---Biografia---
            if(texto_contiene!=''):
                texto_contiene = texto_contiene.strip()
                QsEvento = QsEvento.filter(Q(descripcion__icontains=texto_contiene)|Q(titulo__icontains=texto_contiene))
                mensaje_busqueda += '· Titulo o Descripcion contiene "'+texto_contiene+'"\n'
            else:
                mensaje_busqueda += '· Cualquier Titulo o Descripcion \n'
            
            #---Fecha-Nacimiento---
            if (not fecha_desde is None):
                QsEvento = QsEvento.filter(fecha_inicio__gte=fecha_desde)
                mensaje_busqueda += '· Fecha Evento desde '+datetime.strftime(fecha_desde,'%d-%m-%Y')+'\n'
            else:
                mensaje_busqueda += '· Fecha Evento desde: Cualquier fecha \n'
            
            if (not fecha_hasta is None):
                QsEvento = QsEvento.filter(fecha_final__lte=fecha_hasta)
                mensaje_busqueda += '· Fecha Evento hasta '+datetime.strftime(fecha_hasta,'%d-%m-%Y')+'\n'
            else:
                mensaje_busqueda += '· Fecha Evento hasta: Cualquier fecha \n'
            
            #---Usuarios---
            if salas:
                
                QsEvento = QsEvento.filter(sala__id__in=salas)
                
                # Recorre los nombres y los separa con ,
                nombres_salas = ", ".join([s.nombre for s in salas])
                mensaje_busqueda += f'· Salas: {nombres_salas}\n'
                
            else:
                mensaje_busqueda += '· Cualquier Sala \n'
            
            
                #---Segun-la-Sesion---
                
            if (request.user.rol == 2): # Organizador
                
                mensaje_busqueda += "· Lista de (Todos los Eventos del Sistema)"
                
            else:
                fechaHoy = timezone.now()
                QsEvento = QsEvento.filter(fecha_final__gt = fechaHoy)
                mensaje_busqueda += "· Lista de (Eventos Activos)"
            
            
            #Ejecutamos la querySet y enviamos los usuarios
            eventos = QsEvento.all()
            
            return render(request, 'models/evento/lista_evento.html',
                        {'Eventos_Mostrar':eventos,
                        'Mensaje_Busqueda':mensaje_busqueda}
                        )
    else:
        formulario = EventoBuscarAvanzada(None, request=request)
    return render(request, 'models/evento/crud/buscar_avanzada_evento.html',{'formulario':formulario})
#endregion

#region --- UPDATE ---
@permission_required('examen.change_evento', raise_exception=True)
def evento_editar(request, id_evento): # Editar Perfil
    
    evento = Evento.objects.get(id = id_evento)
    
    # Si la petición es GET se creará el formulario Vacío
    # Si la petición es POST se creará el formulario con Datos.
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    formulario = EventoForm(datosFormulario,instance=evento)
    
    if (request.method == "POST"):
        
        evento_creado = crear_evento_modelo(formulario, request.user)
        
        if(evento_creado):
            messages.success(request, 'Se ha actualizado el Evento: [ '+formulario.cleaned_data.get('titulo')+" ] correctamente.")
            return redirect('eventos_listar')
    
    return render(request, 'models/evento/crud/actualizar_evento.html', {'formulario':formulario,'evento':evento})
#endregion

#region --- DELETE ---
@permission_required('examen.delete_evento', raise_exception=True)
def evento_eliminar(request, id_evento): # Eliminar Perfil
    evento = Evento.objects.get(id = id_evento)
    titulo = evento.titulo
    try:
        evento.delete()
        messages.success(request, 'Se ha eliminado el Evento [ '+titulo+' ] correctamente.')
    except Exception as error:
        print(error)
    return redirect('eventos_listar')
#endregion

# endregion
# ============================================================


# ============================================================
# region Registro
# ============================================================


def registrar_usuario(request):
    
    if request.user.is_authenticated:
        messages.info(request, 'Debe Cerrar Sesion para poder volver a Registrarse')
        return redirect('home')
    
    if request.method == 'POST':
        formulario = RegistroUsuarioForm(request.POST)
        
        if formulario.is_valid():
            
            rol = int(formulario.cleaned_data.get('rol'))
            
            user = formulario.save(commit=False)
            user.save()
            
            if(rol == Usuario.ASISTENTE):
                
                # Agregar el usuario a los grupos
                grupo_usuario = Group.objects.get(name='Asistente')
                grupo_usuario.user_set.add(user)
                
            elif(rol == Usuario.ORGANIZADOR):
                
                # Agregar el usuario a los grupos
                grupo_usuario = Group.objects.get(name='Organizador')
                grupo_usuario.user_set.add(user)
                
                # Crear el Objeto tecnico con la fk del usuario, y añadir el campo adicional
                u_codigo_empleado = formulario.cleaned_data.get('codigo_empleado')
                organizador = Organizador.objects.create(usuario = user, codigo_empleado=u_codigo_empleado)
                organizador.save()
            
            
            # Hacer el Login Automatico
            login(request, user)
            
            # 2 Variables en la Sesion Ejemplo----------------------------------------------
            
            # Nombre Usuario
            request.session['usuario'] = user.username
            
            # Hora Login
            request.session['hora_login'] = timezone.now().strftime("%d/%m/%Y %H:%M")
            
            #-------------------------------------------------------------------------------
            
            return redirect('home')
    else:
        formulario = RegistroUsuarioForm()
        
    return render(request, 'registration/signup_usuario.html', {'formulario': formulario})


# endregion
# ============================================================


# ============================================================
# region Login
# ============================================================


class MiLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        response = super().form_valid(form)

        user = self.request.user
        
        # 2 Variables en la Sesion Ejemplo----------------------------------------------
        
        # Nombre Usuario
        self.request.session['usuario'] = user.username
        
        # Hora Login
        self.request.session['hora_login'] = timezone.now().strftime("%d/%m/%Y %H:%M")

        #-------------------------------------------------------------------------------

        return response


# endregion
# ============================================================


# ============================================================
# region Errores personalizados (400, 403, 404, 500)
# ============================================================

def mi_error_404(request,exception=None):
    return render(request,'error/404.html',None,None,404)

def mi_error_403(request,exception=None):
    return render(request,'error/403.html',None,None,403)

def mi_error_400(request,exception=None):
    return render(request,'error/400.html',None,None,400)

def mi_error_500(request,exception=None):
    return render(request,'error/500.html',None,None,500)

# endregion
# ============================================================