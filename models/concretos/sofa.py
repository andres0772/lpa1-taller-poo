"""
Clase concreta Sofa.
"""

from ..categorias.asientos import Asiento


class Sofa(Asiento):
    """
    Clase concreta que representa un sofá.
    """

    def __init__(
        self,
        nombre: str,
        material: str,
        color: str,
        precio_base: float,
        tiene_respaldo: bool,
        material_tapizado: str,
        numero_cojines: int,
        tiene_chaiselongue: bool,
        altura_regulable: bool = False,
        tiene_ruedas: bool = False,
    ):
        """
        Constructor del sofá.

        Args:
            nombre: Nombre del sofá
            material: Material del sofá
            color: Color del sofá
            precio_base: Precio base del sofá
            tiene_respaldo: Si el sofá tiene respaldo
            material_tapizado: Material del tapizado
            numero_cojines: Número de cojines
            tiene_chaiselongue: Si tiene chaise longue
            altura_regulable: Si tiene altura regulable
            tiene_ruedas: Si tiene ruedas
        """
        # Un sofá típico tiene capacidad para más de una persona
        super().__init__(
            nombre, material, color, precio_base, 3, tiene_respaldo, material_tapizado
        )
        self.numero_cojines = numero_cojines
        self.tiene_chaiselongue = tiene_chaiselongue
        self.altura_regulable = altura_regulable
        self.tiene_ruedas = tiene_ruedas

    @property
    def numero_cojines(self) -> int:
        """Getter para el número de cojines."""
        return self._numero_cojines

    @numero_cojines.setter
    def numero_cojines(self, value: int) -> None:
        """Setter para el número de cojines con validación."""
        if not isinstance(value, int) or value < 0:
            raise ValueError("numero_cojines debe ser un entero no negativo")
        self._numero_cojines = value

    @property
    def tiene_chaiselongue(self) -> bool:
        """Getter para tiene chaise longue."""
        return self._tiene_chaiselongue

    @tiene_chaiselongue.setter
    def tiene_chaiselongue(self, value: bool) -> None:
        """Setter para tiene chaise longue con validación."""
        if not isinstance(value, bool):
            raise ValueError("tiene_chaiselongue debe ser booleano")
        self._tiene_chaiselongue = value

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

    @property
    def tiene_ruedas(self) -> bool:
        """Getter para tiene ruedas."""
        return self._tiene_ruedas

    @tiene_ruedas.setter
    def tiene_ruedas(self, value: bool) -> None:
        """Setter para tiene ruedas con validación."""
        if not isinstance(value, bool):
            raise ValueError("tiene_ruedas debe ser booleano")
        self._tiene_ruedas = value

    def calcular_precio(self) -> float:
        """
        Implementa el cálculo de precio específico para sofás.

        Returns:
            float: Precio final del sofá
        """
        # Comenzar con el precio base
        precio = self.precio_base

        # Aplicar factor de comodidad heredado
        factor = self.calcular_factor_comodidad()
        precio *= factor

        # Agregar costos por características específicas del sofá
        precio += self.numero_cojines * 5.0  # $5 por cojín
        if self.tiene_chaiselongue:
            precio += 30.0  # $30 adicional por chaise longue
        if self.altura_regulable:
            precio += 15.0  # $15 adicional por altura regulable
        if self.tiene_ruedas:
            precio += 10.0  # $10 adicional por ruedas

        # Retornar precio redondeado a 2 decimales
        return round(precio, 2)

    def obtener_descripcion(self) -> str:
        """
        Implementa la descripción específica del sofá.

        Returns:
            str: Descripción completa del sofá
        """
        return (
            f"{self.nombre} de {self.material} en color {self.color}, "
            f"capacidad {self.capacidad_personas} personas, "
            f"respaldo {'Sí' if self.tiene_respaldo else 'No'}, "
            f"tapizado {self.material_tapizado or 'Ninguno'}, "
            f"número de cojines: {self.numero_cojines}, "
            f"chaise longue: {'Sí' if self.tiene_chaiselongue else 'No'}, "
            f"altura regulable: {'Sí' if self.altura_regulable else 'No'}, "
            f"ruedas: {'Sí' if self.tiene_ruedas else 'No'}"
        )
