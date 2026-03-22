"""
Clase concreta Escritorio.
"""

from ..categorias.superficies import Superficie


class Escritorio(Superficie):
    """
    Clase concreta que representa un escritorio.
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
        es_extensible: bool = False,
        numero_cajones: int = 0,
        tiene_bandeja_teclado: bool = False,
        altura_regulable: bool = False,
    ):
        """
        Constructor del escritorio.

        Args:
            numero_cajones: Número de cajones
            tiene_bandeja_teclado: Si tiene bandeja para teclado
            altura_regulable: Si la altura es regulable
            Otros argumentos heredados de Superficie
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
        self.numero_cajones = numero_cajones
        self.tiene_bandeja_teclado = tiene_bandeja_teclado
        self.altura_regulable = altura_regulable

    @property
    def numero_cajones(self) -> int:
        """Getter para el número de cajones."""
        return self._numero_cajones

    @numero_cajones.setter
    def numero_cajones(self, value: int) -> None:
        """Setter para número de cajones con validación."""
        if value < 0:
            raise ValueError("El número de cajones no puede ser negativo")
        self._numero_cajones = value

    @property
    def tiene_bandeja_teclado(self) -> bool:
        """Getter para bandeja de teclado."""
        return self._tiene_bandeja_teclado

    @tiene_bandeja_teclado.setter
    def tiene_bandeja_teclado(self, value: bool) -> None:
        """Setter para bandeja de teclado con validación."""
        if not isinstance(value, bool):
            raise ValueError("tiene_bandeja_teclado debe ser booleano")
        self._tiene_bandeja_teclado = value

    @property
    def altura_regulable(self) -> bool:
        """Getter para altura regulable."""
        return self._altura_regulable

    @altura_regulable.setter
    def altura_regulable(self, value: bool) -> None:
        """Setter para altura regulable con validación."""
        if not isinstance(value, bool):
            raise ValueError("altura_regulable debe ser booleano")
        self._altura_regulable = value

    def calcular_precio(self) -> float:
        """
        Implementa el cálculo de precio específico para escritorios.

        Returns:
            float: Precio final del escritorio
        """
        precio = self.precio_base
        # Costo por número de cajones (más cajones = más material y mano de obra)
        precio += self.numero_cajones * 8.0
        # Costo adicional si tiene bandeja para teclado
        if self.tiene_bandeja_teclado:
            precio += 12.0
        # Costo adicional si la altura es regulable
        if self.altura_regulable:
            precio += 15.0

        return round(precio, 2)

    def obtener_descripcion(self) -> str:
        """
        Implementa la descripción específica del escritorio.

        Returns:
            str: Descripción completa del escritorio
        """
        return (
            f"{self.nombre} de {self.material} en color {self.color}, "
            f"superficie: {self.largo}m x {self.ancho}m, altura: {self.altura}m, "
            f"resistencia: {self.resistencia_peso} kg, material de superficie: {self.material_superficie}, "
            f"extensible: {'Sí' if self.es_extensible else 'No'}, "
            f"cajones: {self.numero_cajones}, bandeja teclado: {'Sí' if self.tiene_bandeja_teclado else 'No'}, "
            f"altura regulable: {'Sí' if self.altura_regulable else 'No'}"
        )
