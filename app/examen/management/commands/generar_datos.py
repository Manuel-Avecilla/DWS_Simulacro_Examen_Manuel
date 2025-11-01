# region Explicación de los imports.
# ------------------------------------------------------------
# BaseCommand: permite crear comandos personalizados de Django.
# Faker: genera datos falsos (en español si se usa Faker('es_ES')).
# random: funciones aleatorias (choice, sample, randint...).
# Decimal: maneja decimales con precisión (para puntuaciones).
# timedelta: suma/resta días a fechas.
# timezone: obtiene fecha/hora actual con soporte de zona horaria.
# Modelos: importamos las clases necesarias del app examen.
# ------------------------------------------------------------
# endregion

# python manage.py generar_datos   <-- Comando para generar los datos (Con Faker)

# python manage.py seed examen --number=15   <-- Comando para generar los datos (Con Seeder)

# python manage.py dumpdata --indent 4 > examen/fixtures/datos.json   <-- Comando para guardar los datos

from django.core.management.base import BaseCommand
from faker import Faker
import random
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from examen.models import *

class Command(BaseCommand):
    help = 'Generando datos usando Faker'

    def handle(self, *args, **kwargs):
        fake = Faker('es_ES')  # Faker en español
        
        # region Creación de Usuarios
        # ------------------------------------------------------------
        # 1. Se crea una lista vacía `usuarios` para guardar las instancias creadas.
        # 2. Se generan 30 usuarios falsos con datos de Faker:
        #    - nombre_usuario: nombre de usuario único.
        #    - correo: email único.
        #    - fecha_registro: fecha actual menos un numero de dias entre 20 y 1000.
        # 3. Cada usuario creado se guarda en la lista `usuarios` para usarlos después.
        # ------------------------------------------------------------
        self.stdout.write("Generando usuarios...")
        usuarios = []
        for _ in range(30):
            usuarios.append(Usuario.objects.create(
                nombre_usuario=fake.unique.user_name(),
                correo=fake.unique.email(),
                password=fake.password(length=10),
                fecha_registro = timezone.now() - timedelta(days=random.randint(20, 1000))
            ))
        # endregion
        
        # region Creación de Cuentas Bancarias
        # ------------------------------------------------------------
        # 1. Se recorre la lista de usuarios creada anteriormente.
        # 2. Por cada usuario se genera una cuenta bancaria asociada (relación 1:1).
        # 3. Faker rellena los campos de la cuenta bancaria:
        # ------------------------------------------------------------
        self.stdout.write("Generando Cuentas Bancarias...")
        for usuario in usuarios:
            CuentaBancaria.objects.create(
                usuario=usuario,
                banco=random.choice(['CX', 'BB','UN','IN']),
                numero=random.randint(10000000, 99999999),
            )
        # endregion
        
        # region Creación de Moviles
        # ------------------------------------------------------------
        # 1. Se crea una lista vacía `moviles` para guardar las instancias creadas.
        # 2. Se generan 30 moviles falsos con datos de Faker:
        # 3. Cada movil creado se guarda en la lista `moviles` para usarlos después.
        # ------------------------------------------------------------
        self.stdout.write("Generando Moviles...")
        moviles = []
        for _ in range(30):
            moviles.append(Movil.objects.create(
                modelo=fake.unique.word().capitalize(),
                descripcion=fake.text(250),
                fecha_salida = timezone.now() - timedelta(days=random.randint(200, 1500))
            ))
        # endregion
        
        # region Votando Moviles por Usuarios
        self.stdout.write("Votando Moviles por Usuarios...")
        # 1. Recorremos todos los Usuarios
        for usuario in usuarios:
            # 2. Seleccionamos 2 Moviles al azar para cada Usuario
            moviles_votados = random.sample(moviles, k=2)
            
            # 3. Creamos la relación en el modelo intermedio Votar
            for movil in moviles_votados:
                Votar.objects.create(
                    usuario=usuario,
                    movil=movil,
                    puntuacion=random.randint(1, 5),
                    comentario=fake.text(100),
                    fecha_envio= timezone.now() - timedelta(days=random.randint(10, 300))
                )
        # endregion
        
        self.stdout.write(self.style.SUCCESS("Datos generados correctamente."))