"""
Servicio de catalogo que proporciona funcionalidades especializadas para
navegación y visualización del inventario de muebles.
"""

from typing import Dict, List, Optional, Tuple, Union

from models.composicion.comedor import Comedor
from models.mueble import Mueble
from services.tienda import TiendaMuebles


class Catalogo:
    """
    Clase que maneja las operaciones especializadas del catalogo de muebles.

    Esta clase se encarga de:
    - Navegación avanzada del catalogo
    - Visualización y presentación de productos
    - Operaciones de filtrado y ordenamiento especializadas
    - Generación de vistas previas y resúmenes

    Conceptos OOP aplicados:
    - Delegación: Utiliza una instancia de TiendaMuebles para operaciones core
    - Especialización: Extiende funcionalidades específicas de catalogo
    - Composición: Contiene una referencia al servicio de tienda
    """

    def __init__(self, tienda: TiendaMuebles):
        """
        Constructor del catalogo.

        Args:
            tienda: Instancia del servicio TiendaMuebles que contiene el inventario
        """
        self._tienda = tienda

    @property
    def tienda(self) -> TiendaMuebles:
        """Getter para la tienda asociada al catalogo."""
        return self._tienda

    def _obtener_material_color_comedor(self, comedor: Comedor) -> Tuple[str, str]:
        """
        Obtiene el material y color representativo de un comedor.
        Usa el material y color de la mesa como representativos.

        Args:
            comedor: Objeto Comedor

        Returns:
            Tupla (material, color)
        """
        if comedor.mesa:
            return comedor.mesa.material, comedor.mesa.color
        # Si no hay mesa, devolver valores por defecto
        return "desconocido", "desconocido"

    def obtener_vista_previa(self, limite: int = 5) -> List[Dict]:
        """
        Obtiene una vista previa de los productos más recientes o destacados.

        Args:
            limite: Número máximo de productos a incluir en la vista previa

        Returns:
            Lista de diccionarios con información resumida de los productos
        """
        muebles = self._tienda._inventario[-limite:] if self._tienda._inventario else []
        comedores = self._tienda._comedores[-limite:] if self._tienda._comedores else []

        vista_previa = []

        # Agregar muebles individuales
        for mueble in muebles:
            try:
                precio = mueble.calcular_precio()
                vista_previa.append(
                    {
                        "tipo": "mueble",
                        "nombre": mueble.nombre,
                        "material": mueble.material,
                        "color": mueble.color,
                        "precio": precio,
                        "descripcion_corta": mueble.obtener_descripcion()[:100] + "..."
                        if len(mueble.obtener_descripcion()) > 100
                        else mueble.obtener_descripcion(),
                    }
                )
            except Exception:
                continue

        # Agregar comedores
        for comedor in comedores:
            try:
                precio = comedor.calcular_precio_total()
                material, color = self._obtener_material_color_comedor(comedor)
                vista_previa.append(
                    {
                        "tipo": "comedor",
                        "nombre": comedor.nombre,
                        "material": material,
                        "color": color,
                        "precio": precio,
                        "descripcion_corta": f"Comedor {comedor.nombre} con {len(comedor._sillas)} sillas y 1 mesa",
                    }
                )
            except Exception:
                continue

        return vista_previa[:limite]

    def buscar_por_caracteristicas(self, **kwargs) -> List[Union[Mueble, Comedor]]:
        """
        Busca muebles por múltiples características simultáneamente.

        Args:
            **kwargs: Parámetros de búsqueda como nombre, material, color, precio_min, precio_max, etc.

        Returns:
            Lista de muebles y comedores que coinciden con todos los criterios
        """
        resultados = []

        # Filtrar muebles individuales
        muebles_filtrados = self._tienda._inventario.copy()

        # Aplicar filtros
        if "nombre" in kwargs and kwargs["nombre"]:
            nombre_filtro = kwargs["nombre"].lower()
            muebles_filtrados = [
                m for m in muebles_filtrados if nombre_filtro in m.nombre.lower()
            ]

        if "material" in kwargs and kwargs["material"]:
            material_filtro = kwargs["material"].lower()
            muebles_filtrados = [
                m for m in muebles_filtrados if m.material.lower() == material_filtro
            ]

        if "color" in kwargs and kwargs["color"]:
            color_filtro = kwargs["color"].lower()
            muebles_filtrados = [
                m for m in muebles_filtrados if m.color.lower() == color_filtro
            ]

        # Filtro de precio
        precio_min = kwargs.get("precio_min", 0)
        precio_max = kwargs.get("precio_max", float("inf"))
        if precio_min > 0 or precio_max != float("inf"):
            muebles_filtrados_temp = []
            for mueble in muebles_filtrados:
                try:
                    precio = mueble.calcular_precio()
                    if precio_min <= precio <= precio_max:
                        muebles_filtrados_temp.append(mueble)
                except Exception:
                    continue
            muebles_filtrados = muebles_filtrados_temp

        resultados.extend(muebles_filtrados)

        # Filtrar comedores (búsqueda más básica por nombre)
        if "nombre" in kwargs and kwargs["nombre"]:
            nombre_filtro = kwargs["nombre"].lower()
            comedores_filtrados = [
                c for c in self._tienda._comedores if nombre_filtro in c.nombre.lower()
            ]
            resultados.extend(comedores_filtrados)

        # Filtrar comedores por material y color (usando el de la mesa)
        if "material" in kwargs and kwargs["material"]:
            material_filtro = kwargs["material"].lower()
            comedores_filtrados = []
            for comedor in self._tienda._comedores:
                try:
                    material_comedor, _ = self._obtener_material_color_comedor(comedor)
                    if material_comedor.lower() == material_filtro:
                        comedores_filtrados.append(comedor)
                except Exception:
                    continue
            # Si ya filtramos por nombre, intersecar los resultados
            if "nombre" in kwargs and kwargs["nombre"]:
                nombre_filtro = kwargs["nombre"].lower()
                resultados = [
                    r
                    for r in resultados
                    if (hasattr(r, "nombre") and nombre_filtro in r.nombre.lower())
                    or (isinstance(r, Comedor) and r in comedores_filtrados)
                ]
            else:
                resultados.extend(comedores_filtrados)

        if "color" in kwargs and kwargs["color"]:
            color_filtro = kwargs["color"].lower()
            comedores_filtrados = []
            for comedor in self._tienda._comedores:
                try:
                    _, color_comedor = self._obtener_material_color_comedor(comedor)
                    if color_comedor.lower() == color_filtro:
                        comedores_filtrados.append(comedor)
                except Exception:
                    continue
            # Si ya filtramos por nombre o material, intersecar los resultados
            if (
                "nombre" in kwargs
                and kwargs["nombre"]
                or "material" in kwargs
                and kwargs["material"]
            ):
                resultados = [
                    r
                    for r in resultados
                    if (
                        (
                            hasattr(r, "nombre")
                            and (
                                "nombre" not in kwargs
                                or not kwargs["nombre"]
                                or kwargs["nombre"].lower() in r.nombre.lower()
                            )
                        )
                        and (
                            (
                                "material" not in kwargs
                                or not kwargs["material"]
                                or self._obtener_material_color_comedor(r)[0].lower()
                                == kwargs["material"].lower()
                            )
                            if isinstance(r, Comedor)
                            else True
                        )
                    )
                    or (isinstance(r, Comedor) and r in comedores_filtrados)
                ]
            else:
                resultados.extend(comedores_filtrados)

        return resultados

    def ordenar_por(
        self, criterio: str = "nombre", orden_ascendente: bool = True
    ) -> List[Union[Mueble, Comedor]]:
        """
        Obtiene todos los productos ordenados según un criterio específico.

        Args:
            criterio: Campo por el cual ordenar (nombre, precio, material, etc.)
            orden_ascendente: True para orden ascendente, False para descendente

        Returns:
            Lista de productos ordenados
        """
        todos_productos = []

        # Agregar muebles individuales con sus precios calculados
        for mueble in self._tienda._inventario:
            try:
                precio = mueble.calcular_precio()
                todos_productos.append(
                    {
                        "objeto": mueble,
                        "tipo": "mueble",
                        "nombre": mueble.nombre,
                        "precio": precio,
                        "material": mueble.material,
                        "color": mueble.color,
                    }
                )
            except Exception:
                continue

        # Agregar comedores con sus precios calculados
        for comedor in self._tienda._comedores:
            try:
                precio = comedor.calcular_precio_total()
                material, color = self._obtener_material_color_comedor(comedor)
                todos_productos.append(
                    {
                        "objeto": comedor,
                        "tipo": "comedor",
                        "nombre": comedor.nombre,
                        "precio": precio,
                        "material": material,
                        "color": color,
                    }
                )
            except Exception:
                continue

        # Definir función de clave para ordenamiento
        def obtener_clave(item):
            if criterio == "nombre":
                return item["nombre"].lower()
            elif criterio == "precio":
                return item["precio"]
            elif criterio == "material":
                return item["material"].lower()
            elif criterio == "color":
                return item["color"].lower()
            else:
                return item["nombre"].lower()  # default

        # Ordenar
        productos_ordenados = sorted(
            todos_productos, key=obtener_clave, reverse=not orden_ascendente
        )

        # Retornar solo los objetos
        return [item["objeto"] for item in productos_ordenados]

    def obtener_estadisticas_catalogo(self) -> Dict:
        """
        Obtiene estadísticas específicas del catalogo para presentación.

        Returns:
            Diccionario con estadísticas del catalogo
        """
        stats_tienda = self._tienda.obtener_estadisticas()

        # Estadísticas adicionales del catalogo
        estadisticas = {
            "total_productos": stats_tienda["total_muebles"]
            + stats_tienda["total_comedores"],
            "valor_catalogo": stats_tienda["valor_inventario"],
            "productos_por_tipo": stats_tienda["tipos_muebles"],
            "precio_promedio": 0,
            "producto_mas_caro": None,
            "producto_mas_barato": None,
        }

        # Calcular precio promedio, más caro y más barato
        precios = []
        productos_con_precio = []

        for mueble in self._tienda._inventario:
            try:
                precio = mueble.calcular_precio()
                precios.append(precio)
                productos_con_precio.append((mueble.nombre, precio, "mueble"))
            except Exception:
                continue

        for comedor in self._tienda._comedores:
            try:
                precio = comedor.calcular_precio_total()
                precios.append(precio)
                productos_con_precio.append((comedor.nombre, precio, "comedor"))
            except Exception:
                continue

        if precios:
            estadisticas["precio_promedio"] = round(sum(precios) / len(precios), 2)
            producto_caro_idx = precios.index(max(precios))
            producto_barato_idx = precios.index(min(precios))
            estadisticas["producto_mas_caro"] = {
                "nombre": productos_con_precio[producto_caro_idx][0],
                "precio": productos_con_precio[producto_caro_idx][1],
                "tipo": productos_con_precio[producto_caro_idx][2],
            }
            estadisticas["producto_mas_barato"] = {
                "nombre": productos_con_precio[producto_barato_idx][0],
                "precio": productos_con_precio[producto_barato_idx][1],
                "tipo": productos_con_precio[producto_barato_idx][2],
            }

        return estadisticas

    def generar_lista_para_mostrar(
        self, productos: List[Union[Mueble, Comedor]]
    ) -> List[Dict]:
        """
        Convierte una lista de productos en un formato adecuado para mostrar en UI.

        Args:
            productos: Lista de objetos Mueble o Comedor

        Returns:
            Lista de diccionarios con formato listo para mostrar
        """
        lista_formateada = []

        for producto in productos:
            if isinstance(producto, Mueble) and not isinstance(producto, Comedor):
                # Es un mueble individual
                try:
                    precio = producto.calcular_precio()
                    lista_formateada.append(
                        {
                            "tipo": "mueble",
                            "nombre": producto.nombre,
                            "descripcion": producto.obtener_descripcion(),
                            "precio": f"${precio:.2f}",
                            "material": producto.material,
                            "color": producto.color,
                            "detalles": f"{producto.nombre} - {producto.material} - {producto.color}",
                        }
                    )
                except Exception:
                    continue
            elif isinstance(producto, Comedor):
                # Es un comedor
                try:
                    precio = producto.calcular_precio_total()
                    material, color = self._obtener_material_color_comedor(producto)
                    lista_formateada.append(
                        {
                            "tipo": "comedor",
                            "nombre": producto.nombre,
                            "descripcion": f"Comedor {producto.nombre} con {len(producto._sillas)} sillas y 1 mesa",
                            "precio": f"${precio:.2f}",
                            "material": material,
                            "color": color,
                            "detalles": f"Comedor {producto.nombre} - {len(producto._sillas)} lugares",
                        }
                    )
                except Exception:
                    continue

        return lista_formateada
