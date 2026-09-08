import json
import os
import re


print("==============================")
print("|°°°BIENVENIDO AL PROGRAMA°°°|")
print("==============================")


# Se creara la Clase

class Transaccion:

    def __init__(self, id, titular, Valor, Hora, Pais, Dispositivo_Conocido):

        # ==============================
        # VALIDACIONES
        # ==============================

        # ID
        if not isinstance(id, int):
            raise ValueError("El ID debe ser un número entero.")

        if id <= 0:
            raise ValueError("El ID debe ser mayor que cero.")

        # TITULAR
        if not isinstance(titular, str):
            raise ValueError("El titular debe ser texto.")

        if titular.strip() == "":
            raise ValueError("El titular no puede estar vacío.")

        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]+", titular.strip()):
            raise ValueError(
                "El titular solo puede contener letras y espacios."
            )

        # VALOR
        if not isinstance(Valor, (int, float)) or isinstance(Valor, bool):
            raise ValueError("El valor debe ser numérico.")

        if Valor <= 0:
            raise ValueError("El valor debe ser mayor que cero.")

        # HORA
        if not isinstance(Hora, int) or isinstance(Hora, bool):
            raise ValueError("La hora debe ser un número entero.")

        if Hora < 0 or Hora > 23:
            raise ValueError("La hora debe estar entre 0 y 23.")

        # PAIS
        if not isinstance(Pais, str):
            raise ValueError("El país debe ser texto.")

        if Pais.strip() == "":
            raise ValueError("El país no puede estar vacío.")

        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]+", Pais.strip()):
            raise ValueError(
                "El país solo puede contener letras y espacios."
            )

        # DISPOSITIVO CONOCIDO
        if not isinstance(Dispositivo_Conocido, bool):
            raise ValueError(
                "Dispositivo_Conocido debe ser True o False."
            )

        # ==============================
        # ATRIBUTOS DEL OBJETO
        # ==============================

        self.id = id
        self.titular = titular.strip()
        self.Valor = Valor
        self.Hora = Hora
        self.Pais = Pais.strip()
        self.Dispositivo_Conocido = Dispositivo_Conocido

        # Se declaran los valores que serán calculados
        self.Puntaje_de_Riesgo = self.calcular_riesgo()
        self.Clasificación = self.clasificar()


    # ==========================================
    # METODO PARA CALCULAR EL RIESGO
    # ==========================================

    def calcular_riesgo(self):

        Puntaje = 0

        if self.Valor >= 2000000:
            Puntaje += 30

        if self.Hora > 0 and self.Hora < 5:
            Puntaje += 20

        if self.Pais.lower() != "colombia":
            Puntaje += 25

        if self.Dispositivo_Conocido == False:
            Puntaje += 30

        return Puntaje


    # ==========================================
    # METODO PARA CLASIFICAR
    # ==========================================

    def clasificar(self):

        if self.Puntaje_de_Riesgo <= 30:
            return "NORMAL"

        elif self.Puntaje_de_Riesgo <= 60:
            return "SOSPECHOSO"

        else:
            return "ALTO RIESGO"


    # ==========================================
    # METODO TO_DICT
    # ==========================================

    def to_dict(self):

        return {
            "id": self.id,
            "titular": self.titular,
            "Valor": self.Valor,
            "Hora": self.Hora,
            "Pais": self.Pais,
            "Dispositivo_Conocido": self.Dispositivo_Conocido,
            "Puntaje_de_Riesgo": self.Puntaje_de_Riesgo,
            "Clasificación": self.Clasificación
        }


    # ==========================================
    # METODO FROM_DICT
    # ==========================================

    @classmethod
    def from_dict(cls, datos):

        return cls(
            datos["id"],
            datos["titular"],
            datos["Valor"],
            datos["Hora"],
            datos["Pais"],
            datos["Dispositivo_Conocido"]
        )


# =========================================================
# FUNCION PARA LEER LAS TRANSACCIONES DESDE JSON
# =========================================================

