# ============================================================
# region Importaciones
# ============================================================

from django import forms
from django.forms import ModelForm
from examen.models import *
from django.contrib.auth.forms import UserCreationForm

# endregion
# ============================================================


# ============================================================
# region Formulario Registro
# ============================================================
class RegistroUsuarioForm(UserCreationForm):
    roles = (
        (Usuario.USUARIO, 'Usuario'),
        (Usuario.TECNICO, 'Tecnico'),
    )   

    puesto = forms.CharField(
        max_length=50,
        label="Puesto (Solo para Tecnicos)",
        required=False
    )

    rol = forms.ChoiceField(choices=roles)
    
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2','rol','puesto')
    
    def clean(self):
        
        #Validamos con el modelo actual
        super().clean()
        
        # Obtener datos
        rol = self.cleaned_data.get('rol')
        puesto = self.cleaned_data.get('puesto')

        #Comprobamos
        if(rol == '2' and not puesto):
            self.add_error("puesto", "Debes rellenar el Puesto.")
        
        if(rol == '3' and puesto):
            self.add_error("puesto", "Solo pueden rellenar los Tecnicos.")


        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data
    
# endregion
# ============================================================





# ============================================================
# region Formulario Modelo
# ============================================================

# Formulario para el CREATE y UPDATE

# endregion
# ============================================================


# ============================================================
# region Formulario Busqueda Avanzada
# ============================================================

# Formulario para el READ (Busqueda Avanzada)

# endregion
# ============================================================