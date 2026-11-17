# Sistema de Inventario de Zapatos — SQLAlchemy ORM

## 1. Información del proyecto

| Información | Descripción |
|---|---|
| Estudiante | [Sebastian Wehdeking Navarro] |
| Asignatura | [DESARROLLO DE APLICACIONES WEB CON ACCESO A DATOS] |
| Docente | [EDUARDO PIMIENTA] |
| Fecha | [17 / 11 / 2026] |
| Lenguaje de programación | Python |
| ORM utilizado | SQLAlchemy |
| Base de datos | SQLite |

## 2. Descripción del proyecto

**¿En qué consiste el programa?**

[Una pequeña tienda de zapatos cuenta con un programa en Python que permite administrar su inventario desde la consola.]

**¿Qué funcionalidades tiene?**

Describe brevemente las operaciones que permite realizar el sistema:

- Registrar zapatos.
- Consultar el inventario.
- Buscar zapatos por ID.
- Actualizar precios.
- Eliminar zapatos.

## 3. Estructura del proyecto

Presenta la estructura de archivos de tu aplicación.

```text
tienda_zapatos/
├── main.py
├── datos.py
├── requirements.txt
├── README.md
└── evidencias/
```

**Explicación de los archivos:**

| Archivo | ¿Cuál es su responsabilidad? |
|---|---|
| `main.py` | [Interaccion con el usuario (Capa de presentación)] |
| `datos.py` | [Es donde va la logica del negocio] |
| `requirements.txt` | [Donde esta la sintaxis de descarga de SQLAlchemy], es obligatorio descargarlo en la terminal para usar sus librerias |
| `zapateria.db` | [Es la base de datos importante dentro del neogcio, donde puede el dueño, consultar, mostrar, modificiar y eliminar los productos] |

## 4. Instalación y ejecución

Explica los pasos para ejecutar el proyecto en otro computador.

**Paso 1. Requisitos**

[Tener los archivos necesarios y la logica de codigo bien construida, tener las extensiones y librerias descargadas.]

**Paso 2. Instalación de dependencias**

```bash
python -m pip install -r requirements.txt
[Es la sintaxis principal para descargar las librerias de SQLAlchemy para utilizarlo, se escribe esa sintaxis a traves de la terminal de VS CODE]
```

**Paso 3. Ejecución**

```bash
python main.py
[aparecera el menu(La capa de presentación que interactuara con el usuario, le muestra unas opciones).]
```

**Paso 4. Resultado esperado**

[Al ejecutar el la sintaxis de codigo correctamente aparecera el menu(La capa de presentación que interactuara con el usuario, le muestra unas opciones).]

---

# 5. Documentación técnica — Preguntas obligatorias

Responde las siguientes preguntas utilizando tu implementación. Cuando sea necesario, incluye fragmentos de tu código para explicar el funcionamiento.

### Pregunta 1. Modelo y tabla

¿Qué clase de Python representa la tabla de la base de datos? Explica cómo SQLAlchemy identifica el nombre de la tabla y sus columnas.

**Respuesta:**

[La clase de Python que representa la tabla es Zapato, la cual hereda de Base (que a su vez hereda de DeclarativeBase).]

**Fragmento de código relacionado:**

[class Zapato(BASE):
    __tablename__ = "zapatos".]

### Pregunta 2. Creación de la base de datos

¿Qué ocurre cuando ejecutas el programa por primera vez? Explica cómo se crea la base de datos `zapateria.db` y la tabla `zapatos`.

**Respuesta:**

[Al ejecutar el programa por primera vez, main.py llama a la función inicializar_bd() definida en datos.py. Dentro de esta función se ejecuta la instrucción Base.metadata.create_all(engine).
Al intentar establecer la conexión definida en engine = create_engine("sqlite:///zapateria.db"), el motor de SQLite detecta que el archivo zapateria.db no existe en la carpeta del proyecto y lo crea automáticamente en el disco.
]

**Fragmento de código relacionado:**

[
from sqlalchemy import create_engine
engine = create_engine("sqlite:///zapateria.db", echo = False)
.]

### Pregunta 3. Registro de zapatos

Cuando seleccionas la opción de registrar un zapato, ¿qué recorrido siguen los datos desde el menú hasta quedar almacenados en SQLite? Identifica las funciones utilizadas.

**Respuesta:**

El flujo de datos sigue esta secuencia:

