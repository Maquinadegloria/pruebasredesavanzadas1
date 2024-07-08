import os
import json
import re
import ipaddress

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

        while True:
            self.limpiar_pantalla()
            print("Dispositivos en el campus:")
            for dispositivo in self.campus[nombre_campus].dispositivos:
                print(f"{dispositivo.nombre} ({dispositivo.modelo})")
            opcion = input("Seleccione una opción:\n1. Agregar dispositivo\n2. Modificar dispositivo\n3. Ver dispositivo\n4. Borrar dispositivo\n5. Volver al menú anterior\n")
            if opcion == "5":
                break
            elif opcion == "1":
                self.agregar_dispositivos(nombre_campus)
            elif opcion == "2":
                self.modificar_dispositivo(nombre_campus)
            elif opcion == "3":
                self.ver_dispositivo(nombre_campus)
            elif opcion == "4":
                self.borrar_dispositivo(nombre_campus)
            else:
                input("Opción no válida. Presione Enter para continuar.")

    def agregar_dispositivos(self, nombre_campus):
        """Agrega un nuevo dispositivo a un campus existente."""
        nombre = input("Ingrese el nombre del dispositivo: ")
        modelo = input("Ingrese el modelo del dispositivo: ")
        capa = self.seleccionar_capa()
        interfaces = input("Ingrese las interfaces de red del dispositivo (separadas por coma): ").split(",")
        interfaces = [interface.strip() for interface in interfaces if interface.strip()]
        ips_masks = self.ingresar_ips_masks(interfaces)
        vlans = self.ingresar_vlans()
        servicios = input("Ingrese los servicios de red configurados (separados por coma): ").split(",")
        servicios = [servicio.strip() for servicio in servicios if servicio.strip()]

        dispositivo = Dispositivo(
            nombre=nombre,
            modelo=modelo,
            capa=capa,
            interfaces=interfaces,
            ips_masks=ips_masks,
            vlans=vlans,
            servicios=servicios
        )
        self.campus[nombre_campus].dispositivos.append(dispositivo)
        print("Dispositivo agregado.")
        input("Presione Enter para continuar.")

    def seleccionar_capa(self):
        """Muestra el menú de selección de capa y permite al usuario seleccionar una opción."""
        while True:
            print("Seleccione la capa jerárquica a la que pertenece:")
            print("1) Núcleo")
            print("2) Distribución")
            print("3) Acceso")
            capa_opcion = input("Opción: ")
            if capa_opcion == "1":
                return "Núcleo"
            elif capa_opcion == "2":
                return "Distribución"
            elif capa_opcion == "3":
                return "Acceso"
            else:
                print("Opción no válida. Inténtelo de nuevo.")

    def ingresar_ips_masks(self, interfaces):
        """Solicita al usuario ingresar las direcciones IP y máscaras de red para las interfaces de un dispositivo."""
        ips_masks = {}
        for interfaz in interfaces:
            while True:
                ip = input(f"Ingrese la dirección IP para la interfaz {interfaz}: ")
                if es_direccion_ipv4(ip) or es_direccion_ipv6(ip):
                    mask = input(f"Ingrese la máscara de red para la interfaz {interfaz}: ")
                    try:
                        ip_obj = ipaddress.ip_interface(f"{ip}/{mask}")
                        ips_masks[interfaz] = (str(ip_obj.ip), str(ip_obj.netmask))
                        break
                    except ValueError:
                        print("Máscara de red no válida. Inténtelo nuevamente.")
                else:
                    print("Dirección IP no válida. Inténtelo nuevamente.")
        return ips_masks

    def ingresar_vlans(self):
        """Solicita al usuario ingresar los nombres y números de VLAN para un dispositivo."""
        vlans = {}
        while True:
            nombre_vlan = input("Ingrese el nombre de la VLAN (o 'fin' para terminar): ")
            if nombre_vlan.lower() == 'fin':
                break
            try:
                numero_vlan = int(input("Ingrese el número de la VLAN: "))
                vlans[nombre_vlan] = numero_vlan
            except ValueError:
                print("El número de VLAN debe ser un entero. Inténtelo de nuevo.")
        return vlans

    def modificar_dispositivo(self, nombre_campus):
        """Modifica un dispositivo existente en un campus."""
        nombre_dispositivo = input("Ingrese el nombre del dispositivo que desea modificar: ")
        for dispositivo in self.campus[nombre_campus].dispositivos:
            if dispositivo.nombre == nombre_dispositivo:
                modelo = input(f"Ingrese el nuevo modelo del dispositivo (actual: {dispositivo.modelo}): ")
                capa = self.seleccionar_capa()
                nuevas_interfaces = input("Ingrese las nuevas interfaces de red del dispositivo (separadas por coma): ").split(",")
                nuevas_ips_masks = self.ingresar_ips_masks(nuevas_interfaces)
                nuevas_vlans = self.ingresar_vlans()
                nuevos_servicios = input(f"Ingrese los nuevos servicios de red configurados (actual: {', '.join(dispositivo.servicios)}): ").split(",")

                dispositivo.modelo = modelo
                dispositivo.capa = capa
                dispositivo.interfaces.extend(nuevas_interfaces)
                dispositivo.ips_masks.update(nuevas_ips_masks)
                dispositivo.vlans.update(nuevas_vlans)
                dispositivo.servicios = nuevos_servicios

                print("Dispositivo modificado.")
                input("Presione Enter para continuar.")
                return
        print("Dispositivo no encontrado.")
        input("Presione Enter para continuar.")

    def ver_dispositivo(self, nombre_campus):
        """Muestra la información de un dispositivo existente en un campus."""
        nombre_dispositivo = input("Ingrese el nombre del dispositivo que desea ver: ")
        for dispositivo in self.campus[nombre_campus].dispositivos:
            if dispositivo.nombre == nombre_dispositivo:
                print(f"Nombre: {dispositivo.nombre}")
                print(f"Modelo: {dispositivo.modelo}")
                print(f"Capa: {dispositivo.capa}")
                print("Interfaces:")
                for interface in dispositivo.interfaces:
                    ip, mask = dispositivo.ips_masks.get(interface, ("", ""))
                    print(f"- {interface}: IP: {ip}, Máscara: {mask}")
                print("VLANs:")
                for vlan, numero in dispositivo.vlans.items():
                    print(f"- {vlan}: {numero}")
                print(f"Servicios: {', '.join(dispositivo.servicios)}")
                input("Presione Enter para continuar.")
                return
        print("Dispositivo no encontrado.")
        input("Presione Enter para continuar.")

    def ver_campus(self):
        """Muestra la información de todos los campus y dispositivos."""
        for nombre, campus in self.campus.items():
            print(f"Campus: {nombre}\nDescripción: {campus.descripcion}")
            for dispositivo in campus.dispositivos:
                print(f"  Dispositivo: {dispositivo.nombre}")
                print(f"  Modelo: {dispositivo.modelo}")
                print(f"  Capa: {dispositivo.capa}")
                print("  Interfaces:")
                for interface in dispositivo.interfaces:
                    ip, mask = dispositivo.ips_masks.get(interface, ("", ""))
                    print(f"    - {interface}: IP: {ip}, Máscara: {mask}")
                print("  VLANs:")
                for vlan, numero in dispositivo.vlans.items():
                    print(f"    - {vlan}: {numero}")
                print(f"  Servicios: {', '.join(dispositivo.servicios)}")
                print("  " + "-" * 30)
        input("Presione Enter para continuar.")

    def borrar_dispositivo(self, nombre_campus):
        """Elimina un dispositivo existente de un campus."""
        nombre_dispositivo = input("Ingrese el nombre del dispositivo que desea borrar: ")
        for dispositivo in self.campus[nombre_campus].dispositivos:
            if dispositivo.nombre == nombre_dispositivo:
                self.campus[nombre_campus].dispositivos.remove(dispositivo)
                print("Dispositivo eliminado.")
                input("Presione Enter para continuar.")
                return
        print("Dispositivo no encontrado.")
        input("Presione Enter para continuar.")

if __name__ == "__main__":
    administrador = AdministradorRedes("datos_redes.json")
    administrador.menu_principal()
