# ============================================================
# region Importaciones
# ============================================================

from django import forms
from django.forms import ModelForm
from examen.models import *
from django.contrib.auth.forms import UserCreationForm

from django.utils import timezone

# endregion
# ============================================================


# ============================================================
# region Formulario Registro
# ============================================================
class RegistroUsuarioForm(UserCreationForm):
    roles = (
        (Usuario.ASISTENTE, 'Asistente'),
        (Usuario.ORGANIZADOR, 'Organizador'),
    )   

    codigo_empleado = forms.CharField(
        max_length=50,
        label="Codigo Empleado (Solo para Organizadores)",
        required=False
    )

    rol = forms.ChoiceField(choices=roles)
    
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2','rol','codigo_empleado')
    
    def clean(self):
        
        #Validamos con el modelo actual
        super().clean()
        
        # Obtener datos
        rol = self.cleaned_data.get('rol')
        codigo_empleado = self.cleaned_data.get('codigo_empleado')

        #Comprobamos
        if(rol == '2' and not codigo_empleado):
            self.add_error("codigo_empleado", "Debes rellenar el Codigo Empleado.")
        
        if(rol == '3' and codigo_empleado):
            self.add_error("codigo_empleado", "Solo pueden rellenar los Organizadores.")


        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data
    
# endregion
# ============================================================





# ============================================================
# region Formulario Modelo
# ============================================================

class EventoForm(ModelForm):
    class Meta:
        model = Evento
        fields = ["categoria","sala","titulo","descripcion","aforo","fecha_inicio","fecha_final"]
        labels = {
            "categoria":("Selecciona una Categoria"),
            "sala":("Seleciona una Sala"),
            "titulo":("Titulo del Evento"),
            "descripcion":("Descripción"),
            "aforo":("Aforo"),
            "fecha_inicio":("Fecha de inicio"),
            "fecha_final":("Fecha de finalización"),
        }
        help_texts = {
            "titulo":("50 caracteres como máximo"),
            "descripcion":("100 caracteres como máximo")
        }
        widgets = {
            "fecha_inicio": forms.DateTimeInput(attrs={"type": "datetime-local"},format='%Y-%m-%dT%H:%M'),
            "fecha_final": forms.DateTimeInput(attrs={"type": "datetime-local"},format='%Y-%m-%dT%H:%M'),
        }

    def clean(self):
        #Validamos con el modelo actual
        super().clean()
        
        #Obtenemos los campos 
        sala = self.cleaned_data.get('sala')
        descripcion = self.cleaned_data.get("descripcion")
        aforo = self.cleaned_data.get("aforo")
        fecha_inicio = self.cleaned_data.get("fecha_inicio")
        fecha_final = self.cleaned_data.get("fecha_final")

        #Comprobamos
        if descripcion and descripcion == "gratis" or descripcion == "cancelado":
            self.add_error("descripcion", "la descripcion esta entre las palabras prohibidas.")

        #Aforo
        #salaQS = Sala.objects.filter(id = sala.id)
        #print(salaQS)
        #if aforo and aforo < salaQS.capacidad_maxima:
        #    self.add_error("aforo", "El aforo del evento no puede ser mayor que la capacidad maxima de la Sala seleccionada.")

        #fecha
        if fecha_inicio and fecha_final:
            if fecha_final < fecha_inicio:
                self.add_error(
                    "fecha_final",
                    "La fecha de finalización debe ser posterior a la fecha de inicio."
                )
        
        fechaHoy = timezone.now()
        if fechaHoy > fecha_inicio :
            self.add_error('fecha_inicio','La fecha de inicio debe ser mayor a Hoy')

        
        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data

# endregion
# ============================================================




# ============================================================
# region Formulario Busqueda Avanzada
# ============================================================

class EventoBuscarAvanzada(forms.Form):
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(EventoBuscarAvanzada, self).__init__(*args, **kwargs)
        
        salasQS = Sala.objects
        u_label = "Seleccionar Salas"
        
        if (self.request.user.rol == 2): # Organizador
            salasQS = salasQS.filter(tiene_proyector=True).all()
            u_label += " (Solo Salas con Proyector)"
            
        else:
            salasQS = salasQS.all()
            u_label += " (Todas las Salas del Sistema)"
        
        
        self.fields["salas"] = forms.ModelMultipleChoiceField(
            label=u_label,
            help_text="(Opcional). Para selecionar los elementos manten pulsada la tecla Ctrl",
            queryset=salasQS,
            required=False,
            widget=forms.SelectMultiple(attrs={
                'class': 'form-select',
                'size': '7'
            })
        )
    
    texto_contiene = forms.CharField(
        label='Titulo o Descripcion contiene',
        help_text="(Opcional)",
        required=False
    )
    
    fecha_desde = forms.DateField(
        label='Fecha Evento desde',
        help_text="(Opcional)",
        required=False,
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"},format='%Y-%m-%dT%H:%M')
    )

    fecha_hasta = forms.DateField(
        label='Fecha Evento hasta',
        help_text="(Opcional)",
        required=False,
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"},format='%Y-%m-%dT%H:%M')
    )
    
    def clean(self):
        
        super().clean()
        
        #Obtenemos los campos
        texto_contiene = self.cleaned_data.get('texto_contiene')
        fecha_desde = self.cleaned_data.get('fecha_desde')
        fecha_hasta = self.cleaned_data.get('fecha_hasta')
        salas = self.cleaned_data.get('salas')
        
        #Comprobamos
        
        if (
            texto_contiene == "" and
            fecha_desde is None and
            fecha_hasta is None and
            len(salas) == 0
        ):
            self.add_error('texto_contiene','Debes rellenar al menos un campo.')
            self.add_error('fecha_desde','Debes rellenar al menos un campo.')
            self.add_error('fecha_hasta','Debes rellenar al menos un campo.')
            self.add_error('salas','Debes rellenar al menos un campo.')
        
        if(
            not fecha_desde is None and
            not fecha_hasta is None and
            fecha_hasta < fecha_desde
            ):
            self.add_error('fecha_desde','Rango de fecha no valido.')
            self.add_error('fecha_hasta','Rango de fecha no valido.')
        
        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data

# endregion
# ============================================================