def cargar_transacciones():

    transacciones = []

    if os.path.exists("transacciones.json"):

        try:

            with open("transacciones.json", "r", encoding="utf-8") as archivo:

                datos = json.load(archivo)

                if not isinstance(datos, list):
                    print("El archivo JSON no contiene una lista.")
                    return transacciones

                for dato in datos:

                    try:
                        transaccion = Transaccion.from_dict(dato)
                        transacciones.append(transaccion)

                    except (KeyError, ValueError, TypeError) as error:

                        print(
                            "Se encontró una transacción inválida en el JSON:",
                            error
                        )

        except json.JSONDecodeError:

            print("El archivo transacciones.json está dañado o tiene un formato incorrecto.")

        except OSError:

            print("No se pudo leer el archivo transacciones.json.")

    else:

        print("No existe transacciones.json.")
        print("Se comenzará con una lista vacía.")

    return transacciones


# =========================================================
# FUNCION PARA GUARDAR LAS TRANSACCIONES
# =========================================================

def guardar_transacciones(transacciones):

    datos = []

    for transaccion in transacciones:
        datos.append(transaccion.to_dict())

    try:

        with open("transacciones.json", "w", encoding="utf-8") as archivo:

            json.dump(
                datos,
                archivo,
                indent=4,
                ensure_ascii=False
            )

        print("\nLas transacciones fueron guardadas correctamente.")

    except OSError:

        print("No se pudo guardar el archivo transacciones.json.")


# =========================================================
# FUNCIONES PARA VALIDAR DATOS INGRESADOS
# =========================================================

def pedir_id():

    while True:

        entrada = input("Asigne su Id: ").strip()

        if entrada == "":
            print("ERROR: El ID no puede estar vacío.")
            continue

        if not entrada.isdigit():
            print("ERROR: El ID solo puede contener números.")
            continue

        id = int(entrada)

        if id <= 0:
            print("ERROR: El ID debe ser mayor que cero.")
            continue

        return id


def pedir_titular():

    while True:

        titular = input("Cual es su titular: ").strip()

        if titular == "":
            print("ERROR: El titular no puede estar vacío.")
            continue

        if not re.fullmatch(
            r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]+",
            titular
        ):
            print(
                "ERROR: El titular solo puede contener letras y espacios."
            )
            continue

        return titular


def pedir_valor():

    while True:

        entrada = input(
            "Indique el valor que va a depositar: "
        ).strip()

        if entrada == "":
            print("ERROR: El valor no puede estar vacío.")
            continue

        if not entrada.isdigit():
            print(
                "ERROR: El valor debe contener únicamente números."
            )
            continue

        Valor = int(entrada)

        if Valor <= 0:
            print(
                "ERROR: El valor debe ser mayor que cero."
            )
            continue

        return Valor


def pedir_hora():

    while True:

        entrada = input("Diga la hora: ").strip()

        if entrada == "":
            print("ERROR: La hora no puede estar vacía.")
            continue

        if not entrada.isdigit():
            print(
                "ERROR: La hora debe ser un número entero."
            )
            continue

        Hora = int(entrada)

        if Hora < 0 or Hora > 23:
            print(
                "ERROR: La hora debe estar entre 0 y 23."
            )
            continue

        return Hora


def pedir_pais():

    while True:

        Pais = input("De que pais es?: ").strip()

        if Pais == "":
            print("ERROR: El país no puede estar vacío.")
            continue

        if not re.fullmatch(
            r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]+",
            Pais
        ):
            print(
                "ERROR: El país solo puede contener letras y espacios."
            )
            continue

        return Pais


def pedir_dispositivo():

    while True:

        respuesta = input(
            "¿Tiene su dispositivo conocido? (S/N): "
        ).strip().upper()

        if respuesta == "":
            print("ERROR: No puede dejar este campo vacío.")
            continue

        if respuesta == "S":
            return True

        elif respuesta == "N":
            return False

        else:
            print(
                "ERROR: Solo puede escribir S o N."
            )


