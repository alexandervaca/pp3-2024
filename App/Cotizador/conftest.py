import pytest

from .models import *
from .utils import *

@pytest.fixture
def vehiculo(db):
    return Vehiculo.objects.create(descripcion="Camión2")

@pytest.fixture
def categoria(db):
    return Categoria.objects.create(descripcion="Transporte2")

@pytest.fixture
def servicio(db, categoria):
    return Servicio.objects.create(idCategoria=categoria, descripcion="Carga2")

@pytest.fixture
def cliente(django_user_model):
    return django_user_model.objects.create_user(username='cliente', password='123')

@pytest.fixture
def proveedor(db):
    from Proveedores.models import Proveedor
    return Proveedor.objects.create(empresa="EmpresaX", email="proveedor@test.com", logo="logo.png", web="https://test.com")

@pytest.fixture
def vehiculo_servicio(db, vehiculo, servicio):
    return VehiculoServicio.objects.create(Vehiculo=vehiculo, Servicio=servicio)

@pytest.fixture
def tarifa(db, proveedor, vehiculo_servicio):
    return Tarifa.objects.create(
        idVechiculoServicio=vehiculo_servicio,
        idProveedor=proveedor,
        precio_unitario=100.00
    )

@pytest.fixture
def cotizacion_con_tarifas(cliente, vehiculo, categoria, servicio, tarifa):
    cot = Cotizacion(
        cantidad=3,
        vehiculo=vehiculo,
        categoria=categoria,
        servicios=[servicio],
        software=[],
        cliente=cliente
    )
    cot.tarifas = [tarifa]
    return cot
