"""
Clase concreta Mesa.
"""

from ..categorias.superficies import Superficie


class Mesa(Superficie):
    """
    Clase concreta que representa una mesa.
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
        numero_patas: int,
        forma: str,
        es_extensible: bool = False,
    ):
        """
        Constructor de la mesa.

        Args:
            numero_patas: Número de patas o soportes
            forma: Forma de la superficie (rectangular, redonda, etc.)
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
        self.numero_patas = numero_patas
        self.forma = forma

    @property
    def numero_patas(self) -> int:
        """Getter para el número de patas."""
        return self._numero_patas

    @numero_patas.setter
    def numero_patas(self, value: int) -> None:
        """Setter para número de patas con validación."""
        if value < 1:
            raise ValueError("Una mesa debe tener al menos 1 pata o soporte")
        self._numero_patas = value

    @property
    def forma(self) -> str:
        """Getter para la forma de la superficie."""
        return self._forma

    @forma.setter
    def forma(self, value: str) -> None:
        """Setter para la forma con validación."""
        if not isinstance(value, str):
            raise ValueError("La forma debe ser una cadena de texto")
        stripped = value.strip()
        if not stripped:
            raise ValueError("La forma no puede estar vacía o contener solo espacios")
        self._forma = stripped

    def calcular_precio(self) -> float:
        """
        Implementa el cálculo de precio específico para mesas.

        Returns:
            float: Precio final de la mesa
        """
        precio = self.precio_base
        # Costo por número de patas (más patas = más material)
        precio += self.numero_patas * 5.0
        # Costo adicional por formas redondas u ovaladas (mayor complejidad de fabricación)
        if self.forma.lower() in {"redonda", "ovalada"}:
            precio += 15.0
        # Costo adicional si es extensible
        if self.es_extensible:
            precio += 20.0
        return round(precio, 2)

    def obtener_descripcion(self) -> str:
        """
        Implementa la descripción específica de la mesa.

        Returns:
            str: Descripción completa de la mesa
        """
        return (
            f"{self.nombre} de {self.material} en color {self.color}, "
            f"superficie: {self.largo}m x {self.ancho}m, altura: {self.altura}m, "
            f"resistencia: {self.resistencia_peso} kg, material de superficie: {self.material_superficie}, "
            f"patas: {self.numero_patas}, forma: {self.forma}, "
            f"extensible: {'Sí' if self.es_extensible else 'No'}"
        )
