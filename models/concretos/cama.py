"""
Clase concreta Cama.
"""

from ..categorias.superficies import Superficie


class Cama(Superficie):
    """
    Clase concreta que representa una cama.
    """

    def __init__(
        self,
        nombre: str,
        material: str,
        color: str,
        precio_base: float,
        largo: float,
        ancho: float,
        altura: float,
        resistencia_peso: float,
        material_superficie: str,
        es_extensible: bool,
        tipo: str,
        tiene_cabecero: bool,
        altura_max: float,
        numero_pillows: int,
    ):
        """
        Constructor de la cama.

        Args:
            nombre: Nombre de la cama
            material: Material de la cama
            color: Color de la cama
            precio_base: Precio base de la cama
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
        super().__init__(
            nombre,
            material,
            color,
            precio_base,
            largo,
            ancho,
            altura,
            resistencia_peso,
            material_superficie,
            es_extensible,
        )
        self.tipo = tipo
        self.tiene_cabecero = tiene_cabecero
        self.altura_max = altura_max
        self.numero_pillows = numero_pillows

    @property
    def tipo(self) -> str:
        """Getter para el tipo de cama."""
        return self._tipo

    @tipo.setter
    def tipo(self, value: str) -> None:
        """Setter para el tipo de cama con validación."""
        if not isinstance(value, str):
            raise ValueError("tipo debe ser una cadena de texto")
        stripped = value.strip()
        if not stripped:
            raise ValueError("tipo no puede estar vacío o contener solo espacios")
        self._tipo = stripped

    @property
    def tiene_cabecero(self) -> bool:
        """Getter para indica si la cama tiene cabecero."""
        return self._tiene_cabecero

    @tiene_cabecero.setter
    def tiene_cabecero(self, value: bool) -> None:
        """Setter para tiene_cabecero con validación."""
        if not isinstance(value, bool):
            raise ValueError("tiene_cabecero debe ser booleano")
        self._tiene_cabecero = value

    @property
    def altura_max(self) -> float:
        """Getter para la altura máxima de la cama."""
        return self._altura_max

    @altura_max.setter
    def altura_max(self, value: float) -> None:
        """Setter para la altura máxima con validación."""
        if not isinstance(value, (int, float)):
            raise ValueError("altura_max debe ser un número")
        if value <= 0:
            raise ValueError("altura_max debe ser mayor que 0")
        self._altura_max = float(value)

    @property
    def numero_pillows(self) -> int:
        """Getter para el número de almohadas incluidas."""
        return self._numero_pillows

    @numero_pillows.setter
    def numero_pillows(self, value: int) -> None:
        """Setter para el número de almohadas con validación."""
        if not isinstance(value, int):
            raise ValueError("numero_pillows debe ser un entero")
        if value < 0:
            raise ValueError("numero_pillows no puede ser negativo")
        self._numero_pillows = value

    def calcular_precio(self) -> float:
        """
        Implementa el cálculo de precio específico para camas.

        Returns:
            float: Precio final de la cama
        """
        # Comenzar con el precio base
        precio = self.precio_base

        # Aplicar factor basado en el tipo de cama
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

        # Retornar precio redondeado a 2 decimales
        return round(precio, 2)

    def obtener_descripcion(self) -> str:
        """
        Implementa la descripción específica de la cama.

        Returns:
            str: Descripción completa de la cama
        """
        return (
            f"{self.nombre} de {self.material} en color {self.color}, "
            f"tipo {self.tipo}, "
            f"dimensiones {self.largo}m x {self.ancho}m x {self.altura}m, "
            f"resistencia de peso: {self.resistencia_peso}kg, "
            f"material de superficie: {self.material_superficie}, "
            f"extensible: {'Sí' if self.es_extensible else 'No'}, "
            f"tiene cabecero: {'Sí' if self.tiene_cabecero else 'No'}, "
            f"altura máxima: {self.altura_max}m, "
            f"incluye {self.numero_pillows} almohada(s)"
        )
