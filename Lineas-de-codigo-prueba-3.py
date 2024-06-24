import os
import json
import re
import ipaddress
import requests

class Campus:
    """Representa un campus con una descripción y una lista de dispositivos."""
    def __init__(self, nombre, descripcion):
        self.nombre = nombre  # Nombre del campus
        self.descripcion = descripcion  # Descripción del campus
        self.dispositivos = []  # Lista de dispositivos en el campus

class Dispositivo:
    """Representa un dispositivo de red con sus atributos."""
    def __init__(self, nombre, modelo, capa, interfaces, ips_masks, vlans, servicios):
        self.nombre = nombre  # Nombre del dispositivo
        self.modelo = modelo  # Modelo del dispositivo
        self.capa = capa  # Capa jerárquica del dispositivo
        self.interfaces = interfaces  # Lista de interfaces de red del dispositivo
        self.ips_masks = ips_masks  # Diccionario de IPs y máscaras de red por interfaz
        self.vlans = vlans  # Diccionario de VLANs
        self.servicios = servicios  # Lista de servicios de red configurados

def es_direccion_ipv4(direccion):
    """Valida si una dirección IP es válida."""
    patron = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
    if patron.match(direccion):
        octetos = direccion.split('.')
        for octeto in octetos:
            if int(octeto) < 0 or int(octeto) > 255:
                return False
        return True
    return False

def es_direccion_ipv6(direccion):
    """Valida si una dirección IPv6 es válida."""
    try:
        ipaddress.IPv6Address(direccion)
        return True
    except ipaddress.AddressValueError:
        return False

class AdministradorRedes:
    """Clase principal para administrar campus y dispositivos de red."""
    
    def __init__(self, nombre_archivo, restconf_url, restconf_username, restconf_password):
        self.nombre_archivo = nombre_archivo
        self.campus = {}
        self.restconf_url = restconf_url
        self.restconf_auth = (restconf_username, restconf_password)
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

        nombre_campus = input("Ingrese el nombre del campus: ")
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
            print(f"Dispositivos en el campus {nombre_campus}:")
            for dispositivo in campus.dispositivos:
                print(f"- {dispositivo.nombre}")

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
        interfaces = input("Ingrese las interfaces del dispositivo (separadas por comas): ").split(",")
        ips_masks = {iface: (input(f"Ingrese la IP para la interfaz {iface}: "), input(f"Ingrese la máscara para la interfaz {iface}: ")) for iface in interfaces}
        vlans = {input(f"Ingrese el nombre de la VLAN: "): input(f"Ingrese el número de la VLAN: ")}
        servicios = input("Ingrese los servicios del dispositivo (separados por comas): ").split(",")
        
        nuevo_dispositivo = Dispositivo(nombre, modelo, capa, interfaces, ips_masks, vlans, servicios)
        campus.dispositivos.append(nuevo_dispositivo)
        self.guardar_dispositivo_en_restconf(campus, nuevo_dispositivo)
        input("Dispositivo agregado. Presione Enter para continuar.")

    def modificar_dispositivo(self, campus):
        """Modifica un dispositivo existente en un campus."""
        nombre = input("Ingrese el nombre del dispositivo que desea modificar: ")
        dispositivo = next((d for d in campus.dispositivos if d.nombre == nombre), None)

        if dispositivo:
            dispositivo.modelo = input(f"Ingrese el nuevo modelo del dispositivo (actual: {dispositivo.modelo}): ")
            dispositivo.capa = input(f"Ingrese la nueva capa del dispositivo (actual: {dispositivo.capa}): ")
            dispositivo.interfaces = input(f"Ingrese las nuevas interfaces del dispositivo (actual: {', '.join(dispositivo.interfaces)}): ").split(",")
            dispositivo.ips_masks = {iface: (input(f"Ingrese la nueva IP para la interfaz {iface}: "), input(f"Ingrese la nueva máscara para la interfaz {iface}: ")) for iface in dispositivo.interfaces}
            dispositivo.vlans = {input(f"Ingrese el nuevo nombre de la VLAN: "): input(f"Ingrese el nuevo número de la VLAN: ")}
            dispositivo.servicios = input(f"Ingrese los nuevos servicios del dispositivo (actual: {', '.join(dispositivo.servicios)}): ").split(",")
            
            self.modificar_dispositivo_en_restconf(campus, dispositivo)
            input("Dispositivo modificado. Presione Enter para continuar.")
        else:
            input("El dispositivo especificado no existe. Presione Enter para continuar.")

    def borrar_dispositivo(self, campus):
        """Elimina un dispositivo de un campus."""
        nombre = input("Ingrese el nombre del dispositivo que desea borrar: ")
        dispositivo = next((d for d in campus.dispositivos if d.nombre == nombre), None)

        if dispositivo:
            campus.dispositivos.remove(dispositivo)
            self.borrar_dispositivo_en_restconf(campus, dispositivo)
            input("Dispositivo eliminado. Presione Enter para continuar.")
        else:
            input("El dispositivo especificado no existe. Presione Enter para continuar.")

    def ver_campus(self):
        """Muestra la lista de campus y sus dispositivos."""
        self.limpiar_pantalla()
        print(self.convertir_a_formato_texto())
        input("Presione Enter para volver al menú principal.")

    def guardar_dispositivo_en_restconf(self, campus, dispositivo):
        """Guarda un dispositivo en el servidor RESTCONF."""
        url = f"{self.restconf_url}/data/campus={campus.nombre}/dispositivos={dispositivo.nombre}"
        data = {
            "modelo": dispositivo.modelo,
            "capa": dispositivo.capa,
            "interfaces": dispositivo.interfaces,
            "ips_masks": dispositivo.ips_masks,
            "vlans": dispositivo.vlans,
            "servicios": dispositivo.servicios
        }
        response = requests.post(url, auth=self.restconf_auth, json=data)
        if response.status_code == 201:
            print("Dispositivo guardado en RESTCONF.")
        else:
            print(f"Error al guardar el dispositivo en RESTCONF: {response.text}")

    def modificar_dispositivo_en_restconf(self, campus, dispositivo):
        """Modifica un dispositivo en el servidor RESTCONF."""
        url = f"{self.restconf_url}/data/campus={campus.nombre}/dispositivos={dispositivo.nombre}"
        data = {
            "modelo": dispositivo.modelo,
            "capa": dispositivo.capa,
            "interfaces": dispositivo.interfaces,
            "ips_masks": dispositivo.ips_masks,
            "vlans": dispositivo.vlans,
            "servicios": dispositivo.servicios
        }
        response = requests.put(url, auth=self.restconf_auth, json=data)
        if response.status_code == 200:
            print("Dispositivo modificado en RESTCONF.")
        else:
            print(f"Error al modificar el dispositivo en RESTCONF: {response.text}")

    def borrar_dispositivo_en_restconf(self, campus, dispositivo):
        """Elimina un dispositivo del servidor RESTCONF."""
        url = f"{self.restconf_url}/data/campus={campus.nombre}/dispositivos={dispositivo.nombre}"
        response = requests.delete(url, auth=self.restconf_auth)
        if response.status_code == 204:
            print("Dispositivo eliminado de RESTCONF.")
        else:
            print(f"Error al eliminar el dispositivo en RESTCONF: {response.text}")

if __name__ == "__main__":
    archivo_json = "datos.json"
    restconf_url = "http://localhost:8080/restconf"
    restconf_username = "admin"
    restconf_password = "admin"
    admin_redes = AdministradorRedes(archivo_json, restconf_url, restconf_username, restconf_password)
    admin_redes.menu_principal()
