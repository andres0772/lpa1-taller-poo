#!/usr/bin/env python3
"""
Final test for the Catalogo class following the same pattern as main.py
"""

from models.composicion.comedor import Comedor
from models.concretos.cama import Cama
from models.concretos.mesa import Mesa
from models.concretos.silla import Silla
from services.catalogo import Catalogo
from services.tienda import TiendaMuebles


def test_catalogo():
    print("Testing Catalogo class...")

    # Crear la tienda
    tienda = TiendaMuebles("Test Store")

    # Add some sample furniture
    silla = Silla("Test Chair", "wood", "black", 100.0, True, "fabric", True, False)
    mesa = Mesa(
        "Test Table",
        "wood",
        "brown",
        200.0,
        2.0,
        1.0,
        0.8,
        50.0,
        "wood",
        4,
        "rectangular",
    )
    cama = Cama(
        "Test Bed",
        "wood",
        "white",
        300.0,
        1.5,
        2.0,
        0.5,
        100.0,
        "wood",
        False,
        "individual",
        False,
        0.5,
        0,
    )

    # Create a comedor
    comedor_mesa = Mesa(
        "Dining Table",
        "wood",
        "brown",
        400.0,
        2.5,
        1.2,
        0.75,
        60.0,
        "wood",
        4,
        "rectangular",
        False,
    )
    comedor_silla1 = Silla(
        "Dining Chair 1", "wood", "brown", 150.0, True, "fabric", False, True
    )
    comedor_silla2 = Silla(
        "Dining Chair 2", "wood", "brown", 150.0, True, "fabric", False, True
    )
    comedor = Comedor("Test Dining Set", comedor_mesa, [comedor_silla1, comedor_silla2])

    # Add items to tienda
    tienda.agregar_mueble(silla)
    tienda.agregar_mueble(mesa)
    tienda.agregar_mueble(cama)
    tienda.agregar_comedor(comedor)

    # Create catalogo
    catalogo = Catalogo(tienda)

    # Test 1: Check that we can access the tienda
    assert catalogo.tienda == tienda
    print("✓ Catalogo correctly stores tienda reference")

    # Test 2: Vista previa
    vista = catalogo.obtener_vista_previa()
    assert len(vista) > 0
    print(f"✓ Vista previa returns {len(vista)} items")

    # Test 3: Búsqueda por material
    resultados = catalogo.buscar_por_caracteristicas(material="wood")
    assert len(resultados) >= 3  # At least the 3 individual items
    print(f"✓ Búsqueda por material 'wood' returns {len(resultados)} items")

    # Test 4: Ordenamiento por precio
    ordenados = catalogo.ordenar_por("precio", True)
    assert len(ordenados) == 4  # 3 individual items + 1 comedor
    print(f"✓ Ordenamiento por precio returns {len(ordenados)} items")

    # Test 5: Estadísticas
    stats = catalogo.obtener_estadisticas_catalogo()
    assert stats["total_productos"] == 4
    assert isinstance(stats["valor_catalogo"], (int, float))
    assert stats["valor_catalogo"] > 0
    print(
        f"✓ Estadísticas: {stats['total_productos']} productos, valor ${stats['valor_catalogo']:.2f}"
    )

    # Test 6: Generación de lista para mostrar
    lista = catalogo.generar_lista_para_mostrar(ordenados[:2])  # First 2 items
    assert len(lista) == 2
    assert all(item["tipo"] in ["mueble", "comedor"] for item in lista)
    print(f"✓ Generación de lista para mostrar works correctly")

    print("\n🎉 All tests passed!")
    return True


if __name__ == "__main__":
    try:
        success = test_catalogo()
        exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback

        traceback.print_exc()
        exit(1)
