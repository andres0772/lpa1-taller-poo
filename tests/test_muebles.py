"""
Pruebas unitarias para las clases de muebles.
Estas pruebas validan el correcto funcionamiento de todos los conceptos OOP implementados.
"""

import pytest

from models.composicion.comedor import Comedor
from models.concretos.cama import Cama
from models.concretos.mesa import Mesa
from models.concretos.silla import Silla
from models.concretos.sofa import Sofa
from models.concretos.sofacama import SofaCama

# Importar las clases a testear
from models.mueble import Mueble


class TestMuebleBase:
    """
    Pruebas para la clase base abstracta Mueble.
    Valida conceptos de abstracción y encapsulación.
    """

    def test_no_puede_instanciar_mueble_directamente(self):
        """
        Prueba que no se puede instanciar la clase abstracta Mueble directamente.
        Valida el concepto de abstracción.
        """
        with pytest.raises(TypeError):
            mueble = Mueble("Test", "Madera", "Café", 100.0)


class TestSilla:
    """
    Pruebas para la clase Silla.
    Valida herencia, polimorfismo y encapsulación.
    """

    def setup_method(self):
        """Configuración que se ejecuta antes de cada test."""
        self.silla_basica = Silla(
            nombre="Silla Básica",
            material="Madera",
            color="Café",
            precio_base=150.0,
            tiene_respaldo=True,
        )

        self.silla_oficina = Silla(
            nombre="Silla Oficina",
            material="Metal",
            color="Negro",
            precio_base=300.0,
            tiene_respaldo=True,
            material_tapizado="cuero",
            altura_regulable=True,
            tiene_ruedas=True,
        )

    def test_creacion_silla_basica(self):
        """Prueba la creación correcta de una silla básica."""
        assert self.silla_basica.nombre == "Silla Básica"
        assert self.silla_basica.material == "Madera"
        assert self.silla_basica.color == "Café"
        assert self.silla_basica.precio_base == 150.0
        assert self.silla_basica.tiene_respaldo == True

    def test_calculo_precio_silla_basica(self):
        """Prueba el cálculo de precio para silla básica."""

        # Implementar test de cálculo de precio
        precio = self.silla_basica.calcular_precio()

        # El precio debe incluir el precio base + factor de comodidad por respaldo
        # Precio base: 150.0
        # Factor comodidad con respaldo: 1.1 (150.0 * 1.1 = 165.0)
        assert precio == 165.0

    def test_calculo_precio_silla_oficina(self):
        """Prueba el cálculo de precio para silla de oficina con todas las características."""
        precio = self.silla_oficina.calcular_precio()

        # Precio base: 300.0
        # Tiene respaldo: factor += 0.1 → 1.1
        # Tapizado de cuero: factor += 0.2 → 1.3
        # Capacidad 1 persona: factor += (1-1)*0.05 = 0 → sigue siendo 1.3
        # Precio con factor de comodidad: 300.0 * 1.3 = 390.0
        # Altura regulable: +10.0 → 400.0
        # Tiene ruedas: +5.0 → 405.0
        assert precio == 405.0

    def test_es_silla_oficina(self):
        """Prueba la lógica de identificación de silla de oficina."""
        # La silla básica no tiene ruedas ni altura regulable
        assert self.silla_basica.es_silla_oficina() == False

        # La silla de oficina tiene tanto ruedas como altura regulable
        assert self.silla_oficina.es_silla_oficina() == True

    def test_regular_altura_silla_sin_mecanismo(self):
        """Prueba que las sillas sin altura regulable no pueden ajustarse."""
        resultado = self.silla_basica.regular_altura(100)
        assert resultado == "La silla no es regulable"

    def test_regular_altura_silla_con_mecanismo(self):
        """Prueba la regulación de altura en sillas que lo permiten."""
        resultado = self.silla_oficina.regular_altura(110)
        assert resultado == "Altura regulada a 110 cm"

    def test_validaciones_setter(self):
        """Prueba las validaciones en los setters."""

        with pytest.raises(ValueError):
            self.silla_basica.nombre = ""

        with pytest.raises(ValueError):
            self.silla_basica.precio_base = -100

        with pytest.raises(ValueError):
            self.silla_basica.capacidad_personas = 0

    def test_obtener_descripcion(self):
        """Prueba que la descripción contenga información relevante."""

        descripcion = self.silla_basica.obtener_descripcion()
        # Verificar que la descripción contenga el nombre y otras características
        assert "Silla Básica" in descripcion
        assert "Madera" in descripcion
        assert "Café" in descripcion
        assert "capacidad 1 personas" in descripcion
        assert "respaldo Sí" in descripcion
        assert "tapizado Ninguno" in descripcion
        assert "altura regulable: No" in descripcion
        assert "ruedas: No" in descripcion

    def test_polimorfismo_herencia(self):
        """Prueba que la silla implementa correctamente los métodos abstractos."""

        # Debe poder llamarse como Mueble (polimorfismo)
        from models.categorias.asientos import Asiento

        assert isinstance(self.silla_basica, Asiento)
        assert hasattr(self.silla_basica, "calcular_precio")
        assert hasattr(self.silla_basica, "obtener_descripcion")

        # Los métodos deben retornar valores válidos
        precio = self.silla_basica.calcular_precio()
        assert isinstance(precio, (int, float))
        assert precio > 0

        descripcion = self.silla_basica.obtener_descripcion()
        assert isinstance(descripcion, str)
        assert len(descripcion) > 0


