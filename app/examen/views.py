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

#region---TECNICO---

#region --- Detalles Tecnico ---
#@permission_required('examen.view_tecnico', raise_exception=True)
def dame_tecnico(request, id_tecnico):
    
    tecnico = (
        Tecnico.objects
        .select_related('usuario')
        .get(id=id_tecnico)
    )
    
    return render(request, 'models/tecnico/detalles_tecnico.html',{'Tecnico_Mostrar':tecnico})
# endregion

#region --- Lista Tecnico ---
#@permission_required('examen.view_tecnico', raise_exception=True)
def tecnicos_listar(request):
    
    tecnicos = (
        Tecnico.objects
        .select_related('usuario')
        .all()
    )
    
    return render(request, 'models/tecnico/lista_tecnico.html',{'Tecnicos_Mostrar':tecnicos})
# endregion

# endregion



# ============================================================
# region CRUD
# ============================================================

#---CREATE---


#---READ---


#---UPDATE---


#---DELETE---



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
            
            if(rol == Usuario.USUARIO):
                
                # Agregar el usuario a los grupos
                grupo_usuario = Group.objects.get(name='Usuario')
                grupo_usuario.user_set.add(user)
                
            elif(rol == Usuario.TECNICO):
                
                # Agregar el usuario a los grupos
                grupo_usuario = Group.objects.get(name='Tecnico')
                grupo_usuario.user_set.add(user)
                
                # Crear el Objeto tecnico con la fk del usuario, y añadir el campo adicional
                u_puesto = formulario.cleaned_data.get('puesto')
                tecnico = Tecnico.objects.create(usuario = user, puesto=u_puesto)
                tecnico.save()
            
            
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