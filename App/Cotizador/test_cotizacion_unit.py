import pytest
from .utils import *
from .models import *
from unittest.mock import patch


@pytest.mark.django_db
def test_obtener_tarifas_filtra_por_vehiculo_y_servicio(mocker, vehiculo, categoria, cliente, servicio):
    tarifa_mock = mocker.MagicMock()
    Tarifa.objects.filter = mocker.MagicMock(return_value=[tarifa_mock])

    cot = Cotizacion(cantidad=1, vehiculo=vehiculo, categoria=categoria,
                     servicios=[servicio], software=[], cliente=cliente)

    tarifas = cot.obtener_tarifas()

    assert tarifa_mock in tarifas
    Tarifa.objects.filter.assert_called_with(
        idVechiculoServicio__Vehiculo=vehiculo,
        idVechiculoServicio__Servicio=servicio.id
    )


@pytest.mark.django_db
def test_calcular_total_por_proveedor_suma_correctamente(cotizacion_con_tarifas):
    totales = cotizacion_con_tarifas.calcular_total_por_proveedor()

    #print("\n\n Totales calculados por proveedor:")
    #for t in totales:
    #    print(t)

    assert isinstance(totales, list)
    assert totales[0]['total'] > 0
    assert totales[0]['total'] == 300.0
    assert 'empresa' in totales[0]


@pytest.mark.django_db
def test_guardar_cotizacion_crea_cab_y_lineas(cotizacion_con_tarifas):
    with patch('Cotizador.utils.Cotizacion_cabecera.objects.create') as mock_create_cab, \
         patch('Cotizador.utils.Cotizacion_linea.objects.create') as mock_create_linea:

        cotizacion_con_tarifas.guardar_cotizacion()

        assert mock_create_cab.called
        assert mock_create_linea.called