class TestSofaCama:
    """
    Pruebas para la clase SofaCama.
    Valida herencia múltiple y resolución MRO.
    """

    def setup_method(self):
        """Configuración que se ejecuta antes de cada test."""
        # Crear instancia de prueba
        self.sofacama = SofaCama(
            nombre="SofaCama Deluxe",
            material="Tela",
            color="Gris",
            precio_base=800.0,
            tiene_respaldo=True,
            material_tapizado="tela",
            numero_cojines=3,
            tiene_chaiselongue=False,
            altura_regulable=False,
            tiene_ruedas=False,
            largo=2.0,
            ancho=1.5,
            altura=0.5,
            resistencia_peso=200.0,
            material_superficie="tela",
            es_extensible=True,
            tipo="matrimonial",
            tiene_cabecero=True,
            altura_max=1.0,
            numero_pillows=2,
        )

    def test_creacion_sofacama(self):
        """Prueba la creación correcta del sofá-cama."""

        # Implementar test de creación con herencia múltiple
        assert self.sofacama.nombre == "SofaCama Deluxe"
        assert self.sofacama.capacidad_personas == 3  # Valor por defecto de Asiento
        assert self.sofacama.tipo == "matrimonial"
        assert self.sofacama.tiene_cabecero == True
        # Verificar que es instancia de ambas clases padre
        from models.concretos.cama import Cama
        from models.concretos.sofa import Sofa

        assert isinstance(self.sofacama, Sofa)
        assert isinstance(self.sofacama, Cama)

    def test_conversion_modos(self):
        """Prueba la conversión entre modos sofá y cama."""

        # Inicialmente debe estar en modo sofá
        assert self.sofacama.modo_actual == "sofa"

        # Convertir a cama
        resultado = self.sofacama.convertir_a_cama()
        assert "convertido a cama" in resultado.lower()
        assert self.sofacama.modo_actual == "cama"

        # Intentar convertir a cama nuevamente
        resultado2 = self.sofacama.convertir_a_cama()
        assert "ya está en modo cama" in resultado2.lower()

        # Convertir de vuelta a sofá
        resultado3 = self.sofacama.convertir_a_sofa()
        assert "convertida a sofá" in resultado3.lower()
        assert self.sofacama.modo_actual == "sofa"

    def test_calculo_precio_dual(self):
        """Prueba el cálculo de precio considerando funcionalidad dual."""
        precio = self.sofacama.calcular_precio()

        assert precio == 2147.0

    def test_capacidad_total(self):
        """Prueba las capacidades en ambos modos."""

        capacidades = self.sofacama.obtener_capacidad_total()
        # Verificar que retorna un diccionario con las capacidades esperadas
        assert isinstance(capacidades, dict)
        assert "sofa" in capacidades
        assert "cama" in capacidades
        assert "total" in capacidades
        assert capacidades["sofa"] == 3  # Capacidad del sofá (heredada de Asiento)
        assert capacidades["cama"] == 2  # Capacidad estándar de cama
        assert capacidades["total"] == 5  # Suma de ambas capacidades

    def test_herencia_multiple_mro(self):
        """Prueba que la herencia múltiple funciona correctamente."""

        # Implementar test de MRO (Method Resolution Order)
        from models.concretos.cama import Cama
        from models.concretos.sofa import Sofa

        assert isinstance(self.sofacama, Sofa)
        assert isinstance(self.sofacama, Cama)

        # Verificar que tiene métodos de ambas clases padre
        assert hasattr(self.sofacama, "convertir_a_cama")
        assert hasattr(self.sofacama, "convertir_a_sofa")
        assert hasattr(self.sofacama, "calcular_precio")
        assert hasattr(self.sofacama, "obtener_descripcion")


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

        self.silla1 = Silla("Silla 1", "Madera", "Roble", 120.0, True)
        self.silla2 = Silla("Silla 2", "Madera", "Roble", 120.0, True)

        self.comedor = Comedor(
            nombre="Comedor Familiar", mesa=self.mesa, sillas=[self.silla1, self.silla2]
        )

    def test_creacion_comedor(self):
        """Prueba la creación correcta del comedor con composición."""

        # Implementar test de composición
        assert self.comedor.nombre == "Comedor Familiar"
        assert self.comedor.mesa == self.mesa
        assert len(self.comedor.sillas) == 2
        assert self.silla1 in self.comedor.sillas
        assert self.silla2 in self.comedor.sillas

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
        # Nota: Este test fallará en tiempo de compilación debido a typing,
        # pero lo mantenemos para validar el comportamiento en tiempo de ejecución
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

    def test_descuento_set_completo(self):
        """Prueba el descuento por set completo (4+ sillas)."""
        # Agregar más sillas para alcanzar el descuento (necesitamos 4+ sillas)
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

    def test_descripcion_completa(self):
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

    def test_resumen_estadistico(self):
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

    def test_len_comedor(self):
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


