"""
Clase abstracta para muebles de almacenamiento.
"""

from abc import ABC, abstractmethod

from ..mueble import Mueble


class Almacenamiento(Mueble, ABC):
    """
    Clase abstracta para todos los muebles de guardar cosas.
    """

    def __init__(
        self,
        nombre: str,
        material: str,
        color: str,
        precio_base: float,
        numero_puertas: int,
        numero_estantes: int,
        tiene_cajones: bool,
    ):
        """
        Constructor para muebles de almacenamiento.
        """
        super().__init__(nombre, material, color, precio_base)
        self.numero_puertas = numero_puertas
        self.numero_estantes = numero_estantes
        self.tiene_cajones = tiene_cajones

    @property
    def numero_puertas(self) -> int:
        """Getter para el número de puertas."""
        return self._numero_puertas

    @numero_puertas.setter
    def numero_puertas(self, value: int) -> None:
        """Setter para número de puertas con validación."""
        if value < 0:
            raise ValueError("El número de puertas no puede ser negativo")
        self._numero_puertas = value

    @property
    def numero_estantes(self) -> int:
        """Getter para el número de estantes."""
        return self._numero_estantes

    @numero_estantes.setter
    def numero_estantes(self, value: int) -> None:
        """Setter para número de estantes con validación."""
        if value < 0:
            raise ValueError("El número de estantes no puede ser negativo")
        self._numero_estantes = value

    @property
    def tiene_cajones(self) -> bool:
        """Getter para si tiene cajones."""
        return self._tiene_cajones

    @tiene_cajones.setter
    def tiene_cajones(self, value: bool) -> None:
        """Setter para tiene_cajones con validación."""
        if not isinstance(value, bool):
            raise ValueError("tiene_cajones debe ser booleano")
        self._tiene_cajones = value

    def obtener_info_almacenamiento(self) -> str:
        """Obtiene información específica del almacenamiento."""
        info = f"Puertas: {self.numero_puertas}"
        info += f", Estantes: {self.numero_estantes}"
        info += f", Tiene cajones: {'Sí' if self.tiene_cajones else 'No'}"
        return info
