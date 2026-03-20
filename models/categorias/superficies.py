"""
Clase abstracta para muebles para superficies de trabajo o del hogar.
"""

from abc import ABC, abstractmethod

from ..mueble import Mueble


class Superficie(Mueble, ABC):
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
    ):
        """Constructor para muebles de superficie."""
        super().__init__(nombre, material, color, precio_base)
        self.largo = largo
        self.ancho = ancho
        self.altura = altura
        self.resistencia_peso = resistencia_peso
        self.material_superficie = material_superficie
        self.es_extensible = es_extensible

    @property
    def largo(self) -> float:
        """Getter para el largo de la superficie."""
        return self._largo

    @largo.setter
    def largo(self, value: float) -> None:
        """Setter para el largo de la superficie con validación."""
        if value <= 0:
            raise ValueError("El largo debe ser mayor que 0")
        self._largo = value

    @property
    def ancho(self) -> float:
        """Getter para el ancho de la superficie."""
        return self._ancho

    @ancho.setter
    def ancho(self, value: float) -> None:
        """Setter para el ancho de la superficie con validación."""
        if value <= 0:
            raise ValueError("El ancho debe ser mayor que 0")
        self._ancho = value

    @property
    def altura(self) -> float:
        """Getter para la altura de la superficie."""
        return self._altura

    @altura.setter
    def altura(self, value: float) -> None:
        """Setter para la altura de la superficie con validación."""
        if value <= 0:
            raise ValueError("La altura debe ser mayor que 0")
        self._altura = value

    @property
    def resistencia_peso(self) -> float:
        """Getter para la resistencia de peso de la superficie."""
        return self._resistencia_peso

    @resistencia_peso.setter
    def resistencia_peso(self, value: float) -> None:
        """Setter para la resistencia de peso de la superficie con validación."""
        if value <= 0:
            raise ValueError("La resistencia de peso debe ser mayor que 0")
        self._resistencia_peso = value

    @property
    def material_superficie(self) -> str:
        """Getter para el material de la superficie."""
        return self._material_superficie

    @material_superficie.setter
    def material_superficie(self, value: str) -> None:
        """Setter para el material de la superficie con validación."""
        if not isinstance(value, str):
            raise ValueError("material_superficie debe ser una cadena de texto")
        stripped = value.strip()
        if not stripped:
            raise ValueError(
                "material_superficie no puede estar vacío o contener solo espacios"
            )
        self._material_superficie = stripped

    @property
    def es_extensible(self) -> bool:
        """Getter para la extensibilidad de la superficie."""
        return self._es_extensible

    @es_extensible.setter
    def es_extensible(self, value: bool) -> None:
        """Setter para es_extensible con validación."""
        if not isinstance(value, bool):
            raise ValueError("es_extensible debe ser booleano")
        self._es_extensible = value

    def obtener_info_superficie(self) -> str:
        """Obtiene información específica de la superficie."""
        info = f"Dimensiones: {self.largo}m x {self.ancho}m x {self.altura}m"
        info += f", Resistencia de peso: {self.resistencia_peso}kg"
        info += f", Material de superficie: {self.material_superficie}"
        info += f", Extensible: {'Sí' if self.es_extensible else 'No'}"
        return info