# =========================================================
# FUNCION PARA MOSTRAR UNA TRANSACCION
# =========================================================

def mostrar_transaccion(transaccion):

    print("======================================")
    print("|=======DATOS DE LA TRANSACCION=======|")
    print("======================================")

    print("Identificación del usuario:", transaccion.id)
    print("Su nombre es:", transaccion.titular)
    print("Valor depositado: $", transaccion.Valor)
    print("La hora en la que se deposito el dinero:", transaccion.Hora)
    print("Pais de origen del usuario:", transaccion.Pais)
    print(
        "Su dispositivo es conocido?",
        transaccion.Dispositivo_Conocido
    )
    print(
        "Puntaje de riesgo:",
        transaccion.Puntaje_de_Riesgo
    )
    print(
        "Clasificación:",
        transaccion.Clasificación
    )

    print("======================================")


# =========================================================
# CARGAR TRANSACCIONES EXISTENTES
# =========================================================

transacciones = cargar_transacciones()


# =========================================================
# CASOS DE PRUEBA OBLIGATORIOS
# =========================================================

caso1 = Transaccion(
    1,
    "Laura Gómez",
    3500000,
    2,
    "Colombia",
    False
)

caso2 = Transaccion(
    2,
    "Carlos Pérez",
    500000,
    14,
    "Colombia",
    True
)

caso3 = Transaccion(
    3,
    "Ana Torres",
    2500000,
    10,
    "Perú",
    True
)


# =========================================================
# AGREGAR LOS CASOS SI NO EXISTEN
# =========================================================

ids_existentes = []

for transaccion in transacciones:
    ids_existentes.append(transaccion.id)


if caso1.id not in ids_existentes:
    transacciones.append(caso1)


if caso2.id not in ids_existentes:
    transacciones.append(caso2)


if caso3.id not in ids_existentes:
    transacciones.append(caso3)


# =========================================================
# MOSTRAR CASOS DE PRUEBA
# =========================================================

print("\n")
print("======================================")
print("|=======CASOS DE PRUEBA=======|")
print("======================================")


mostrar_transaccion(caso1)
mostrar_transaccion(caso2)
mostrar_transaccion(caso3)


# =========================================================
# PERMITIR INGRESAR UNA TRANSACCION DIFERENTE
# =========================================================

print("\n")
print("======================================")
print("|=======NUEVA TRANSACCION=======|")
print("======================================")

respuesta = input(
    "¿Desea ingresar una nueva transacción? (S/N): "
).strip().upper()


if respuesta == "S":

    while True:

        try:

            id = pedir_id()

            # Comprobar que el ID no esté repetido

            repetido = False

            for transaccion in transacciones:

                if transaccion.id == id:
                    repetido = True
                    break

            if repetido:

                print(
                    "ERROR: Ese ID ya existe. Ingrese otro."
                )

                continue

            break

        except ValueError as error:

            print("ERROR:", error)


    titular = pedir_titular()

    Valor = pedir_valor()

    Hora = pedir_hora()

    Pais = pedir_pais()

    Dispositivo_Conocido = pedir_dispositivo()


    try:

        nueva_transaccion = Transaccion(
            id,
            titular,
            Valor,
            Hora,
            Pais,
            Dispositivo_Conocido
        )

        transacciones.append(nueva_transaccion)

        print("\nTransacción creada correctamente.")

        mostrar_transaccion(nueva_transaccion)

    except ValueError as error:

        print(
            "No se pudo crear la transacción:",
            error
        )


elif respuesta == "N":

    print("No se agregará una nueva transacción.")


else:

    print(
        "Respuesta no reconocida. "
        "Se continuarán únicamente los casos de prueba."
    )


# =========================================================
# GUARDAR TODA LA LISTA
# =========================================================

guardar_transacciones(transacciones)


print("\n======================================")
print("Programa finalizado correctamente.")
print("Cantidad total de transacciones:", len(transacciones))
print("======================================")