from django.test import TestCase

from propietarios.services import PropietarioService


class TestPropietarioService(TestCase):
    def test_01_el_servicio_realiza_crud_completo_de_propietario(self):
        data = {
            "dni": "12345678",
            "nombre": "Juan",
            "apellido": "Perez",
            "telefono": "1122334455",
            "email": "juan@test.com",
        }
        created = PropietarioService.crear_propietario(data)
        fetched = PropietarioService.obtener_propietario(created.dni)
        self.assertEqual(fetched.nombre, "Juan")

        listado = PropietarioService.listar_propietarios()
        self.assertEqual(listado.count(), 1)

        actualizado = PropietarioService.actualizar_propietario(
            created.dni, {"nombre": "Juan Actualizado"}
        )
        self.assertEqual(actualizado.nombre, "Juan Actualizado")

        PropietarioService.eliminar_propietario(created.dni)
        self.assertEqual(PropietarioService.listar_propietarios().count(), 0)