- En main.py, el menú solicita al usuario ingresar por consola los valores de modelo, talla y precio.
- main.py invoca la función crear_zapato(modelo, talla, precio) de datos.py enviando esos datos como argumentos.
- Dentro de crear_zapato(), se instancia un objeto en memoria de la clase modelo: nuevo_zapato = Zapato(modelo=modelo, talla=talla, precio=precio).
- Se abre una sesión con with Session(engine) as session:, se añade la instancia al área de trabajo de la sesión mediante session.add(nuevo_zapato) y finalmente session.commit() traduce el objeto a una sentencia INSERT INTO zapatos que guarda el registro permanentemente en zapateria.db, asignándole automáticamente su id

**Fragmento de código relacionado:**

def crear_zapato(modelo, talla, precio):
    with Session(engine) as session:
        nuevo_Zapato = Zapato(modelo = modelo, talla = talla, precio = precio)
        session.add(nuevo_Zapato)
        session.commit()
        return True


### Pregunta 4. Sesiones y transacciones

¿Para qué se utiliza una sesión de SQLAlchemy? ¿Qué ocurriría si agregas o modificas un objeto, pero no confirmas la transacción con `commit()`?

**Respuesta:**

Una sesión (Session(engine)) actúa como una zona de intercambio o unidad de trabajo entre los objetos Python en memoria y la base de datos relacional. Gestiona la conexión, rastrea los cambios realizados sobre los objetos cargados o creados y agrupa las operaciones en transacciones.

Si agregas o modificas un objeto con session.add() o alterando sus atributos, pero no ejecutas session.commit(), los cambios quedan únicamente en la memoria temporal de la transacción actual. Al cerrarse el bloque with Session(engine) as session:, SQLAlchemy descarta la transacción pendiente (ejecuta un rollback implícito) y los datos nunca se escriben en el archivo zapateria.db


### Pregunta 5. Búsqueda por ID

¿Cómo funciona la búsqueda de zapatos por ID? Explica qué devuelve tu función cuando encuentra el registro y qué devuelve cuando no existe.

**Respuesta:**

La función buscar_zapato(id_zapato) abre una sesión y utiliza el método session.get(Zapato, id_zapato). Este método consulta directamente por la clave primaria (id) de la tabla zapatos.

**Fragmento de código relacionado:**

[Agrega el código de búsqueda y explícalo.]

def buscar_zapato(id_zapato):

    with Session(engine) as session:
        return session.get(Zapato, id_zapato)

- Cuando encuentra el registro: SQLAlchemy reconstruye los datos de la fila encontrada y la función devuelve una instancia del objeto Zapato con todos sus atributos (id, modelo, talla, precio)

- Cuando no existe: session.get() no encuentra coincidencia y la función retorna None, lo que permite que main.py muestre un mensaje indicando que el zapato no fue encontrado sin que el programa se detenga por un error.

### Pregunta 6. Actualización de precios

¿Cómo se actualiza el precio de un zapato mediante el ORM? Explica cómo se obtiene el objeto, cómo se modifica su atributo y cómo se guarda el cambio.

**Respuesta:**

Cuando no existe: session.get() no encuentra coincidencia y la función retorna None, lo que permite que main.py muestre un mensaje indicando que el zapato no fue encontrado sin que el programa se detenga por un error.

**Fragmento de código relacionado:**

def actualizar_precio(id_zapato, nuevo_precio):

    with Session(engine) as session:
        zapato = session.get(Zapato, id_zapato)
        if zapato is not None:
            zapato.precio = nuevo_precio
            session.commit()

            return True

- Obtención del objeto: Se busca el registro existente mediante zapato = session.get(Zapato, id_zapato).

- Modificación del atributo: Si zapato is not None, se reasigna directamente su propiedad en Python mediante zapato.precio = nuevo_precio. Al estar el objeto vinculado a la sesión activa, SQLAlchemy detecta automáticamente que el atributo fue modificado (dirty state).

- Guardado del cambio: Se ejecuta session.commit(), lo cual genera una sentencia UPDATE zapatos SET precio = ... WHERE id = ... en SQLite y retorna True (si el ID no existía, retorna False sin alterar la base de datos).

### Pregunta 7. Eliminación de registros

¿Qué ocurre cuando eliminas un zapato? Explica cómo compruebas que el registro ya no existe en la base de datos.

**Respuesta:**

En eliminar_zapato(id_zapato), primero se recupera el objeto con zapato = session.get(Zapato, id_zapato). Si existe, se marca para borrado con session.delete(zapato) y se ejecuta session.commit(), lo que dispara una sentencia DELETE FROM zapatos WHERE id = ... en SQLite y retorna True

**Fragmento de código relacionado:**

def eliminar_zapato(id_zapato):
    
    with Session(engine) as session:
        zapato = session.get(Zapato, id_zapato)
        if zapato is not None:
            session.delete(zapato)
            session.commit()

            return True

