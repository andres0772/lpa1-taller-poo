"""
Clase concreta Cajonera.
"""

from ..categorias.almacenamiento import Almacenamiento


class Cajonera(Almacenamiento):
    """
    Clase concreta que representa una cajonera.
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
        numero_gavetas: int,
        altura_gaveta: float,
        tiene_separadores: bool,
    ):
        """
        Constructor para cajoneras.
        """
        super().__init__(
            nombre,
            material,
            color,
            precio_base,
            numero_puertas,
            numero_estantes,
            tiene_cajones,
        )
        self.numero_gavetas = numero_gavetas
        self.altura_gaveta = altura_gaveta
        self.tiene_separadores = tiene_separadores

    @property
    def numero_gavetas(self) -> int:
        """Getter para el número de gavetas."""
        return self._numero_gavetas

    @numero_gavetas.setter
    def numero_gavetas(self, value: int) -> None:
        """Setter para número de gavetas con validación."""
        if value < 0:
            raise ValueError("El número de gavetas no puede ser negativo")
        self._numero_gavetas = value

    @property
    def altura_gaveta(self) -> float:
        """Getter para la altura de las gavetas."""
        return self._altura_gaveta

    @altura_gaveta.setter
    def altura_gaveta(self, value: float) -> None:
        """Setter para altura de gavetas con validación."""
        if value <= 0:
            raise ValueError("La altura de las gavetas debe ser mayor a cero")
        self._altura_gaveta = value

    @property
    def tiene_separadores(self) -> bool:
        """Getter para si tiene separadores."""
        return self._tiene_separadores

    @tiene_separadores.setter
    def tiene_separadores(self, value: bool) -> None:
        """Setter para tiene_separadores con validación."""
        if not isinstance(value, bool):
            raise ValueError("tiene_separadores debe ser booleano")
        self._tiene_separadores = value

    def calcular_precio(self) -> float:
        """
        Calcula el precio de la cajonera.
        Fórmula: precio_base + (10 * numero_gavetas) + (5 * altura_gaveta) + (30 si tiene_separadores)
        """
        precio = self.precio_base
        precio += self.numero_gavetas * 10
        precio += self.altura_gaveta * 5
        if self.tiene_separadores:
            precio += 30
        return round(precio, 2)

    def obtener_descripcion(self) -> str:
        """
        Obtiene una descripción completa de la cajonera.
        """
        desc = f"Cajonera {self.nombre} de {self.material} color {self.color}"
        desc += f" con {self.numero_puertas} puertas y {self.numero_estantes} estantes"
        desc += f", {'con' if self.tiene_cajones else 'sin'} cajones"
        desc += f" ({self.numero_gavetas} gavetas de {self.altura_gaveta}cm de altura)"
        desc += f", {'con' if self.tiene_separadores else 'sin'} separadores"
        desc += f". Precio calculado: ${self.calcular_precio()}"
        return desc
