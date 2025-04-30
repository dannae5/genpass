"""
Script Generador de Contraseñas Seguras - genPass

Este script permite:
- Generar contraseñas personalizadas o completamente aleatorias.
- Especificar longitud, cantidad de números y caracteres especiales.
- Usar una palabra base para construir la contraseña.
- Generar varias claves a la vez.
- Guardarlas en un fichero, aplicar hash o copiar al portapapeles.
- Limpiar la pantalla opcionalmente.
"""

import secrets
import string
import argparse
import sys
import os
import hashlib
import pyperclip
from colorama import Fore, Style, init

# Inicializa colorama para dar formato de color a los mensajes en consola
init(autoreset=True)

class Generador:
    """
    Clase encargada de generar contraseñas seguras y manejar funcionalidades adicionales
    como copiar al portapapeles, aplicar hash y guardar en archivos.
    """

    def __init__(self):
        # Atributo privado que almacena la última contraseña generada
        self.__password = None

    def generarContrasena(self,
                          longitud: int = 12,
                          usarEspeciales: bool = True,
                          cantEspeciales: int = 2,
                          usarNumeros: bool = True,
                          cantNumeros: int = 2,
                          palabraBase: str = "") -> str:
        """
        Genera una contraseña basada en parámetros personalizados.

        Args:
            longitud (int): Longitud total de la contraseña.
            usarEspeciales (bool): Si se deben incluir caracteres especiales.
            cantEspeciales (int): Cantidad de caracteres especiales.
            usarNumeros (bool): Si se deben incluir números.
            cantNumeros (int): Cantidad de dígitos numéricos.
            palabraBase (str): Palabra base con la que iniciar la contraseña.

        Returns:
            str: Contraseña generada.
        """
        try:
            if longitud < len(palabraBase) + cantEspeciales + cantNumeros:
                raise ValueError("La longitud debe ser suficiente para incluir todos los elementos.")

            letras = string.ascii_letters
            especiales = string.punctuation if usarEspeciales else ''
            numeros = string.digits if usarNumeros else ''

            # Se arma la contraseña con los elementos requeridos
            password_chars = list(palabraBase)
            password_chars += [secrets.choice(numeros) for _ in range(cantNumeros)]
            password_chars += [secrets.choice(especiales) for _ in range(cantEspeciales)]

            # Completa con letras hasta llegar a la longitud deseada
            restantes = longitud - len(password_chars)
            password_chars += [secrets.choice(letras) for _ in range(restantes)]

            # Mezcla aleatoria de caracteres
            secrets.SystemRandom().shuffle(password_chars)
            self.__password = ''.join(password_chars)
            return self.__password

        except Exception as e:
            print(f"{Fore.RED}⚠️ Error al generar la contraseña: {e}")
            sys.exit(1)

    def generarContrasenaAleatoria(self) -> str:
        """
        Genera una contraseña completamente aleatoria con parámetros predefinidos.

        Returns:
            str: Contraseña aleatoria generada.
        """
        longitud = 16
        cantEspeciales = 3
        cantNumeros = 3

        letras = string.ascii_letters
        especiales = string.punctuation
        numeros = string.digits

        # Se eligen aleatoriamente los caracteres de cada tipo
        password_chars = (
            [secrets.choice(numeros) for _ in range(cantNumeros)] +
            [secrets.choice(especiales) for _ in range(cantEspeciales)]
        )

        # Rellenar con letras hasta completar la longitud
        restantes = longitud - len(password_chars)
        password_chars += [secrets.choice(letras) for _ in range(restantes)]

        # Mezcla aleatoria de todos los caracteres
        secrets.SystemRandom().shuffle(password_chars)
        self.__password = ''.join(password_chars)
        return self.__password

    def aplicarHash(self, tipo_hash: str = "sha256") -> str:
        """
        Aplica un algoritmo hash criptográfico a la última contraseña generada.

        Args:
            tipo_hash (str): Tipo de algoritmo hash a usar (e.g. 'sha256', 'md5').

        Returns:
            str: Cadena hexadecimal del hash generado.
        """
        try:
            h = hashlib.new(tipo_hash)
            h.update(self.__password.encode())
            return h.hexdigest()
        except ValueError:
            print(f"{Fore.YELLOW}⚠️ Algoritmo de hash no soportado.")
            return ""

    def guardarEnFichero(self, archivo: str, contenido: str):
        """
        Guarda el contenido especificado en un archivo.

        Args:
            archivo (str): Nombre del archivo donde se guardará.
            contenido (str): Contenido a escribir.
        """
        try:
            with open(archivo, 'a', encoding='utf-8') as f:
                f.write(contenido + '\n')
            print(f"{Fore.GREEN}✅ Contraseña guardada en '{archivo}'")
        except Exception as e:
            print(f"{Fore.RED}❌ Error al guardar en archivo: {e}")

    def copiarAlPortapapeles(self):
        """
        Copia la contraseña actual al portapapeles del sistema.
        """
        try:
            pyperclip.copy(self.__password)
            print(f"{Fore.CYAN}📋 Contraseña copiada al portapapeles.")
        except Exception:
            print(f"{Fore.YELLOW}⚠️ No se pudo acceder al portapapeles.")

    @staticmethod
    def limpiarPantalla():
        """
        Limpia la pantalla de la consola dependiendo del sistema operativo.
        """
        limpiar = lambda: os.system('cls' if os.name == 'nt' else 'clear')
        limpiar()


