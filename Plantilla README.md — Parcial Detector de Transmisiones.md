# Parcial — Detector de Transacciones Sospechosas

Nombre:  SEBASTIAN W
Código:  PYTHON Y JSON
Grupo:  4E

## 1. ¿Qué debe hacer el programa?

Escriba en máximo 3 o 4 líneas cuál es el objetivo del programa.

Respuesta:
programa en Python que permita registrar transacciones y analizar automáticamente el nivel de riesgo de cada operación.

El sistema no utilizará bases de datos. La información deberá mantenerse en memoria durante la ejecución y almacenarse en un archivo JSON.
---

## 2. Clase `Transmision`

La clase tendrá los siguientes atributos:

- `id`:
- `origen`:
- `mensaje`:
- `puntaje`:
- `clasificacion`:

Escriba brevemente qué representa cada uno.
ID = una identificación unica que tendra el usuario
origen = de donde proviene el usuario
Mensaje = Una señal que se le transmitira a la consola
Puntaje = El medidor donde se llevara a cabo la clasificación 
Clasificación = Asignarle un rango dependiendo de su medida
---

## 3. Métodos

### `analizar()`

Responsabilidad: Calcula y retorna el puntaje de riesgo de la transacción.

### `clasificar()`

Responsabilidad: Retorna la clasificación correspondiente según el puntaje de riesgo.

### `to_dict()`

Responsabilidad: Convierte el objeto Transaccion en un diccionario que pueda guardarse en JSON.

### `from_dict()`

Responsabilidad: Debe implementarse como método de clase:

@classmethod
def from_dict(cls, datos):
Recibe un diccionario leído desde JSON y retorna un objeto Transaccion.

---

## 4. Algoritmo de análisis

Complete el siguiente pseudocódigo:

```text
puntaje = 0

SI el mensaje contiene (valor >= $2000000) 
    sumar +30 puntos

SI el mensaje contiene (Hora > 5 y Hora <)
    sumar +20 puntos

SI el mensaje contiene (Pais != Colombia)
    sumar +25 puntos

SI el mensaje contiene (Dispositivo_Conocido == false)
    sumar +30 puntos


```

---

## 5. Persistencia

Explique brevemente qué ocurre al iniciar el programa:
Al iniciar el programa, se lee el archivo JSON, se deserializa y la información se convierte nuevamente en objetos para poder trabajar con ellos dentro del programa.
```text
JSON
 ↓
____________________
 ↓
____________________
```

Explique qué ocurre al guardar:

```text
Objetos
 ↓
##Los objetos del programa se convierten (serializan) en formato JSON para poder almacenarlos en un archivo. Cuando se ##necesiten nuevamente, el JSON puede convertirse otra vez en objetos mediante deserialización.
 ↓
JSON
```

---

## 6. Menú

Indique qué debe hacer cada opción:

### Opción 1 — Registrar transacción

1.  Pedir los datos de la transmisión al usuario
2.  Crear un objeto con esos datos.
3.  Guardar el objeto en el archivo JSON.

### Opción 2 — Listar transmisiones

1.  Leer y deserializar las transmisiones almacenadas en el archivo JSON.
2.  Mostrar las transmisiones registradas en pantalla.

### Opción 3 — Salir

Acción:
Terminar la ejecución del programa.
---

## Nota

Este archivo debe completarse durante los primeros 15 minutos del parcial, antes de comenzar la implementación.