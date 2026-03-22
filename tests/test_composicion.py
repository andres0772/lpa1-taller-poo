"""
Pruebas unitarias para las clases de composición.
"""

import pytest

from models.composicion.comedor import Comedor
from models.concretos.mesa import Mesa
from models.concretos.silla import Silla


class TestComedor:
    """
    Pruebas para la clase Comedor.
    Valida composición y agregación.
    """

    def setup_method(self):
        """Configuración que se ejecuta antes de cada test."""
        # Crear instancias para composición
        self.mesa = Mesa(
            nombre="Mesa Familiar",
            material="Madera",
            color="Roble",
            precio_base=500.0,
            largo=2.0,
            ancho=1.0,
            altura=0.75,
            resistencia_peso=100.0,
            material_superficie="Madera",
            numero_patas=4,
            forma="rectangular",
        )

        self.silla1 = Silla("Silla 1", "Madera", "Roble", 120.0, True)
        self.silla2 = Silla("Silla 2", "Madera", "Roble", 120.0, True)

        self.comedor = Comedor(
            nombre="Comedor Familiar", mesa=self.mesa, sillas=[self.silla1, self.silla2]
        )

    def test_creacion_comedor(self):
        """Prueba la creación correcta del comedor con composición."""
        assert self.comedor.nombre == "Comedor Familiar"
        assert self.comedor.mesa == self.mesa
        assert len(self.comedor.sillas) == 2
        assert self.silla1 in self.comedor.sillas
        assert self.silla2 in self.comedor.sillas

    def test_composicion_relaciones(self):
        """Prueba las relaciones de composición del comedor."""
        # El comedor "tiene-una" mesa
        assert hasattr(self.comedor, "mesa")
        assert self.comedor.mesa is not None
        assert isinstance(self.comedor.mesa, Mesa)

        # El comedor "tiene-unas" sillas (lista)
        assert hasattr(self.comedor, "sillas")
        assert isinstance(self.comedor.sillas, list)
        assert len(self.comedor.sillas) == 2

        # Las sillas son del tipo correcto
        for silla in self.comedor.sillas:
            assert isinstance(silla, Silla)

    def test_agregar_silla(self):
        """Prueba agregar sillas al comedor."""
        silla_nueva = Silla("Silla Nueva", "Madera", "Roble", 120.0, True)

        resultado = self.comedor.agregar_silla(silla_nueva)
        assert "exitosamente" in resultado.lower()
        assert len(self.comedor.sillas) == 3
        assert silla_nueva in self.comedor.sillas

    def test_agregar_objeto_invalido(self):
        """Prueba que no se pueden agregar objetos que no sean sillas."""
        # Intentar agregar un objeto que no es una silla - pasar una cadena
        try:
            resultado = self.comedor.agregar_silla("No soy una silla")  # type: ignore
            assert "Error" in resultado
            assert "Solo se pueden agregar objetos de tipo Silla" in resultado
        except TypeError:
            # Si hay un error de tipo, también es aceptable
            assert True

        # Verificar que no se haya agregado nada
        assert len(self.comedor.sillas) == 2

    def test_quitar_silla(self):
        """Prueba quitar sillas del comedor."""
        # Quitar la última silla (índice -1 por defecto)
        resultado = self.comedor.quitar_silla()
        assert "removida" in resultado.lower()
        assert len(self.comedor.sillas) == 1
        assert self.silla1 in self.comedor.sillas  # La primera silla queda

        # Quitar por índice específico
        resultado = self.comedor.quitar_silla(0)
        assert "removida" in resultado.lower()
        assert len(self.comedor.sillas) == 0

        # Intentar quitar de lista vacía
        resultado = self.comedor.quitar_silla()
        assert "no hay sillas" in resultado.lower()

    def test_quitar_silla_indice_invalido(self):
        """Prueba quitar silla con índice inválido."""
        resultado = self.comedor.quitar_silla(5)  # Índice fuera de rango
        assert "índice" in resultado.lower() or "inválido" in resultado.lower()
        assert len(self.comedor.sillas) == 2  # No se removió nada

    def test_calculo_precio_total(self):
        """Prueba el cálculo del precio total del comedor."""
        # Precio de la mesa
        precio_mesa = self.mesa.calcular_precio()

        # Precio de las sillas
        precio_sillas = sum(
            silla.calcular_precio() for silla in [self.silla1, self.silla2]
        )

        # Precio total sin descuento
        precio_esperado = precio_mesa + precio_sillas

        # Verificar el cálculo
        precio_total = self.comedor.calcular_precio_total()
        assert precio_total == precio_esperado
        assert precio_total == round(precio_mesa + precio_sillas, 2)

    def test_calculo_precio_total_con_descuento(self):
        """Prueba el cálculo del precio total con descuento por set completo."""
        # Agregar más sillas para alcanzar el descuento
        silla3 = Silla("Silla 3", "Madera", "Roble", 120.0, True)
        silla4 = Silla("Silla 4", "Madera", "Roble", 120.0, True)

        self.comedor.agregar_silla(silla3)
        self.comedor.agregar_silla(silla4)

        # Ahora tenemos 4 sillas, debería aplicar el descuento del 5%
        precio_con_descuento = self.comedor.calcular_precio_total()

        # Calcular precio sin descuento para verificar
        precio_sin_descuento = self.mesa.calcular_precio()
        precio_sin_descuento += sum(
            silla.calcular_precio() for silla in self.comedor.sillas
        )

        # El precio con descuento debería ser el 95% del precio sin descuento
        esperado = round(precio_sin_descuento * 0.95, 2)
        assert precio_con_descuento == esperado

        # Verificar que el descuento se aplicó correctamente
        assert precio_con_descuento < precio_sin_descuento
        assert abs(precio_con_descuento - (precio_sin_descuento * 0.95)) < 0.01

    def test_obtener_descripcion_completa(self):
        """Prueba la generación de descripción completa."""
        descripcion = self.comedor.obtener_descripcion_completa()

        # Verificar que la descripción contenga información esperada
        assert "COMEDOR FAMILIAR" in descripcion
        assert "MESA:" in descripcion
        assert "SILLAS (2 unidades):" in descripcion
        assert self.mesa.nombre in descripcion
        assert self.silla1.nombre in descripcion
        assert self.silla2.nombre in descripcion
        assert "$" in descripcion  # Debe incluir el precio
        assert "PRECIO TOTAL" in descripcion

    def test_obtener_descripcion_completa_con_descuento(self):
        """Prueba la generación de descripción completa con descuento."""
        # Agregar sillas para alcanzar el descuento
        silla3 = Silla("Silla 3", "Madera", "Roble", 120.0, True)
        silla4 = Silla("Silla 4", "Madera", "Roble", 120.0, True)
        self.comedor.agregar_silla(silla3)
        self.comedor.agregar_silla(silla4)

        descripcion = self.comedor.obtener_descripcion_completa()

        # Verificar que mencione el descuento
        assert "DESCUENTO" in descripcion or "descuento" in descripcion
        assert "(Incluye 5% de descuento por set completo)" in descripcion

    def test_obtener_resumen(self):
        """Prueba la generación de resumen estadístico."""
        resumen = self.comedor.obtener_resumen()

        # Verificar que el resumen contiene las claves esperadas
        assert isinstance(resumen, dict)
        assert "nombre" in resumen
        assert "total_muebles" in resumen
        assert "precio_mesa" in resumen
        assert "precio_sillas" in resumen
        assert "precio_total" in resumen
        assert "capacidad_personas" in resumen
        assert "materiales_utilizados" in resumen

        # Verificar algunos valores específicos
        assert resumen["nombre"] == "Comedor Familiar"
        assert resumen["total_muebles"] == 3  # 1 mesa + 2 sillas
        assert resumen["capacidad_personas"] == 2  # Número de sillas

    def test_metodo_len(self):
        """Prueba el método __len__ del comedor."""
        # El comedor inicialmente tiene 1 mesa + 2 sillas = 3 muebles
        assert len(self.comedor) == 3

        # Agregar una silla
        silla_nueva = Silla("Silla Nueva", "Madera", "Roble", 120.0, True)
        self.comedor.agregar_silla(silla_nueva)
        # Ahora debería ser 1 mesa + 3 sillas = 4 muebles
        assert len(self.comedor) == 4

        # Quitar una silla
        self.comedor.quitar_silla()
        # Ahora debería ser 1 mesa + 2 sillas = 3 muebles
        assert len(self.comedor) == 3

    def test_capacidad_maxima_sillas(self):
        """Prueba la capacidad máxima de sillas."""
        # Verificar la capacidad por defecto
        assert self.comedor._calcular_capacidad_maxima() == 6

        # Empezamos con 2 sillas
        assert len(self.comedor.sillas) == 2

        # Podemos agregar hasta 4 sillas más antes de alcanzar el límite de 6
        sillas_agregadas_exitosamente = 0
        sillas_rechazadas = 0

        # Intentamos agregar 6 sillas más (de la 3 a la 8)
        for i in range(3, 9):
            silla = Silla(f"Silla {i}", "Madera", "Roble", 120.0, True)

            # Verificamos si podemos agregarla ANTES de agregar
            if len(self.comedor.sillas) < 6:
                # Debería poder agregarse (aún no hemos alcanzado el límite)
                resultado = self.comedor.agregar_silla(silla)
                assert "exitosamente" in resultado.lower()
                sillas_agregadas_exitosamente += 1
            else:
                # No debería poder agregarse (capacidad máxima alcanzada)
                resultado = self.comedor.agregar_silla(silla)
                assert "Capacidad máxima" in resultado
                sillas_rechazadas += 1

        # Deberíamos haber agregado exactamente 4 sillas exitosamente
        # (2 iniciales + 4 agregadas = 6, que es el límite)
        # Y deberíamos haber rechazado 2 sillas (las intentos 5 y 6 de agregar)
        assert sillas_agregadas_exitosamente == 4
        assert sillas_rechazadas == 2
        assert len(self.comedor.sillas) == 6  # 2 iniciales + 4 agregadas

    def test_metodo_str(self):
        """Prueba el método __str__ del comedor."""
        str_repr = str(self.comedor)
        assert "Comedor Familiar" in str_repr
        assert "Mesa +" in str_repr
        assert "2 sillas" in str_repr

    def test_propiedades_solo_lectura(self):
        """Prueba que las propiedades sean de solo lectura (devuelven copias)."""
        # Obtener las sillas
        sillas = self.comedor.sillas

        # Verificar que es una copia
        assert isinstance(sillas, list)
        assert len(sillas) == 2

        # Modificar la lista devuelta no debe afectar al comedor
        sillas.append(Silla("Silla Falsa", "Plástico", "Blanco", 50.0, False))
        assert len(self.comedor.sillas) == 2  # No cambió

    def test_independencia_objetos(self):
        """Prueba que los objetos contenidos pueden existir independientemente."""
        # Guardar referencias
        mesa_original = self.comedor.mesa
        silla_original = self.comedor.sillas[0]

        # Crear un nuevo comedor con los mismos objetos
        comedor2 = Comedor("Otro Comedor", mesa_original, [silla_original])

        # Ambos comedores deberían referenciar los mismos objetos
        assert comedor2.mesa is mesa_original
        assert comedor2.sillas[0] is silla_original

        # Modificar un objeto en un comedor debería afectar al otro
        comedor2.mesa.nombre = "Mesa Modificada"
        assert self.comedor.mesa.nombre == "Mesa Modificada"
