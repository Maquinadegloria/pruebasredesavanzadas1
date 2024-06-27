import os
import json
import requests
import subprocess
from github import Github
from campus import Campus
from dispositivo import Dispositivo

class AdministradorRedes:
    """Clase principal para administrar campus y dispositivos de red."""
    
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo
        self.campus = {}
        self.cargar_desde_archivo()

    def cargar_desde_archivo(self):
        """Carga los datos de campus y dispositivos desde el archivo JSON."""
        if not os.path.exists(self.nombre_archivo):
            return

        with open(self.nombre_archivo, "r") as archivo:
            try:
                datos = json.load(archivo)
                for nombre, descripcion in datos.get("campus", {}).items():
                    campus = Campus(nombre, descripcion)
                    self.campus[nombre] = campus
                    for dispositivo_info in datos.get(nombre, []):
                        dispositivo = Dispositivo(**dispositivo_info)
                        campus.dispositivos.append(dispositivo)
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error al leer el archivo {self.nombre_archivo}: {e}")

    def guardar_en_archivo(self):
        """Guarda los datos en un archivo JSON."""
        datos = {"campus": {}}
        for nombre, campus in self.campus.items():
            datos["campus"][nombre] = campus.descripcion
            datos[nombre] = [dispositivo.__dict__ for dispositivo in campus.dispositivos]

        with open(self.nombre_archivo, "w") as archivo:
            json.dump(datos, archivo, indent=4)

    def convertir_a_formato_texto(self):
        """Convierte los datos a formato de texto legible."""
        texto = ""
        for nombre, campus in self.campus.items():
            texto += f"Campus: {nombre}\nDescripción: {campus.descripcion}\n"
            for dispositivo in campus.dispositivos:
                texto += f"\nDispositivo: {dispositivo.nombre}\n"
                texto += f"Modelo: {dispositivo.modelo}\n"
                texto += f"Capa: {dispositivo.capa}\n"
                texto += "Interfaces:\n"
                for interface in dispositivo.interfaces:
                    ip, mask = dispositivo.ips_masks.get(interface, ("No configurada", "No configurada"))
                    texto += f"- {interface}: IP: {ip}, Máscara: {mask}\n"
                texto += "VLANs:\n"
                for vlan, numero in dispositivo.vlans.items():
                    texto += f"- {vlan}: {numero}\n"
                texto += f"Servicios: {', '.join(dispositivo.servicios)}\n"
                texto += "-" * 30 + "\n"
        return texto

    def guardar_y_convertir_datos(self):
        """Guarda los datos en JSON y luego los convierte a texto."""
        self.guardar_en_archivo()
        print("Datos guardados en formato JSON.")

        while True:
            archivo_texto = input("Ingrese el nombre del archivo de texto para guardar los datos convertidos: ")
            if archivo_texto:
                try:
                    with open(archivo_texto, "w") as archivo:
                        archivo.write(self.convertir_a_formato_texto())
                    print(f"Datos convertidos y guardados en el archivo: {archivo_texto}")
                    break
                except IOError as e:
                    print(f"Error al escribir en el archivo: {e}")
            else:
                print("El nombre del archivo no puede estar vacío. Por favor, inténtelo de nuevo.")

    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def menu_principal(self):
        """Muestra el menú principal y permite al usuario seleccionar una opción."""
        opciones = {
            "1": self.administrar_campus,
            "2": self.administrar_dispositivos,
            "3": self.guardar_y_convertir_datos,
            "4": self.ver_campus,
            "5": self.salir
        }

        while True:
            self.limpiar_pantalla()
            print("¡Bienvenido al Administrador de Redes!")
            print("1. Administrar campus")
            print("2. Administrar dispositivos de red")
            print("3. Guardar y convertir datos")
            print("4. Ver campus y dispositivos")
            print("5. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion in opciones:
                opciones[opcion]()
            else:
                input("Opción no válida. Presione Enter para continuar.")

    def salir(self):
        """Sale del programa."""
        print("¡Hasta luego!")
        exit()

    def administrar_campus(self):
        """Muestra el menú de administración de campus y permite al usuario seleccionar una opción."""
        opciones = {
            "1": self.agregar_campus,
            "2": self.modificar_campus,
            "3": self.borrar_campus,
            "4": lambda: None
        }

        while True:
            self.limpiar_pantalla()
            print("Campus:")
            for nombre in sorted(self.campus.keys()):
                print(nombre)
            opcion = input("Seleccione una opción:\n1. Agregar campus\n2. Modificar campus\n3. Borrar campus\n4. Volver al menú principal\n")

            if opcion in opciones:
                if opcion == "4":
                    break
                else:
                    opciones[opcion]()
            else:
                input("Opción no válida. Presione Enter para continuar.")

    def agregar_campus(self):
        """Agrega un nuevo campus a la instancia de la clase."""
        nombre = input("Ingrese el nombre del campus: ")
        descripcion = input("Ingrese una descripción del campus: ")
        if nombre in self.campus:
            input("El campus ya existe. Presione Enter para continuar.")
        else:
            self.campus[nombre] = Campus(nombre, descripcion)
            input("Campus agregado. Presione Enter para continuar.")

    def modificar_campus(self):
        """Modifica la descripción de un campus existente en la instancia de la clase."""
        nombre = input("Ingrese el nombre del campus que desea modificar: ")
        if nombre in self.campus:
            nueva_descripcion = input("Ingrese la nueva descripción del campus: ")
            self.campus[nombre].descripcion = nueva_descripcion
            input("Campus modificado. Presione Enter para continuar.")
        else:
            input("El campus especificado no existe. Presione Enter para continuar.")

    def borrar_campus(self):
        """Elimina un campus existente de la instancia de la clase."""
        nombre = input("Ingrese el nombre del campus que desea borrar: ")
        if nombre in self.campus:
            del self.campus[nombre]
            input("Campus eliminado. Presione Enter para continuar.")
        else:
            input("El campus especificado no existe. Presione Enter para continuar.")

    def administrar_dispositivos(self):
        """Administra los dispositivos dentro de un campus."""
        self.limpiar_pantalla()
        print("Campus disponibles:")
        for nombre in sorted(self.campus.keys()):
            print(f"- {nombre}")

        nombre_campus = input("Ingrese el nombre del campus para administrar dispositivos: ")
        if nombre_campus not in self.campus:
            input("El campus especificado no existe. Presione Enter para continuar.")
            return

        campus = self.campus[nombre_campus]

        opciones = {
            "1": lambda: self.agregar_dispositivo(campus),
            "2": lambda: self.modificar_dispositivo(campus),
            "3": lambda: self.borrar_dispositivo(campus),
            "4": lambda: None
        }

        while True:
            self.limpiar_pantalla()
            print(f"Campus: {nombre_campus}")
            for dispositivo in campus.dispositivos:
                print(f"- {dispositivo.nombre} ({dispositivo.modelo}, {dispositivo.capa})")
            opcion = input("Seleccione una opción:\n1. Agregar dispositivo\n2. Modificar dispositivo\n3. Borrar dispositivo\n4. Volver al menú principal\n")

            if opcion in opciones:
                if opcion == "4":
                    break
                else:
                    opciones[opcion]()
            else:
                input("Opción no válida. Presione Enter para continuar.")

    def agregar_dispositivo(self, campus):
        """Agrega un nuevo dispositivo a un campus."""
        nombre = input("Ingrese el nombre del dispositivo: ")
        modelo = input("Ingrese el modelo del dispositivo: ")
        capa = input("Ingrese la capa del dispositivo: ")
        interfaces = input("Ingrese las interfaces del dispositivo (separadas por comas): ").split(',')
        ips_masks = {}
        vlans = {}
        servicios = input("Ingrese los servicios del dispositivo (separados por comas): ").split(',')

        for interface in interfaces:
            ip = input(f"Ingrese la IP para la interfaz {interface}: ")
            mascara = input(f"Ingrese la máscara para la interfaz {interface}: ")
            ips_masks[interface] = (ip, mascara)

        while True:
            vlan_nombre = input("Ingrese el nombre de la VLAN (o deje vacío para terminar): ")
            if not vlan_nombre:
                break
            vlan_numero = input(f"Ingrese el número de la VLAN {vlan_nombre}: ")
            vlans[vlan_nombre] = vlan_numero

        dispositivo = Dispositivo(nombre, modelo, capa, interfaces, ips_masks, vlans, servicios)
        campus.dispositivos.append(dispositivo)
        input("Dispositivo agregado. Presione Enter para continuar.")

    def modificar_dispositivo(self, campus):
        """Modifica un dispositivo existente en un campus."""
        nombre = input("Ingrese el nombre del dispositivo que desea modificar: ")
        dispositivo = next((d for d in campus.dispositivos if d.nombre == nombre), None)

        if not dispositivo:
            input("El dispositivo especificado no existe. Presione Enter para continuar.")
            return

        nuevo_nombre = input(f"Ingrese el nuevo nombre del dispositivo (actual: {dispositivo.nombre}): ")
        nuevo_modelo = input(f"Ingrese el nuevo modelo del dispositivo (actual: {dispositivo.modelo}): ")
        nueva_capa = input(f"Ingrese la nueva capa del dispositivo (actual: {dispositivo.capa}): ")
        nuevas_interfaces = input(f"Ingrese las nuevas interfaces del dispositivo (actual: {', '.join(dispositivo.interfaces)}): ").split(',')
        nuevos_servicios = input(f"Ingrese los nuevos servicios del dispositivo (actual: {', '.join(dispositivo.servicios)}): ").split(',')

        dispositivo.nombre = nuevo_nombre if nuevo_nombre else dispositivo.nombre
        dispositivo.modelo = nuevo_modelo if nuevo_modelo else dispositivo.modelo
        dispositivo.capa = nueva_capa if nueva_capa else dispositivo.capa
        dispositivo.interfaces = nuevas_interfaces if nuevas_interfaces else dispositivo.interfaces
        dispositivo.servicios = nuevos_servicios if nuevos_servicios else dispositivo.servicios

        dispositivo.ips_masks = {}
        for interface in dispositivo.interfaces:
            ip = input(f"Ingrese la IP para la interfaz {interface} (actual: {dispositivo.ips_masks.get(interface, ('No configurada',))[0]}): ")
            mascara = input(f"Ingrese la máscara para la interfaz {interface} (actual: {dispositivo.ips_masks.get(interface, ('No configurada', 'No configurada'))[1]}): ")
            dispositivo.ips_masks[interface] = (ip, mascara)

        dispositivo.vlans = {}
        while True:
            vlan_nombre = input("Ingrese el nombre de la VLAN (o deje vacío para terminar): ")
            if not vlan_nombre:
                break
            vlan_numero = input(f"Ingrese el número de la VLAN {vlan_nombre}: ")
            dispositivo.vlans[vlan_nombre] = vlan_numero

        input("Dispositivo modificado. Presione Enter para continuar.")

    def borrar_dispositivo(self, campus):
        """Borra un dispositivo de un campus."""
        nombre = input("Ingrese el nombre del dispositivo que desea borrar: ")
        dispositivo = next((d for d in campus.dispositivos if d.nombre == nombre), None)

        if dispositivo:
            campus.dispositivos.remove(dispositivo)
            input("Dispositivo eliminado. Presione Enter para continuar.")
        else:
            input("El dispositivo especificado no existe. Presione Enter para continuar.")

    def ver_campus(self):
        """Muestra los campus y dispositivos en formato de texto legible."""
        texto = self.convertir_a_formato_texto()
        print(texto)
        input("Presione Enter para continuar.")

    def hacer_solicitud_http(self, url):
        """Ejemplo de cómo hacer una solicitud HTTP utilizando la biblioteca requests."""
        try:
            respuesta = requests.get(url)
            if respuesta.status_code == 200:
                print(f"Respuesta del servidor: {respuesta.text}")
            else:
                print(f"Error en la solicitud: {respuesta.status_code}")
        except requests.RequestException as e:
            print(f"Excepción durante la solicitud HTTP: {e}")

    def clonar_repositorio(self, url_repositorio, directorio_destino):
        """Ejemplo de cómo clonar un repositorio Git utilizando subprocess."""
        try:
            resultado = subprocess.run(["git", "clone", url_repositorio, directorio_destino], check=True, capture_output=True, text=True)
            print(f"Repositorio clonado en {directorio_destino}. Salida: {resultado.stdout}")
        except subprocess.CalledProcessError as e:
            print(f"Error al clonar el repositorio: {e.stderr}")

    def crear_issue_github(self, token, repositorio, titulo, cuerpo):
        """Ejemplo de cómo crear un issue en GitHub utilizando PyGithub."""
        try:
            g = Github(token)
            repo = g.get_repo(repositorio)
            issue = repo.create_issue(title=titulo, body=cuerpo)
            print(f"Issue creado: {issue.html_url}")
        except Exception as e:
            print(f"Error al crear el issue: {e}")