- Comprobación: Se verifica de dos formas en la aplicación: ejecutando la opción de listar todos los zapatos (listar_zapatos()), donde el registro ya no aparece en el inventario, o intentando consultarlo nuevamente por su ID mediante buscar_zapato(id_zapato) (o intentando actualizarlo/eliminarlo otra vez), comprobando que devuelve None o False respectivamente.

### Pregunta 8. Persistencia de datos

¿Qué sucede con los zapatos registrados cuando cierras y vuelves a ejecutar el programa? Explica por qué permanecen almacenados.

**Respuesta:**

Cuando se cierra el programa y lo vuelves a ejecutar, los zapatos registrados previamente (que no hayan sido eliminados) siguen intactos y disponibles al consultar el listado (listar_zapatos()) o buscarlos por ID (buscar_zapato())

---

## 6. Pruebas de funcionamiento y evidencias

Debes ejecutar el programa y demostrar el funcionamiento de cada una de las operaciones.

### Prueba 1. Registrar zapatos

- **Acción realizada:** registrar dos zapatos.
- **Datos utilizados:** [Indicar modelo, talla y precio].
- **Resultado obtenido:** [Se registran las caracteristicas del modelo del zapato y se guarda automaticamente dentro de la base de datos].

**Evidencia:**

![Registro de zapatos](evidencias/registro.png)

### Prueba 2. Listar inventario

- **Acción realizada:** consultar todos los zapatos.
- **Resultado obtenido:** [muestra en la consola la lista de todos los zapatos junto con su información guardada en la base de datos].

**Evidencia:**

![Listado de zapatos](evidencias/listado.png)

### Prueba 3. Buscar por ID

- **ID utilizado:** [Indicar ID].
- **Resultado obtenido:** [El programa busca el par de zapatos correspondiente con su numero unico de ID].

**Evidencia:**

![Búsqueda de zapatos](evidencias/busqueda.png)

### Prueba 4. Actualizar precio

- **Zapato seleccionado:** [2].
- **Precio anterior:** [35.99].
- **Precio nuevo:** [40.99].
- **Resultado obtenido:** [Se modificó el precio del par de zapatos].

**Evidencia:**

![Actualización de precio](evidencias/actualizacion.png)

### Prueba 5. Eliminar zapato

- **ID eliminado:** [3].
- **Resultado obtenido:** [Cuando el mensaje muestre que se eliminó correctamnete el ID del zapato seleccionado, haz la consulta de la lista y si recuerdas el ID del par de zapato eliminado
ya no aparecera en la lista porque ya le ordenaste al programa que lo eliminaste ].

**Evidencia:**

![Eliminación de zapato](evidencias/eliminacion.png)

### Prueba 6. Comprobar persistencia

- **Acción realizada:** cerrar y ejecutar nuevamente el programa.
- **Resultado obtenido:** [dependiendo si ya guardaste zapatos anteriormente, al cerrar el editor de texto junto con el programa en funcionamento la información guardada en la base de datos
no se pierde y queda intacta en la base de datos ].

**Evidencia:**

![Persistencia de datos](evidencias/persistencia.png)

### Pruebas con registros inexistentes

Ejecuta las operaciones de buscar, actualizar y eliminar utilizando un ID que no exista.

| Operación | ¿Qué sucedió? |
|-|---|
| Buscar ID inexistente | [Zapato No encontrado] |
| Actualizar ID inexistente | [ID no existente] |
| Eliminar ID inexistente | [ID no existente] |

## 7. Conclusiones

Responde brevemente:

1. ¿Qué aprendiste al implementar las operaciones CRUD utilizando SQLAlchemy?
2. ¿Qué diferencia identificaste entre trabajar con objetos Python y escribir sentencias SQL directamente?
3. ¿Cuál fue la principal dificultad durante el desarrollo y cómo la solucionaste?


## Indicaciones de documentación

- Responde las ocho preguntas con tus propias palabras.
- Relaciona tus explicaciones con el código que implementaste.
- Incluye fragmentos de código únicamente cuando ayuden a explicar tu respuesta.
- Todas las evidencias deben corresponder a ejecuciones reales del programa.
- Guarda las capturas dentro de la carpeta `evidencias/` utilizando los nombres indicados o actualiza las rutas del README.
- Verifica que las imágenes se visualicen correctamente en GitHub.
- Elimina los textos entre corchetes y reemplázalos con tus respuestas antes de entregar.
- La documentación debe permitir que otra persona comprenda cómo instalar, ejecutar y utilizar tu aplicación.