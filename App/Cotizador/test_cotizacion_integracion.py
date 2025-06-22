import pytest
from .utils import *
from .models import *

@pytest.mark.django_db
def test_integracion_guardar_cotizacion_crea_en_db(cliente, vehiculo, categoria, servicio, tarifa):
    cot = Cotizacion(
        cantidad=2,
        vehiculo=vehiculo,
        categoria=categoria,
        servicios=[servicio],
        software=[],
        cliente=cliente
    )

    cot.tarifas = [tarifa]
    cabecera = cot.guardar_cotizacion()

    assert Cotizacion_cabecera.objects.filter(id=cabecera.id).exists()
    assert Cotizacion_linea.objects.filter(idCotizazion_cab=cabecera).count() > 0


@pytest.mark.django_db
def test_integracion_calcular_total_retornar_proveedor_valido(cliente, vehiculo, categoria, servicio, tarifa):
    cot = Cotizacion(
        cantidad=1,
        vehiculo=vehiculo,
        categoria=categoria,
        servicios=[servicio],
        software=[],
        cliente=cliente
    )
    cot.tarifas = [tarifa]
    totales = cot.calcular_total_por_proveedor()

    assert len(totales) == 1
    assert totales[0]['id'] == tarifa.idProveedor.id
    assert totales[0]['total'] == tarifa.precio_unitario
