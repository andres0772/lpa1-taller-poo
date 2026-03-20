"""
Clase abstracta para muebles de asiento.
Esta clase agrupa las características comunes de sillas, sillones y sofás.
"""

from abc import ABC, abstractmethod

from ..mueble import Mueble


class Asiento(Mueble, ABC):
    """
    Clase abstracta para todos los muebles donde las personas se sientan.

    Hereda de Mueble y añade características específicas de los asientos
    como capacidad de personas, tipo de respaldo, etc.

    Conceptos OOP aplicados:
    - Herencia: Extiende la clase Mueble
    - Abstracción: Agrupa características comunes de asientos
    - Polimorfismo: Permite diferentes implementaciones del cálculo de comodidad
    """

    def __init__(
        self,
        nombre: str,
        material: str,
        color: str,
        precio_base: float,
        capacidad_personas: int,
        tiene_respaldo: bool,
        material_tapizado: str | None = None,
    ):
        """
        Constructor para muebles de asiento.

        Args:
            capacidad_personas: Número de personas que pueden sentarse
            tiene_respaldo: Si el asiento tiene respaldo o no
            material_tapizado: Material del tapizado (opcional)
            Otros argumentos heredados de Mueble
        """
        super().__init__(nombre, material, color, precio_base)
        self.capacidad_personas = capacidad_personas
        self.tiene_respaldo = tiene_respaldo
        self.material_tapizado = material_tapizado

    @property
    def capacidad_personas(self) -> int:
        """Getter para la capacidad de personas."""
        return self._capacidad_personas

    @capacidad_personas.setter
    def capacidad_personas(self, value: int) -> None:
        """Setter para capacidad con validación."""
        if value <= 0:
            raise ValueError("La capacidad debe ser mayor a 0")
        self._capacidad_personas = value

    @property
    def tiene_respaldo(self) -> bool:
        """Getter para si el asiento tiene respaldo."""
        return self._tiene_respaldo

    @tiene_respaldo.setter
    def tiene_respaldo(self, value: bool) -> None:
        """Setter para si el asiento tiene respaldo con validación."""
        if not isinstance(value, bool):
            raise ValueError("El valor debe ser Booleano")
        self._tiene_respaldo = value

    @property
    def material_tapizado(self) -> str | None:
        """Getter para el material del tapizado"""

        return self._material_tapizado

    @material_tapizado.setter
    def material_tapizado(self, value: str | None) -> None:
        """Setter para el material del tapizado con validación."""
        if value is not None:
            if not isinstance(value, str):
                raise ValueError("material_tapizado debe ser string o None")
            stripped = value.strip()
            if not stripped:
                raise ValueError(
                    "material_tapizado no puede estar vacío o contener solo espacios"
                )
            self._material_tapizado = stripped
        else:
            self._material_tapizado = None

    def calcular_factor_comodidad(self) -> float:
        """
        Calcula un factor de comodidad basado en las características del asiento.
        Este es un método concreto que pueden usar las clases hijas.

        Returns:
            float: Factor multiplicador para el precio (1.0 = neutral)
        """
        factor = 1.0

        if self.tiene_respaldo:
            factor += 0.1

        if self.material_tapizado:
            if self.material_tapizado.lower() == "cuero":
                factor += 0.2
            elif self.material_tapizado.lower() == "tela":
                factor += 0.1

        factor += (self.capacidad_personas - 1) * 0.05

        return factor

    def obtener_info_asiento(self) -> str:
        """
        Obtiene información específica del asiento.
        Método concreto auxiliar para las clases hijas.

        Returns:
            str: Información detallada del asiento
        """
        info = f"Capacidad: {self.capacidad_personas} personas"
        if self.tiene_respaldo:
            info += f", Respaldo: {'Sí' if self.tiene_respaldo else 'No'}"
        if self.material_tapizado:
            info += f", Tapizado: {self.material_tapizado}"
        return info

    @abstractmethod
    def calcular_precio(self) -> float:
        """
        Calcula el precio del asiento.
        Método abstracto que debe ser implementado por las clases hijas.
        """
        pass

    @abstractmethod
    def obtener_descripcion(self) -> str:
        """
        Obtiene la descripción del asiento.
        Método abstracto que debe ser implementado por las clases hijas.
        """
        pass
