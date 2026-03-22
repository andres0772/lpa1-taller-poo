"""
Clase concreta Armario.
"""

from ..categorias.almacenamiento import Almacenamiento


class Armario(Almacenamiento):
    """
    Clase concreta que representa un armario.
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
        tiene_barro: bool,
        numero_gavetas: int,
        altura_colgador: float,
    ):
        """
        Constructor para armarios.
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
        self.tiene_barro = tiene_barro
        self.numero_gavetas = numero_gavetas
        self.altura_colgador = altura_colgador

    @property
    def tiene_barro(self) -> bool:
        """Getter para si tiene barro (río para colgar ropa)."""
        return self._tiene_barro

    @tiene_barro.setter
    def tiene_barro(self, value: bool) -> None:
        """Setter para tiene_barro con validación."""
        if not isinstance(value, bool):
            raise ValueError("tiene_barro debe ser booleano")
        self._tiene_barro = value

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
    def altura_colgador(self) -> float:
        """Getter para la altura del colgador."""
        return self._altura_colgador

    @altura_colgador.setter
    def altura_colgador(self, value: float) -> None:
        """Setter para altura del colgador con validación."""
        if value <= 0:
            raise ValueError("La altura del colgador debe ser positiva")
        self._altura_colgador = value

    def calcular_precio(self) -> float:
        """
        Calcula el precio del armario.
        Fórmula: precio_base + 10% por puerta + 5% por estante + 15% si tiene barro + 20% por gaveta
        """
        precio = self.precio_base
        precio += self.numero_puertas * (self.precio_base * 0.1)
        precio += self.numero_estantes * (self.precio_base * 0.05)
        if self.tiene_barro:
            precio += self.precio_base * 0.15
        precio += self.numero_gavetas * (self.precio_base * 0.2)
        return round(precio, 2)

    def obtener_descripcion(self) -> str:
        """
        Obtiene una descripción completa del armario.
        """
        desc = f"Armario {self.nombre} de {self.material} color {self.color}"
        desc += f" con {self.numero_puertas} puertas y {self.numero_estantes} estantes"
        desc += f", {'con' if self.tiene_cajones else 'sin'} cajones"
        desc += f", {'con' if self.tiene_barro else 'sin'} barro para colgar ropa"
        desc += f" ({self.numero_gavetas} gavetas internas)"
        desc += f" y altura de colgador de {self.altura_colgador}m"
        desc += f". Precio calculado: ${self.calcular_precio()}"
        return desc
