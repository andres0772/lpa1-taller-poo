"""
Clase SofaCama que implementa herencia múltiple.
Esta clase hereda tanto de Sofa como de Cama.
"""

from .cama import Cama
from .sofa import Sofa


class SofaCama(Sofa, Cama):
    """
    Clase que representa un sofá-cama, heredando de Sofa y Cama.

    Un sofá-cama es un mueble que funciona tanto como asiento durante el día
    como cama durante la noche.
    """

    def __init__(
        self,
        nombre: str,
        material: str,
        color: str,
        precio_base: float,
        # Parámetros de Sofa
        tiene_respaldo: bool = True,
        material_tapizado: str = "tela",
        numero_cojines: int = 2,
        tiene_chaiselongue: bool = False,
        altura_regulable: bool = False,
        tiene_ruedas: bool = False,
        # Parámetros de Cama
        largo: float = 2.0,
        ancho: float = 1.5,
        altura: float = 0.5,
        resistencia_peso: float = 200.0,
        material_superficie: str = "tela",
        es_extensible: bool = True,
        tipo: str = "matrimonial",
        tiene_cabecero: bool = True,
        altura_max: float = 1.0,
        numero_pillows: int = 2,
    ):
        """
        Constructor del sofá-cama.

        Args:
            nombre: Nombre del sofá-cama
            material: Material del sofá-cama
            color: Color del sofá-cama
            precio_base: Precio base del sofá-cama
            tiene_respaldo: Si el sofá-cama tiene respaldo
            material_tapizado: Material del tapizado
            numero_cojines: Número de cojines
            tiene_chaiselongue: Si tiene chaise longue
            altura_regulable: Si tiene altura regulable
            tiene_ruedas: Si tiene ruedas
            largo: Largo de la cama
            ancho: Ancho de la cama
            altura: Altura de la cama
            resistencia_peso: Resistencia al peso de la cama
            material_superficie: Material de la superficie de la cama
            es_extensible: Si la cama es extensible
            tipo: Tipo de cama (individual, matrimonial, etc.)
            tiene_cabecero: Si la cama tiene cabecero
            altura_max: Altura máxima (para camas ajustables)
            numero_pillows: Número de almohadas incluidas
        """
        # Inicializar la clase base Mueble explícitamente para evitar doble inicialización
        from ..mueble import Mueble

        Mueble.__init__(self, nombre, material, color, precio_base)

        # Inicializar atributos de Asiento usando los setters (capacidad_personas fija a 3 como en Sofa)
        self.capacidad_personas = 3
        self.tiene_respaldo = tiene_respaldo
        self.material_tapizado = material_tapizado

        # Inicializar atributos específicos de Sofa usando los setters
        self.numero_cojines = numero_cojines
        self.tiene_chaiselongue = tiene_chaiselongue
        self.altura_regulable = altura_regulable
        self.tiene_ruedas = tiene_ruedas

        # Inicializar atributos de Superficie usando los setters
        self.largo = largo
        self.ancho = ancho
        self.altura = altura
        self.resistencia_peso = resistencia_peso
        self.material_superficie = material_superficie
        self.es_extensible = es_extensible

        # Inicializar atributos específicos de Cama usando los setters
        self.tipo = tipo
        self.tiene_cabecero = tiene_cabecero
        self.altura_max = altura_max
        self.numero_pillows = numero_pillows

        # Inicializar modo actual (por defecto comienza como sofá)
        self._modo_actual = "sofa"

    @property
    def modo_actual(self) -> str:
        """Propiedad que devuelve el modo actual del sofá-cama."""
        return self._modo_actual

    def convertir_a_cama(self) -> str:
        """
        Convierte el sofá-cama a modo cama.

        Returns:
            str: Mensaje indicando el resultado de la conversión
        """
        if self._modo_actual == "cama":
            return "Ya está en modo cama"
        self._modo_actual = "cama"
        return "convertido a cama"

    def convertir_a_sofa(self) -> str:
        """
        Convierte el sofá-cama a modo sofá.

        Returns:
            str: Mensaje indicando el resultado de la conversión
        """
        if self._modo_actual == "sofa":
            return "Ya está en modo sofá"
        self._modo_actual = "sofa"
        return "convertida a sofá"

    def obtener_capacidad_total(self) -> dict:
        """
        Obtiene la capacidad total en ambos modos.

        Returns:
            dict: Diccionario con las capacidades en modo sofá y cama
        """
        # Capacidad en modo sofá (heredada de Asiento/Sofa)
        capacidad_sofa = self.capacidad_personas

        # Capacidad en modo cama (asumimos 2 personas para una cama estándar)
        # Podemos basarnos en el tipo de cama o usar un valor fijo
        capacidad_cama = 2  # Valor estándar para cama

        return {
            "sofa": capacidad_sofa,
            "cama": capacidad_cama,
            "total": capacidad_sofa + capacidad_cama,
        }

    def calcular_precio(self) -> float:
        """
        Calcula el precio combinando las funcionalidades de sofá y cama.

        Returns:
            float: Precio final del sofá-cama
        """
        # Comenzar con el precio base
        precio = self.precio_base

        # Aplicar factor de comodidad heredado de Sofa
        factor_comodidad = self.calcular_factor_comodidad()
        precio *= factor_comodidad

        # Agregar costos por características específicas del sofá
        precio += self.numero_cojines * 5.0  # $5 por cojín
        if self.tiene_chaiselongue:
            precio += 30.0  # $30 adicional por chaise longue
        if self.altura_regulable:
            precio += 15.0  # $15 adicional por altura regulable
        if self.tiene_ruedas:
            precio += 10.0  # $10 adicional por ruedas

        # Aplicar factor basado en el tipo de cama (de Cama)
        factor_tipo = 1.0
        if self.tipo.lower() == "matrimonial":
            factor_tipo = 1.2
        elif self.tipo.lower() in ["king", "queen"]:
            factor_tipo = 1.5
        elif self.tipo.lower() == "individual":
            factor_tipo = 1.0
        else:
            factor_tipo = 1.1  # Tipo estándar

        precio *= factor_tipo

        # Agregar costos por características específicas de la cama
        if self.tiene_cabecero:
            precio += 25.0  # $25 adicional por tener cabecero

        # Costo adicional por almohadas
        precio += self.numero_pillows * 8.0  # $8 por almohada

        # Costo adicional por ser extensible
        if self.es_extensible:
            precio += 40.0  # $40 adicional por ser extensible

        sobrecosto_dual = self.precio_base * 0.5  # 50% del precio base
        precio += sobrecosto_dual + 100.0 + 300.0  # mecanismo + colchón

        # Retornar precio redondeado a 2 decimales
        return round(precio, 2)

    def obtener_descripcion(self) -> str:
        """
        Proporciona una descripción que combina características de sofá y cama.

        Returns:
            str: Descripción completa del sofá-cama
        """
        return (
            f"Sofá-cama {self.nombre} de {self.material} en color {self.color}, "
            f"capacidad {self.capacidad_personas} personas, "
            f"respaldo {'Sí' if self.tiene_respaldo else 'No'}, "
            f"tapizado {self.material_tapizado or 'Ninguno'}, "
            f"número de cojines: {self.numero_cojines}, "
            f"chaise longue: {'Sí' if self.tiene_chaiselongue else 'No'}, "
            f"altura regulable: {'Sí' if self.altura_regulable else 'No'}, "
            f"ruedas: {'Sí' if self.tiene_ruedas else 'No'}, "
            f"tipo de cama: {self.tipo}, "
            f"dimensiones {self.largo}m x {self.ancho}m x {self.altura}m, "
            f"resistencia de peso: {self.resistencia_peso}kg, "
            f"material de superficie: {self.material_superficie}, "
            f"extensible: {'Sí' if self.es_extensible else 'No'}, "
            f"tiene cabecero: {'Sí' if self.tiene_cabecero else 'No'}, "
            f"altura máxima: {self.altura_max}m, "
            f"incluye {self.numero_pillows} almohada(s)"
        )