def menuInteractivo() -> int:
    """
    Muestra el menú interactivo del programa genPass.

    Returns:
        int: Opción seleccionada por el usuario.
    """
    while True:
        Generador.limpiarPantalla()
        print(f"{Fore.MAGENTA}{'-'*40}")
        print(f"{Fore.CYAN}        🔒 genPass - Generador de Contraseñas")
        print(f"{Fore.MAGENTA}{'-'*40}\n")
        print("1. 📝 Generar contraseña personalizada")
        print("2. 🔁 Generar contraseña aleatoria (básica)")
        print("3. 💥 Generar varias claves aleatorias")
        print("4. 🔐 Generar clave totalmente aleatoria")
        print("5. 🚪 Salir\n")

        try:
            opcion = int(input(f"{Fore.YELLOW}Seleccione una opción (1-5): "))
            if 1 <= opcion <= 5:
                return opcion
            else:
                print(f"{Fore.RED}⚠️ Opción inválida. Intente nuevamente.")
        except ValueError:
            print(f"{Fore.RED}⚠️ Entrada inválida. Ingrese solo números.")


def main():
    """
    Función principal del programa.
    Controla el flujo de ejecución según la opción elegida por el usuario.
    """
    generador = Generador()

    while True:
        op = menuInteractivo()

        if op == 5:
            print(f"{Fore.GREEN}👋 ¡Gracias por usar genPass!")
            break

        elif op == 1:
            print(f"\n{Fore.CYAN}🔧 Generar contraseña personalizada:")
            try:
                longitud = int(input("Longitud deseada: "))
                usarEspeciales = input("¿Usar caracteres especiales? (s/n): ").lower() == 's'
                cantEspeciales = int(input("Cantidad de especiales: ")) if usarEspeciales else 0
                usarNumeros = input("¿Usar números? (s/n): ").lower() == 's'
                cantNumeros = int(input("Cantidad de números: ")) if usarNumeros else 0
                palabraBase = input("Palabra base (opcional): ")
                cantidad = int(input("¿Cuántas contraseñas generar?: "))

                for i in range(cantidad):
                    # Generación y visualización de contraseña
                    contra = generador.generarContrasena(
                        longitud=longitud,
                        usarEspeciales=usarEspeciales,
                        cantEspeciales=cantEspeciales,
                        usarNumeros=usarNumeros,
                        cantNumeros=cantNumeros,
                        palabraBase=palabraBase
                    )
                    print(f"\n{Fore.GREEN}🔐 Contraseña {i+1}: {contra}")

                    if input("¿Aplicar hash? (s/n): ").lower() == 's':
                        tipo_hash = input("Tipo de hash (ej. sha256, md5, sha1): ")
                        hashed = generador.aplicarHash(tipo_hash)
                        print(f"   🔐 Hash generado: {hashed}")
                        if input("¿Guardar en archivo? (s/n): ").lower() == 's':
                            archivo = input("Nombre del archivo (ej. passwords.txt): ")
                            generador.guardarEnFichero(archivo, f"Contraseña: {contra}, Hash: {hashed}")
                    else:
                        if input("¿Guardar en archivo? (s/n): ").lower() == 's':
                            archivo = input("Nombre del archivo: ")
                            generador.guardarEnFichero(archivo, contra)

                    if input("¿Copiar al portapapeles? (s/n): ").lower() == 's':
                        generador.copiarAlPortapapeles()

            except Exception as e:
                print(f"{Fore.RED}❌ Error en entrada: {e}")

        elif op == 2:
            # Opción para generar una sola contraseña aleatoria simple
            print(f"\n{Fore.MAGENTA}🔄 Generando contraseña aleatoria básica...")
            contra = generador.generarContrasenaAleatoria()
            print(f"{Fore.GREEN}🔐 Contraseña generada: {contra}")

            if input("¿Aplicar hash? (s/n): ").lower() == 's':
                tipo_hash = input("Tipo de hash (ej. sha256, md5, sha1): ")
                hashed = generador.aplicarHash(tipo_hash)
                print(f"   🔐 Hash generado: {hashed}")

            if input("¿Guardar en archivo? (s/n): ").lower() == 's':
                archivo = input("Nombre del archivo: ")
                generador.guardarEnFichero(archivo, contra)

            if input("¿Copiar al portapapeles? (s/n): ").lower() == 's':
                generador.copiarAlPortapapeles()

        elif op == 3:
            # Genera múltiples contraseñas aleatorias sin opciones personalizadas
            cantidad = int(input("\n¿Cuántas contraseñas aleatorias generar?: "))
            print(f"{Fore.MAGENTA}🔄 Generando {cantidad} contraseñas aleatorias...\n")
            for i in range(cantidad):
                contra = generador.generarContrasenaAleatoria()
                print(f"{Fore.GREEN}🔐 Contraseña {i+1}: {contra}")

        elif op == 4:
            # Similar a la opción 2 pero con hash y guardado opcional
            print(f"{Fore.MAGENTA}🔒 Generando una contraseña totalmente aleatoria...\n")
            contra = generador.generarContrasenaAleatoria()
            print(f"{Fore.GREEN}🔐 Contraseña generada: {contra}")

            if input("¿Aplicar hash? (s/n): ").lower() == 's':
                tipo_hash = input("Tipo de hash (ej. sha256, md5, sha1): ")
                hashed = generador.aplicarHash(tipo_hash)
                print(f"   🔐 Hash generado: {hashed}")

            if input("¿Guardar en archivo? (s/n): ").lower() == 's':
                archivo = input("Nombre del archivo (ej. passwords.txt): ")
                generador.guardarEnFichero(archivo, f"Contraseña: {contra}, Hash: {hashed}" if tipo_hash else contra)

            if input("¿Copiar al portapapeles? (s/n): ").lower() == 's':
                generador.copiarAlPortapapeles()

        # Opción para salir del bucle principal
        if input("\n¿Volver al menú principal? (s/n): ").lower() != 's':
            break

    Generador.limpiarPantalla()


# Punto de entrada del programa
if __name__ == "__main__":
    main()
