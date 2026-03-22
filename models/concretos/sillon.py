"""
Clase concreta Sillón.
Implementa un mueble de asiento específico para una persona con características de sillón.
"""

from ..categorias.asientos import Asiento


class Sillon(Asiento):
    """
    Clase concreta que representa un sillón.

    Un sillón es un asiento individual con características específicas
    como reposapiés, material del cojín y mecanismo giratorio.

    Conceptos OOP aplicados:
    - Herencia: Hereda de Asiento
    - Polimorfismo: Implementa métodos abstractos de manera específica
    - Encapsulamiento: Protege atributos específicos del sillón
    """

    def __init__(
        self,
        nombre: str,
        material: str,
        color: str,
        precio_base: float,
        tiene_respaldo: bool,
        material_tapizado: str,
        tiene_reposapiés: bool = False,
        material_cojin: str = "algodón",
        giratorio: bool = False,
    ):
        """
        Constructor del sillón.

        Args:
            tiene_reposapiés: Si el sillón tiene reposapiés
            material_cojin: Material del cojín del sillón
            giratorio: Si el sillón es giratorio
            Otros argumentos heredados de Asiento
        """
        # Un sillón típico tiene capacidad para 1 persona
        super().__init__(
            nombre, material, color, precio_base, 1, tiene_respaldo, material_tapizado
        )

        # Inicializar atributos específicos usando setters para validación
        self.tiene_reposapiés = tiene_reposapiés
        self.material_cojin = material_cojin
        self.giratorio = giratorio

    # Getter y setter para tiene_reposapiés
    @property
    def tiene_reposapiés(self) -> bool:
        """Getter para tiene reposapiés."""
        return self._tiene_reposapiés

    @tiene_reposapiés.setter
    def tiene_reposapiés(self, value: bool) -> None:
        """Setter para tiene reposapiés con validación."""
        if not isinstance(value, bool):
            raise TypeError("tiene_reposapiés debe ser un valor booleano")
        self._tiene_reposapiés = value

    # Getter y setter para material_cojin
    @property
    def material_cojin(self) -> str:
        """Getter para material del cojín."""
        return self._material_cojin

    @material_cojin.setter
    def material_cojin(self, value: str) -> None:
        """Setter para material del cojín con validación."""
        if not isinstance(value, str):
            raise TypeError("material_cojin debe ser una cadena de texto")
        if not value.strip():
            raise ValueError("material_cojin no puede estar vacío")
        self._material_cojin = value.strip()

    # Getter y setter para giratorio
    @property
    def giratorio(self) -> bool:
        """Getter para giratorio."""
        return self._giratorio

    @giratorio.setter
    def giratorio(self, value: bool) -> None:
        """Setter para giratorio con validación."""
        if not isinstance(value, bool):
            raise TypeError("giratorio debe ser un valor booleano")
        self._giratorio = value

    def calcular_precio(self) -> float:
        """
        Implementa el cálculo de precio específico para sillones.

        Returns:
            float: Precio final del sillón
        """
        # Comenzar con el precio base
        precio = self._precio_base

        # Aplicar factor de comodidad heredado
        factor = self.calcular_factor_comodidad()
        precio *= factor

        # Agregar costos por características específicas del sillón
        if self._tiene_reposapiés:
            precio += 25.0  # $25 adicional por reposapiés
        if self._giratorio:
            precio += 20.0  # $20 adicional por mecanismo giratorio
        # Costo adicional según material del cojín
        if self._material_cojin.lower() == "cuero":
            precio += 30.0  # $30 adicional por cojin de cuero
        elif self._material_cojin.lower() == "lana":
            precio += 15.0  # $15 adicional por cojin de lana
        elif self._material_cojin.lower() == "terciopelo":
            precio += 20.0  # $20 adicional por cojin de terciopelo

        # Retornar precio redondeado a 2 decimales
        return round(precio, 2)

    def obtener_descripcion(self) -> str:
        """
        Implementa la descripción específica del sillón.

        Returns:
            str: Descripción completa del sillón
        """
        base_desc = super().obtener_descripcion()
        return (
            f"{base_desc}, "
            f"Tiene reposapiés: {'Sí' if self._tiene_reposapiés else 'No'}, "
            f"Material del cojín: {self._material_cojin}, "
            f"Giratorio: {'Sí' if self._giratorio else 'No'}"
        )