class TestConceptosOOPGenerales:
    """
    Pruebas que validan conceptos generales de OOP aplicados en todo el sistema.
    """

    def test_polimorfismo_general(self):
        """Prueba que diferentes tipos de muebles implementan polimorfismo correctamente."""
        from models.concretos.cama import Cama
        from models.concretos.mesa import Mesa
        from models.concretos.silla import Silla
        from models.concretos.sofa import Sofa
        from models.concretos.sofacama import SofaCama

        # Crear instancias de diferentes tipos de muebles
        silla = Silla("Silla Test", "Madera", "Negra", 100.0, True)
        mesa = Mesa(
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
        cama = Cama(
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
        sofá = Sofa(
            "Sofá Test", "Tela", "Gris", 400.0, True, "tela", 3, False, False, False
        )
        sofacama = SofaCama("Sofá-Cama Test", "Tela", "Azul", 500.0)

        # Lista de todos los muebles
        muebles = [silla, mesa, cama, sofá, sofacama]

        # Todos deben ser instancias de Mueble (polimorfismo)
        from models.mueble import Mueble

        for mueble in muebles:
            assert isinstance(mueble, Mueble)
            # Todos deben implementar los métodos abstractos
            assert hasattr(mueble, "calcular_precio")
            assert hasattr(mueble, "obtener_descripcion")
            # Los métodos deben retornar valores válidos
            precio = mueble.calcular_precio()
            assert isinstance(precio, (int, float))
            assert precio > 0
            descripcion = mueble.obtener_descripcion()
            assert isinstance(descripcion, str)
            assert len(descripcion) > 0

    def test_encapsulacion_general(self):
        """Prueba que la encapsulación funciona correctamente."""
        silla = Silla("Silla Test", "Madera", "Negra", 100.0, True)

        # Probar que los getters funcionan
        assert silla.nombre == "Silla Test"
        assert silla.material == "Madera"
        assert silla.color == "Negra"
        assert silla.precio_base == 100.0

        # Probar que los setters funcionan con valores válidos
        silla.nombre = "Nuevo Nombre"
        assert silla.nombre == "Nuevo Nombre"

        silla.material = "Metal"
        assert silla.material == "Metal"

        silla.color = "Blanco"
        assert silla.color == "Blanco"

        silla.precio_base = 150.0
        assert silla.precio_base == 150.0

        # Probar que los setters rechazan valores inválidos
        with pytest.raises(ValueError):
            silla.nombre = ""  # Nombre vacío

        with pytest.raises(ValueError):
            silla.nombre = "   "  # Solo espacios

        with pytest.raises(ValueError):
            silla.precio_base = -10.0  # Precio negativo

        # Probar encapsulamiento de atributos específicos de Silla
        silla.altura_regulable = True
        assert silla.altura_regulable == True

        silla.tiene_ruedas = True
        assert silla.tiene_ruedas == True

        # Para booleanos, intentamos asignar valores que no sean booleanos válidos
        # En Python, solo True y False son booleanos válidos
        with pytest.raises(ValueError):
            silla.altura_regulable = 1  # Entero no es booleano

        with pytest.raises(ValueError):
            silla.tiene_ruedas = 0  # Entero no es booleano

    def test_herencia_jerarquia(self):
        """Prueba que la jerarquía de herencia funciona correctamente."""
        from models.categorias.almacenamiento import Almacenamiento
        from models.categorias.asientos import Asiento
        from models.categorias.superficies import Superficie
        from models.concretos.cama import Cama
        from models.concretos.mesa import Mesa
        from models.concretos.silla import Silla
        from models.concretos.sofa import Sofa
        from models.concretos.sofacama import SofaCama

        # Crear instancias
        silla = Silla("Silla Test", "Madera", "Negra", 100.0, True)
        mesa = Mesa(
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
        cama = Cama(
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
        sofá = Sofa(
            "Sofá Test", "Tela", "Gris", 400.0, True, "tela", 3, False, False, False
        )
        sofacama = SofaCama("Sofá-Cama Test", "Tela", "Azul", 500.0)

        # Verificar relaciones de herencia
        # Silla hereda de Asiento
        assert isinstance(silla, Asiento)

        # SofáCama hereda de tanto Sofa como Cama (herencia múltiple)
        assert isinstance(sofacama, Sofa)
        assert isinstance(sofacama, Cama)

        # SofáCama también hereda de Asiento (a través de Sofa) y Superficie (a través de Cama)
        assert isinstance(sofacama, Asiento)
        assert isinstance(sofacama, Superficie)

        # Verificar que todos heredan de Mueble
        from models.mueble import Mueble

        assert isinstance(silla, Mueble)
        assert isinstance(mesa, Mueble)
        assert isinstance(cama, Mueble)
        assert isinstance(sofá, Mueble)
        assert isinstance(sofacama, Mueble)

        # Verificar la cadena de herencia (MRO - Method Resolution Order) para SofaCama
        # En caso de conflicto, Sofa se resuelve antes que Cama (orden de declaración)
        mro = SofaCama.__mro__
        assert SofaCama in mro
        assert Sofa in mro
        assert Cama in mro
        assert Asiento in mro  # A través de Sofa
        assert Superficie in mro  # A través de Cama
        assert Mueble in mro
        assert object in mro  # Siempre último


# Agregar fixture para datos de prueba si es necesario
@pytest.fixture
def muebles_de_prueba():
    """Fixture que proporciona muebles de prueba para múltiples tests."""
    return {
        "silla_basica": Silla("Silla Test", "Madera", "Café", 100.0, True),
        "mesa_basica": Mesa(
            "Mesa Test",
            "Madera",
            "Roble",
            300.0,
            2.0,
            1.0,
            0.75,
            100.0,
            "Madera",
            4,
            "rectangular",
        ),
        "sofacama": SofaCama("SofaCama Test", "Tela", "Gris", 800.0),
    }


class TestIntegracion:
    """
    Pruebas de integración que validan el funcionamiento conjunto de múltiples clases.
    """

    def test_creacion_tienda_completa(self):
        """Prueba la creación de una tienda con múltiples tipos de muebles."""

        from services.tienda import TiendaMuebles

        tienda = TiendaMuebles("Tienda Test")

        # Crear muebles variados
        silla = Silla(
            "Silla Ergonomica", "Metal", "Negra", 250.0, True, "malla", True, True
        )
        mesa = Mesa(
            "Mesa de Centro",
            "Vidrio",
            "Transparente",
            180.0,
            1.2,
            0.6,
            0.4,
            80.0,
            "Vidrio Templado",
            4,
            "redonda",
        )
        cama = Cama(
            "Cama King",
            "Madera",
            "Cerezo",
            600.0,
            2.0,
            2.0,
            0.6,
            250.0,
            "Lino",
            True,
            "king",
            True,
            0.8,
            4,
        )
        sofa = Sofa(
            "Sofa Seccional",
            "Tela",
            "Azul Marino",
            900.0,
            True,
            "chenille",
            5,
            True,
            False,
            True,
        )
        comedor_mesa = Mesa(
            "Mesa Comedor",
            "Roble",
            "Natural",
            400.0,
            2.5,
            1.2,
            0.8,
            150.0,
            "Barnizado",
            6,
            "rectangular",
        )
        comedor_silla1 = Silla("Silla Comedor 1", "Roble", "Natural", 180.0, True)
        comedor_silla2 = Silla("Silla Comedor 2", "Roble", "Natural", 180.0, True)
        comedor_silla3 = Silla("Silla Comedor 3", "Roble", "Natural", 180.0, True)
        comedor_silla4 = Silla("Silla Comedor 4", "Roble", "Natural", 180.0, True)
        comedor = Comedor(
            "Comedor Elegante",
            comedor_mesa,
            [comedor_silla1, comedor_silla2, comedor_silla3, comedor_silla4],
        )

        # Agregar a la tienda
        assert (
            tienda.agregar_mueble(silla)
            == "Mueble Silla Ergonomica agregado exitosamente al inventario"
        )
        assert (
            tienda.agregar_mueble(mesa)
            == "Mueble Mesa de Centro agregado exitosamente al inventario"
        )
        assert (
            tienda.agregar_mueble(cama)
            == "Mueble Cama King agregado exitosamente al inventario"
        )
        assert (
            tienda.agregar_mueble(sofa)
            == "Mueble Sofa Seccional agregado exitosamente al inventario"
        )
        assert (
            tienda.agregar_comedor(comedor)
            == "Comedor Comedor Elegante agregado exitosamente"
        )

        # Verificar el inventario
        assert tienda.total_muebles == 4  # 4 muebles individuales
        assert len(tienda._comedores) == 1  # 1 comedor
        assert tienda.calcular_valor_inventario() > 0

        # Verificar búsquedas
        # Búsqueda por nombre exacto
        resultados = tienda.buscar_muebles_por_nombre("Silla Ergonomica")
        assert len(resultados) == 1
        assert resultados[0] == silla

        # Búsqueda por coincidencia parcial
        resultados = tienda.buscar_muebles_por_nombre("Silla")
        assert len(resultados) >= 1  # Al menos la silla ergonomica
        assert silla in resultados

        # Búsqueda case insensitive
        resultados = tienda.buscar_muebles_por_nombre("mesa")
        assert (
            len(resultados) == 1
        )  # Solo Mesa de Centro (la Mesa Comedor está dentro del comedor)
        assert resultados[0].nombre == "Mesa de Centro"

        # Verificar filtros
        # Filtrar por precio
        resultados = tienda.filtrar_por_precio(precio_min=200, precio_max=300)
        assert len(resultados) >= 1
        assert silla in resultados  # La silla cuesta más de 200 y menos de 300

        # Filtrar por material
        resultados = tienda.filtrar_por_material("Madera")
        assert (
            len(resultados) >= 1
        )  # Solo la cama (el comedor está en _comedores, no en _inventario)
        assert cama in resultados
        # El comedor no aparece aquí porque está en _comedores, no en _inventario

        # Filtrar por tipo
        sillas = tienda.obtener_muebles_por_tipo(Silla)
        assert len(sillas) == 1
        assert sillas[0] == silla

        mesas = tienda.obtener_muebles_por_tipo(Mesa)
        assert (
            len(mesas) == 1
        )  # Solo Mesa de Centro (la Mesa Comedor está dentro del comedor)
        assert mesa in mesas
        # La Mesa Comedor no aparece aquí porque está dentro del comedor, no en el inventario directo

        # Verificar descuentos
        assert (
            tienda.aplicar_descuento("sillas", 15)
            == "Descuento del 15% aplicado a la categoría 'sillas'"
        )
        assert (
            tienda.aplicar_descuento("mesas", 10)
            == "Descuento del 10% aplicado a la categoría 'mesas'"
        )
        assert len(tienda._descuentos_activos) == 2

        # Verificar venta
        venta = tienda.realizar_venta(silla, "Cliente VIP")
        assert "error" not in venta
        assert venta["mueble"] == "Silla Ergonomica"
        assert venta["cliente"] == "Cliente VIP"
        assert tienda.total_muebles == 3  # Un mueble menos después de la venta
        assert len(tienda._ventas_realizadas) == 1

        # Verificar estadísticas
        stats = tienda.obtener_estadisticas()
        assert stats["total_muebles"] == 3
        assert stats["total_comedores"] == 1
        assert stats["ventas_realizadas"] == 1
        assert stats["descuentos_activos"] == 2
        # Después de vender la silla, no debería haber sillas en el inventario
        assert (
            "Silla" not in stats["tipos_muebles"]
            or stats["tipos_muebles"]["Silla"] == 0
        )

        # Verificar reporte
        reporte = tienda.generar_reporte_inventario()
        assert "REPORTE DE INVENTARIO" in reporte
        assert tienda.nombre in reporte
        assert "DESCUENTOS ACTIVOS:" in reporte


if __name__ == "__main__":
    # Configurar ejecución de pruebas
    pytest.main([__file__, "-v"])
