# LPA1 Taller 1: Tienda de Muebles

Este taller está diseñado para introducir a los estudiantes en los conceptos de la Programación Orientada a Objetos (OOP) utilizando Python. Construiremos una tienda de muebles que implementa una jerarquía de clases aplicando los conceptos vistos en clase.

## Estudiante

Cuenta: https://github.com/andres0772?tab=repositories

## Objetivos

- Implementar **abstracción** mediante clases abstractas
- Diseñar jerarquías de clases usando **herencia**
- Aplicar **composición** para crear objetos complejos
- Utilizar **herencia múltiple** correctamente
- Implementar **polimorfismo** para comportamientos dinámicos
- Crear **métodos abstractos** y concretos
- Utilizar [**getters**](https://realpython.com/python-property/#getting-started-with-pythons-property) y [**setters**](https://realpython.com/python-getter-setter/#using-properties-instead-of-getters-and-setters-the-python-way) para encapsulación
- Escribir **pruebas unitarias** con [pytest](https://docs.pytest.org/en/stable/) para validar el código
- Crear interfaces de usuario con [**Rich**](https://rich.readthedocs.io/en/stable/introduction.html)

## Conceptos

### 1. Abstracción
- Ocultamos la complejidad interna y mostramos solo las funcionalidades esenciales
- Implementada mediante clases abstractas como `Mueble`, `Asiento`, etc.

### 2. Encapsulación
- Protegemos los datos internos usando atributos privados y métodos getter/setter
- Ejemplo: `_precio`, `_material` con sus respectivos métodos de acceso

### 3. Herencia
- Las clases hijas heredan propiedades y métodos de las clases padre
- Ejemplo: `Silla` hereda de `Asiento` que hereda de `Mueble`

### 4. Polimorfismo
- Diferentes objetos responden al mismo método de manera específica
- Ejemplo: cada mueble implementa `calcular_precio()` de forma diferente

### 5. Composición
- Un objeto contiene otros objetos como partes
- Ejemplo: `Comedor` contiene una `Mesa` y varias `Silla`s

### 6. Herencia Múltiple
- Una clase hereda de múltiples clases padre
- Ejemplo: `SofaCama` hereda de `Sofa` y `Cama`


## Instrucciones

### 0. Preparación

* Clonar el proyecto

    ```bash
    git clone https://github.com/andres0772/lpa1-taller-poo.git
    cd lpa1-taller-poo
    ```

* Crear y activar un entorno virtual

    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/WSL/Macos
    ```

* Instalar las dependencias

    ```bash
    pip install -r requirements.txt
    ```

### 1. Implementar la Clase Base Abstracta

**Archivo**: `models/mueble.py`

1. Importa `ABC` y `abstractmethod` de `abc`
2. Define la clase `Mueble` heredando de `ABC`
3. Implementa el constructor con atributos básicos
4. Crea propiedades con getters y setters
5. Define métodos abstractos `calcular_precio()` y `obtener_descripcion()`

**Conceptos**: Abstracción, encapsulación, métodos abstractos

### 2. Crear Clases Categorícas

**Archivos**: `models/categorias/asientos.py`, `almacenamiento.py`, `superficies.py`

1. Define clases abstractas que heredan de `Mueble`
2. Añade atributos específicos de cada categoría
3. Implementa métodos comunes a la categoría
4. Mantén algunos métodos abstractos para las clases concretas

**Conceptos**: Herencia, abstracción de categorías

### 3. Implementar Clases Concretas

**Archivos**: Todos los archivos en `models/concretos/`

1. Hereda de la clase de categoría correspondiente
2. Implementa todos los métodos abstractos
3. Añade atributos específicos del mueble
4. Implementa la lógica de cálculo de precio específica

**Conceptos**: Herencia, polimorfismo, implementación concreta

### 4. Herencia Múltiple

**Archivo**: `models/concretos/sofacama.py`

1. Implementa `SofaCama` heredando de `Sofa` y `Cama`
2. Resuelve conflictos de métodos usando `super()`
3. Implementa funcionalidades únicas de la combinación

**Conceptos**: Herencia múltiple, resolución de MRO

### 5. Composición

**Archivo**: `models/composicion/comedor.py`

1. Crea la clase `Comedor` que contiene una `Mesa` y múltiples `Silla`s
2. Implementa métodos para agregar/quitar sillas
3. Calcula el precio total sumando todos los componentes

**Conceptos**: Composición, agregación

### 6. Lógica de Negocio

**Archivos**: `services/tienda.py`, `services/catalogo.py`

1. Implementa la gestión del inventario
2. Crea métodos para buscar y filtrar muebles
3. Implementa funcionalidades de venta

**Conceptos**: Separación de responsabilidades, arquitectura en capas

### 7. Interfaz de Usuario

**Archivo**: `ui/menu.py`

1. Usa [Rich](https://rich.readthedocs.io/en/stable/introduction.html) para crear una interfaz atractiva
2. Implementa un menú interactivo
3. Muestra información de muebles de forma clara

**Conceptos**: Separación de interfaz y lógica

### 8. Pruebas Unitarias

**Archivos**: Todos los archivos en `tests/`

1. Crea tests para cada clase y método
2. Verifica el comportamiento de herencia y polimorfismo
3. Prueba casos edge y validaciones

**Conceptos**: Testing, calidad de código

## Ejecutar las Pruebas

- Ejecutar todas las pruebas

    ```bash
    python3 -m pytest -v
    ```

- Ejecutar pruebas con medición de cobertura (coverage)

    ```bash
    python3 -m pytest --cov=models --cov=services
    ```

## Ejecutar la Aplicación

```bash
python3 main.py
```

## Entregables

El estudiante debe actualizar su repositio personal con:

* Código fuente completo con todos los TODOs resueltos
* Pruebas unitarias funcionando al 100%
* Aplicación ejecutable con interfaz funcional
* Documentación adicional si es necesaria

## Buenas Prácticas y Workflow Moderno

* Comienza por lo simple, implementa primero las clases básicas antes que las complejas
* Consulta la documentación y revisa los conceptos de OOP cuando tengas dudas
* Fomentar el uso de nombres descriptivos, comentarios claros y una estructura de código coherente.
* Enfatizar la importancia de las pruebas unitarias para garantizar la calidad del código.
* Utilizar Git para gestionar los cambios y realizar commits atómicos.
* Mantener el `README.md` actualizado y documentar el código cuando sea necesario.
