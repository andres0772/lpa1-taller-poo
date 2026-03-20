"""
Clase concreta Silla.
Implementa un mueble de asiento específico para una persona.
"""

from ..categorias.asientos import Asiento


class Silla(Asiento):
    """
    Clase concreta que representa una silla.

    Una silla es un asiento individual con características específicas
    como altura regulable, ruedas, etc.

    Conceptos OOP aplicados:
    - Herencia: Hereda de Asiento
    - Polimorfismo: Implementa métodos abstractos de manera específica
    - Encapsulamiento: Protege atributos específicos de la silla
    """

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

    def __init__(
        self,
        nombre: str,
        material: str,
        color: str,
        precio_base: float,
        tiene_respaldo: bool = True,
        material_tapizado: str | None = None,
        altura_regulable: bool = False,
        tiene_ruedas: bool = False,
    ):
        """
        Constructor de la silla.

        Args:
            altura_regulable: Si la silla puede regular su altura
            tiene_ruedas: Si la silla tiene ruedas
            Otros argumentos heredados de Asiento
        """
        super().__init__(
            nombre, material, color, precio_base, 1, tiene_respaldo, material_tapizado
        )
        self.altura_regulable = altura_regulable
        self.tiene_ruedas = tiene_ruedas

    def calcular_precio(self) -> float:
        """
        Implementa el cálculo de precio específico para sillas.

        Returns:
            float: Precio final de la silla
        """
        # 1. Comenzar con el precio base
        base = self.precio_base
        # 2. Aplicar factor de comodidad heredado
        factor = self.calcular_factor_comodidad()
        # 3. Agregar costos por características especiales
        precio = base * factor
        if self.altura_regulable:
            precio += 10.0
        if self.tiene_ruedas:
            precio += 5.0
        # 4. Retornar precio redondeado a 2 decimales
        return round(precio, 2)

    def obtener_descripcion(self) -> str:
        """
        Implementa la descripción específica de la silla.

        Returns:
            str: Descripción completa de la silla
        """
        return (
            f"{self.nombre} de {self.material} en color {self.color}, "
            f"capacidad {self.capacidad_personas} personas, "
            f"respaldo {'Sí' if self.tiene_respaldo else 'No'}, "
            f"tapizado {self.material_tapizado or 'Ninguno'}, "
            f"altura regulable: {'Sí' if self.altura_regulable else 'No'}, "
            f"ruedas: {'Sí' if self.tiene_ruedas else 'No'}"
        )

    def regular_altura(self, nueva_altura: int) -> str:
        """
        Simula la regulación de altura de la silla.
        Método específico de la clase Silla.

        Args:
            nueva_altura: Nueva altura en centímetros

        Returns:
            str: Mensaje del resultado de la operación
        """
        if self.altura_regulable:
            return f"Altura regulada a {nueva_altura} cm"
        return "La silla no es regulable"

    def es_silla_oficina(self) -> bool:
        """
        Determina si la silla es adecuada para oficina.

        Returns:
            bool: True si es silla de oficina
        """
        return self.tiene_ruedas and self.altura_regulable
