"""
Pruebas unitarias para la Tienda.
"""

import pytest
from services.tienda import TiendaMuebles
from models.concretos.silla import Silla
from models.concretos.mesa import Mesa
from models.concretos.cama import Cama
from models.concretos.sofa import Sofa
from models.concretos.sofacama import SofaCama
from models.composicion.comedor import Comedor


class TestTiendaMuebles:
    """
    Pruebas para la clase TiendaMuebles.
    Valida la gestión de inventario, búsquedas, filtros y operaciones de venta.
    """

    def setup_method(self):
        """Configuración que se ejecuta antes de cada test."""
        self.tienda = TiendaMuebles("Tienda Test")

        # Crear muebles de prueba
        self.silla = Silla("Silla Test", "Madera", "Negra", 100.0, True)
        self.mesa = Mesa(
            "Mesa Test",
            "Madera",
            "Blanca",
            200.0,
            1.0,
            1.0,
            0.75,
            50.0,
            "Madera",
            4,
            "rectangular",
        )
        self.cama = Cama(
            "Cama Test",
            "Madera",
            "Marron",
            300.0,
            2.0,
            1.5,
            0.5,
            150.0,
            "Tela",
            True,
            "individual",
            True,
            0.5,
            2,
        )
        self.sofa = Sofa(
            "Sofá Test", "Tela", "Gris", 400.0, True, "tela", 3, False, False, False
        )
        self.sofacama = SofaCama("Sofá-Cama Test", "Tela", "Azul", 500.0)

        # Crear un comedor para pruebas
        self.comedor = Comedor(
            nombre="Comedor Test",
            mesa=self.mesa,
            sillas=[self.silla, Silla("Silla 2", "Madera", "Negra", 100.0, True)],
        )

    def test_creacion_tienda(self):
        """Prueba la creación correcta de una tienda."""
        assert self.tienda.nombre == "Tienda Test"
        assert self.tienda.total_muebles == 0
        assert len(self.tienda._inventario) == 0
        assert len(self.tienda._comedores) == 0
        assert len(self.tienda._ventas_realizadas) == 0
        assert len(self.tienda._descuentos_activos) == 0

    def test_agregar_mueble(self):
        """Prueba agregar muebles al inventario."""
        resultado = self.tienda.agregar_mueble(self.silla)
        assert "agregado exitosamente" in resultado
        assert self.tienda.total_muebles == 1
        assert self.silla in self.tienda._inventario

    def test_agregar_mueble_invalido(self):
        """Prueba que no se pueden agregar objetos que no sean muebles."""
        resultado = self.tienda.agregar_mueble("No soy un mueble")
        assert "Error" in resultado
        assert "Solo se pueden agregar objetos de tipo Mueble" in resultado
        assert self.tienda.total_muebles == 0

    def test_agregar_mueble_precio_invalido(self):
        """Prueba que no se puedan agregar muebles con precio inválido."""
        # Crear un mueble con precio base negativo (esto lanzará una excepción en el constructor)
        # Pero para probar la validación en agregar_mueble, creamos un mueble válido y luego modificamos su precio
        silla_valida = Silla("Silla Válida", "Madera", "Negra", 100.0, True)
        # Forzamos un precio inválido mediante manipulación directa (para testing)
        silla_valida._precio_base = -50.0

        resultado = self.tienda.agregar_mueble(silla_valida)
        assert "Error" in resultado
        assert "precio válido mayor a 0" in resultado
        assert self.tienda.total_muebles == 0

    def test_agregar_comedor(self):
        """Prueba agregar comedores a la tienda."""
        resultado = self.tienda.agregar_comedor(self.comedor)
        assert "agregado exitosamente" in resultado
        assert len(self.tienda._comedores) == 1
        assert self.comedor in self.tienda._comedores

    def test_agregar_comedor_invalido(self):
        """Prueba que no se puedan agregar objetos que no sean comedores."""
        resultado = self.tienda.agregar_comedor("No soy un comedor")
        assert "Error" in resultado
        assert "Solo se pueden agregar objetos de tipo Comedor" in resultado
        assert len(self.tienda._comedores) == 0

    def test_buscar_muebles_por_nombre(self):
        """Prueba buscar muebles por nombre."""
        # Agregar algunos muebles
        self.tienda.agregar_mueble(self.silla)
        self.tienda.agregar_mueble(self.mesa)
        self.tienda.agregar_mueble(self.sofa)

        # Buscar por nombre exacto
        resultados = self.tienda.buscar_muebles_por_nombre("Silla Test")
        assert len(resultados) == 1
        assert resultados[0] == self.silla

        # Buscar por coincidencia parcial
        resultados = self.tienda.buscar_muebles_por_nombre("Silla")
        assert len(resultados) == 1  # Solo la silla coincide
        assert resultados[0] == self.silla

        # Buscar por coincidencia parcial (mayúsculas/minúsculas)
        resultados = self.tienda.buscar_muebles_por_nombre("silla")
        assert len(resultados) == 1
        assert resultados[0] == self.silla

        # Buscar algo que no existe
        resultados = self.tienda.buscar_muebles_por_nombre("Inexistente")
        assert len(resultados) == 0

        # Buscar con cadena vacía
        resultados = self.tienda.buscar_muebles_por_nombre("")
        assert len(resultados) == 0

    def test_filtrar_por_precio(self):
        """Prueba filtrar muebles por rango de precios."""
        # Agregar muebles con diferentes precios
        self.tienda.agregar_mueble(self.silla)  # 100.0 * 1.1 = 110.0 (con respaldo)
        self.tienda.agregar_mueble(self.mesa)  # 200.0 + (4 * 5.0) = 220.0
        self.tienda.agregar_mueble(
            self.cama
        )  # 300.0 (precio base, sin modificadores en Cama básica)
        self.tienda.agregar_mueble(self.sofa)  # 400.0 * 1.1 = 440.0 (con respaldo)
        self.tienda.agregar_mueble(self.sofacama)  # Precio más complejo

        # Filtrar por rango bajo
        resultados = self.tienda.filtrar_por_precio(precio_min=0, precio_max=150)
        assert len(resultados) == 1  # Solo la silla
        assert resultados[0] == self.silla

        # Filtrar por rango medio
        resultados = self.tienda.filtrar_por_precio(precio_min=150, precio_max=250)
        assert len(resultados) == 1  # Solo la mesa
        assert resultados[0] == self.mesa

        # Filtrar por rango alto - ajustado para incluir el sofá (535.0)
        resultados = self.tienda.filtrar_por_precio(precio_min=500, precio_max=600)
        assert len(resultados) >= 1  # El sofá debería estar en este rango
        precios = [m.calcular_precio() for m in resultados]
        assert all(500 <= p <= 600 for p in precios)
        # Verificar que el sofá esté en los resultados
        assert self.sofa in resultados

        # Filtrar con rango que no incluye nada (el sofá-cama está a 1523.0, así que usamos un rango acima de su precio)
        resultados = self.tienda.filtrar_por_precio(precio_min=2000, precio_max=3000)
        assert len(resultados) == 0

    def test_filtrar_por_material(self):
        """Prueba filtrar muebles por material."""
        # Agregar muebles de diferentes materiales
        self.tienda.agregar_mueble(self.silla)  # Madera
        self.tienda.agregar_mueble(self.mesa)  # Madera
        self.tienda.agregar_mueble(self.sofa)  # Tela

        # Filtrar por madera
        resultados = self.tienda.filtrar_por_material("Madera")
        assert len(resultados) == 2
        assert self.silla in resultados
        assert self.mesa in resultados

        # Filtrar por tela
        resultados = self.tienda.filtrar_por_material("Tela")
        assert len(resultados) == 1
        assert self.sofa in resultados

        # Filtrar por material inexistente
        resultados = self.tienda.filtrar_por_material("Plástico")
        assert len(resultados) == 0

        # Probar case insensitive
        resultados = self.tienda.filtrar_por_material("madera")
        assert len(resultados) == 2

    def test_obtener_muebles_por_tipo(self):
        """Prueba obtener muebles por tipo específico."""
        # Agregar diferentes tipos de muebles
        self.tienda.agregar_mueble(self.silla)
        self.tienda.agregar_mueble(self.mesa)
        self.tienda.agregar_mueble(self.sofa)

        # Obtener sillas
        sillas = self.tienda.obtener_muebles_por_tipo(Silla)
        assert len(sillas) == 1
        assert sillas[0] == self.silla

        # Obtener mesas
        mesas = self.tienda.obtener_muebles_por_tipo(Mesa)
        assert len(mesas) == 1
        assert mesas[0] == self.mesa

        # Obtener sofás
        sofás = self.tienda.obtener_muebles_por_tipo(Sofa)
        assert len(sofás) == 1
        assert sofás[0] == self.sofa

        # Obtener tipo que no existe
        # Usamos un tipo que no está en nuestra jerarquía de muebles
        resultado = self.tienda.obtener_muebles_por_tipo(str)
        assert len(resultado) == 0

    def test_calcular_valor_inventario(self):
        """Prueba calcular el valor total del inventario."""
        # Inicialmente el inventario está vacío
        assert self.tienda.calcular_valor_inventario() == 0.0

        # Agregar algunos muebles y calcular el valor
        self.tienda.agregar_mueble(self.silla)  # Precio: 110.0
        self.tienda.agregar_mueble(self.mesa)  # Precio: 220.0

        valor_esperado = self.silla.calcular_precio() + self.mesa.calcular_precio()
        valor_actual = self.tienda.calcular_valor_inventario()
        assert valor_actual == valor_esperado
        assert valor_actual == 330.0

        # Agregar un comedor y verificar que también se incluye
        self.tienda.agregar_comedor(self.comedor)
        # El valor debería aumentar con el precio total del comedor
        valor_antes = self.tienda.calcular_valor_inventario()
        self.tienda.agregar_mueble(self.cama)  # Agregar otro mueble
        valor_despues = self.tienda.calcular_valor_inventario()
        assert valor_despues > valor_antes

    def test_aplicar_descuento(self):
        """Prueba aplicar descuentos a categorías."""
        resultado = self.tienda.aplicar_descuento("sillas", 10)
        assert "Descuento del 10% aplicado" in resultado
        assert "sillas" in self.tienda._descuentos_activos
        assert self.tienda._descuentos_activos["sillas"] == 0.1  # 10% = 0.1

        # Probar otro descuento
        resultado = self.tienda.aplicar_descuento("mesas", 25)
        assert "Descuento del 25% aplicado" in resultado
        assert self.tienda._descuentos_activos["mesas"] == 0.25

        # Probar límites
        resultado = self.tienda.aplicar_descuento("camas", 0)
        assert "Descuento del 0% aplicado" in resultado
        assert self.tienda._descuentos_activos["camas"] == 0.0

        resultado = self.tienda.aplicar_descuento("everything", 100)
        assert "Descuento del 100% aplicado" in resultado
        assert self.tienda._descuentos_activos["everything"] == 1.0

        # Probar porcentaje inválido
        resultado = self.tienda.aplicar_descuento("sillas", -5)
        assert "Error" in resultado
        assert "porcentaje debe estar entre 0 y 100" in resultado

        resultado = self.tienda.aplicar_descuento("sillas", 150)
        assert "Error" in resultado
        assert "porcentaje debe estar entre 0 y 100" in resultado

    def test_realizar_venta(self):
        """Prueba realizar la venta de un mueble."""
        # Agregar un mueble al inventario
        self.tienda.agregar_mueble(self.silla)
        assert self.tienda.total_muebles == 1

        # Realizar la venta
        venta = self.tienda.realizar_venta(self.silla, "Juan Pérez")

        # Verificar que la venta se registró correctamente
        assert "error" not in venta
        assert venta["mueble"] == "Silla Test"
        assert venta["cliente"] == "Juan Pérez"
        assert venta["precio_original"] == self.silla.calcular_precio()
        assert venta["precio_final"] == venta["precio_original"]  # Sin descuento
        assert venta["descuento"] == 0
        assert "fecha" in venta

        # Verificar que el mueble fue eliminado del inventario
        assert self.tienda.total_muebles == 0
        assert self.silla not in self.tienda._inventario
        assert len(self.tienda._ventas_realizadas) == 1
        assert self.tienda._ventas_realizadas[0] == venta

    def test_realizar_venta_con_descuento(self):
        """Prueba realizar una venta con descuento aplicado."""
        # Agregar un mueble y aplicar un descuento a su categoría
        self.tienda.agregar_mueble(self.silla)
        self.tienda.aplicar_descuento("silla", 10)  # 10% de descuento

        # Realizar la venta
        venta = self.tienda.realizar_venta(self.silla, "María Gómez")

        # Verificar que se aplicó el descuento
        assert "error" not in venta
        precio_original = self.silla.calcular_precio()
        precio_esperado = precio_original * 0.9  # 10% de descuento
        assert venta["precio_original"] == precio_original
        assert venta["descuento"] == 10.0  # 10%
        assert venta["precio_final"] == round(precio_esperado, 2)

        # Verificar que el mueble fue eliminado del inventario
        assert self.tienda.total_muebles == 0

    def test_realizar_venta_mueble_no_disponible(self):
        """Prueba intentar vender un mueble que no está en inventario."""
        # No agregamos el mueble al inventario
        venta = self.tienda.realizar_venta(self.silla, "Cliente")

        # Verificar que devuelve un error
        assert "error" in venta
        assert "no está disponible en inventario" in venta["error"]

        # Verificar que no se registró ninguna venta
        assert len(self.tienda._ventas_realizadas) == 0

    def test_obtener_estadisticas(self):
        """Prueba obtener estadísticas de la tienda."""
        # Estadísticas iniciales
        stats = self.tienda.obtener_estadisticas()
        assert stats["total_muebles"] == 0
        assert stats["total_comedores"] == 0
        assert stats["valor_inventario"] == 0.0
        assert stats["ventas_realizadas"] == 0
        assert stats["tipos_muebles"] == {}
        assert stats["descuentos_activos"] == 0

        # Agregar algunos muebles
        self.tienda.agregar_mueble(self.silla)
        self.tienda.agregar_mueble(self.mesa)
        self.tienda.agregar_mueble(self.sofa)

        # Agregar un comedor
        self.tienda.agregar_comedor(self.comedor)

        # Aplicar algunos descuentos
        self.tienda.aplicar_descuento("sillas", 10)
        self.tienda.aplicar_descuento("mesas", 5)

        # Verificar estadísticas actualizadas
        stats = self.tienda.obtener_estadisticas()
        assert stats["total_muebles"] == 3
        assert stats["total_comedores"] == 1
        assert stats["valor_inventario"] > 0
        assert stats["ventas_realizadas"] == 0
        assert len(stats["tipos_muebles"]) == 3  # Silla, Mesa, Sofa
        assert stats["tipos_muebles"]["Silla"] == 1
        assert stats["tipos_muebles"]["Mesa"] == 1
        assert stats["tipos_muebles"]["Sofa"] == 1
        assert stats["descuentos_activos"] == 2

    def test_generar_reporte_inventario(self):
        """Prueba generar un reporte completo del inventario."""
        # Agregar algunos muebles
        self.tienda.agregar_mueble(self.silla)
        self.tienda.agregar_mueble(self.mesa)

        # Generar reporte
        reporte = self.tienda.generar_reporte_inventario()

        # Verificar que contiene información esperada
        assert "REPORTE DE INVENTARIO" in reporte
        assert self.tienda.nombre in reporte
        assert "Total de muebles: 2" in reporte
        assert "Total de comedores: 0" in reporte
        assert "Valor total del inventario:" in reporte
        assert "DISTRIBUCIÓN POR TIPOS:" in reporte
        assert "- Silla: 1 unidades" in reporte
        assert "- Mesa: 1 unidades" in reporte

        # Probar con descuentos
        self.tienda.aplicar_descuento("sillas", 10)
        reporte = self.tienda.generar_reporte_inventario()
        assert "DESCUENTOS ACTIVOS:" in reporte
        assert "- sillas: 10.0%" in reporte
