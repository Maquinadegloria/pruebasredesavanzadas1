import os
import json
import re

class Campus:
    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion
        self.dispositivos = []

class Dispositivo:
    def __init__(self, nombre, modelo, capa, interfaces, ips_masks, vlans, servicios):
        self.nombre = nombre
        self.modelo = modelo
        self.capa = capa
        self.interfaces = interfaces
        self.ips_masks = ips_masks
        self.vlans = vlans
        self.servicios = servicios

def es_direccion_ipv4(direccion):
    patron_ipv4 = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return re.match(patron_ipv4, direccion) is not None

class AdministradorRedes:
    """
    Clase que representa un administrador de redes.

    Attributes:
        nombre_archivo (str): El nombre del archivo utilizado para cargar y guardar los datos.
        campus (dict): Un diccionario que almacena los campus y sus respectivos dispositivos.
    """

    def __init__(self, nombre_archivo):
        """
        Inicializa una instancia de la clase AdministradorRedes.

        Args:
            nombre_archivo (str): El nombre del archivo utilizado para cargar y guardar los datos.
        """
        self.nombre_archivo = nombre_archivo
        self.campus = {}
        if os.path.exists(nombre_archivo):
            self.cargar_desde_archivo()

    def cargar_desde_archivo(self):
        """
        Carga los datos desde un archivo JSON y los almacena en la instancia de la clase.
        """
        with open(self.nombre_archivo, "r") as archivo:
            datos = json.load(archivo)
            for nombre, descripcion in datos["campus"].items():
                campus = Campus(nombre, descripcion)
                self.campus[nombre] = campus

                dispositivos_info = datos.get(nombre, [])
                for dispositivo_info in dispositivos_info:
                    dispositivo = Dispositivo(**dispositivo_info)
                    campus.dispositivos.append(dispositivo)

    def guardar_en_archivo(self):
        """
        Guarda los datos de la instancia de la clase en un archivo JSON.
        """
        datos = {"campus": {}, "dispositivos": {}}
        for nombre, campus in self.campus.items():
            datos["campus"][nombre] = campus.descripcion
            datos[nombre] = []
            for dispositivo in campus.dispositivos:
                datos[nombre].append(dispositivo.__dict__)

        with open(self.nombre_archivo, "w") as archivo:
            json.dump(datos, archivo, indent=4)

    def interpretar_json_y_guardar_texto(self, archivo_texto):
        """
        Interpreta los datos de un archivo JSON, los convierte a formato de texto y los guarda en un archivo.

        Args:
            archivo_texto (str): El nombre del archivo de texto en el que se guardarán los datos convertidos.
        """
        if os.path.exists(self.nombre_archivo):
            with open(self.nombre_archivo, "r") as archivo:
                datos = json.load(archivo)
                for nombre, descripcion in datos["campus"].items():
                    campus = Campus(nombre, descripcion)
                    self.campus[nombre] = campus

                    dispositivos_info = datos.get(nombre, [])
                    for dispositivo_info in dispositivos_info:
                        dispositivo = Dispositivo(**dispositivo_info)
                        campus.dispositivos.append(dispositivo)

            texto_formato = self.convertir_a_formato_texto()
            with open(archivo_texto, "w") as archivo_texto:
                archivo_texto.write(texto_formato)
            print(f"Datos convertidos y guardados en el archivo: {archivo_texto}")

    def convertir_a_formato_texto(self):
        """
        Convierte los datos de la instancia de la clase a formato de texto.

        Returns:
            str: Los datos convertidos en formato de texto.
        """
        texto_formato = ""
        for nombre, campus in self.campus.items():
            texto_formato += f"Campus: {nombre}\nDescripción: {campus.descripcion}\n"
            for dispositivo in campus.dispositivos:
                texto_formato += f"\nDispositivo: {dispositivo.nombre}\n"
                texto_formato += f"Modelo: {dispositivo.modelo}\n"
                texto_formato += f"Capa: {dispositivo.capa}\n"
                texto_formato += "Interfaces:\n"
                for interface in dispositivo.interfaces:
                    ip, mask = dispositivo.ips_masks.get(interface, ("", ""))
                    texto_formato += f"- {interface}: IP: {ip}, Máscara: {mask}\n"
                texto_formato += "VLANs:\n"
                for vlan, numero in dispositivo.vlans.items():
                    texto_formato += f"- {vlan}: {numero}\n"
                texto_formato += f"Servicios: {', '.join(dispositivo.servicios)}\n"
                texto_formato += "-" * 30 + "\n"
        return texto_formato

    def menu_principal(self):
        """
        Muestra el menú principal y permite al usuario seleccionar una opción.
        """
        while True:
            os.system("clear")
            print("¡Bienvenido al Administrador de Redes!")
            print("1. Administrar campus")
            print("2. Administrar dispositivos de red")
            print("3. Guardar información en archivo de texto")
            print("4. Interpretar archivo JSON, convertir a formato de texto y guardar")
            print("5. Salir")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                self.administrar_campus()
            elif opcion == "2":
                self.administrar_dispositivos()
            elif opcion == "3":
                self.guardar_en_archivo()
            elif opcion == "4":
                archivo_texto = input("Ingrese el nombre del archivo de texto para guardar los datos: ")
                self.interpretar_json_y_guardar_texto(archivo_texto)
                input("Presione Enter para continuar.")
            elif opcion == "5":
                print("¡Hasta luego!")
                break
            else:
                input("Opción no válida. Presione Enter para continuar.")

    def administrar_campus(self):
        """
        Muestra el menú de administración de campus y permite al usuario seleccionar una opción.
        """
        while True:
            os.system("clear")
            print("Campus:")
            for nombre in sorted(self.campus.keys()):
                print(nombre)
            opcion = input("Seleccione una opción:\n1. Agregar campus\n2. Modificar campus\n3. Borrar campus\n4. Volver al menú principal\n")
            if opcion == "1":
                self.agregar_campus()
            elif opcion == "2":
                self.modificar_campus()
            elif opcion == "3":
                self.borrar_campus()
            elif opcion == "4":
                break
            else:
                input("Opción no válida. Presione Enter para continuar.")

    def agregar_campus(self):
        """
        Agrega un nuevo campus a la instancia de la clase.
        """
        nombre = input("Ingrese el nombre del campus: ")
        descripcion = input("Ingrese una descripción del campus: ")
        self.campus[nombre] = Campus(nombre, descripcion)
        input("Campus agregado. Presione Enter para continuar.")

    def modificar_campus(self):
        """
        Modifica la descripción de un campus existente en la instancia de la clase.
        """
        nombre = input("Ingrese el nombre del campus que desea modificar: ")
        if nombre in self.campus:
            nueva_descripcion = input("Ingrese la nueva descripción del campus: ")
            self.campus[nombre].descripcion = nueva_descripcion
            input("Campus modificado. Presione Enter para continuar.")
        else:
            input("El campus especificado no existe. Presione Enter para continuar.")

    def borrar_campus(self):
        """
        Elimina un campus existente de la instancia de la clase.
        """
        nombre = input("Ingrese el nombre del campus que desea borrar: ")
        if nombre in self.campus:
            del self.campus[nombre]
            input("Campus eliminado. Presione Enter para continuar.")
        else:
            input("El campus especificado no existe. Presione Enter para continuar.")

    def administrar_dispositivos(self):
        """
        Muestra el menú de administración de dispositivos y permite al usuario seleccionar una opción.
        """
        while True:
            os.system("clear")
            print("Campus disponibles:")
            for nombre, campus in self.campus.items():
                print(f"{nombre}: {campus.descripcion}")
            campus_seleccionado = input("Ingrese el nombre del campus en el que desea agregar dispositivos (o 'fin' para salir): ")
            if campus_seleccionado.lower() == "fin":
                break
            elif campus_seleccionado in self.campus:
                self.agregar_dispositivos(campus_seleccionado)
            else:
                print("El campus especificado no existe.") 

    def agregar_dispositivos(self, nombre_campus):
        """
        Agrega dispositivos a un campus existente en la instancia de la clase.

        Args:
            nombre_campus (str): El nombre del campus al que se agregarán los dispositivos.
        """
        os.system("clear")
        dispositivos_nuevos = []
        while True:
            nombre = input("Ingrese el nombre del dispositivo (o 'fin' para salir): ")
            if nombre.lower() == "fin":
                break
            modelo = input("Ingrese el modelo del dispositivo: ")
            capa = self.seleccionar_capa()
            interfaces = input("Ingrese las interfaces de red del dispositivo (separadas por coma): ").split(",")
            ips_masks = self.ingresar_ips_masks(interfaces)
            vlans = self.ingresar_vlans()
            servicios = input("Ingrese los servicios de red configurados (separados por coma): ").split(",")

            dispositivo = Dispositivo(nombre, modelo, capa, interfaces, ips_masks, vlans, servicios)
            dispositivos_nuevos.append(dispositivo)
        
        self.campus[nombre_campus].dispositivos.extend(dispositivos_nuevos)
        print("Dispositivos agregados.")

    def seleccionar_capa(self):
        """
        Muestra el menú de selección de capa y permite al usuario seleccionar una opción.

        Returns:
            str: La capa seleccionada.
        """
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
            return "Desconocida"

    def ingresar_ips_masks(self, interfaces):
        """
        Solicita al usuario ingresar las direcciones IP y máscaras de red para las interfaces de un dispositivo.

        Args:
            interfaces (list): Una lista de las interfaces del dispositivo.

        Returns:
            dict: Un diccionario que mapea cada interfaz con su dirección IP y máscara de red correspondientes.
        """
        ips_masks = {}
        for interfaz in interfaces:
            while True:
                ip = input(f"Ingrese la dirección IP para la interfaz {interfaz}: ")
                mask = input(f"Ingrese la máscara de red para la interfaz {interfaz}: ")
                if es_direccion_ipv4(ip):
                    ips_masks[interfaz] = (ip, mask)
                    break
                else:
                    print("La dirección IP ingresada no es válida. Inténtelo nuevamente.")
        return ips_masks

    def ingresar_vlans(self):
        """
        Solicita al usuario ingresar los nombres y números de VLAN para un dispositivo.

        Returns:
            dict: Un diccionario que mapea cada nombre de VLAN con su número correspondiente.
        """
        vlans = {}
        while True:
            nombre_vlan = input("Ingrese el nombre de la VLAN (o 'fin' para terminar): ")
            if nombre_vlan.lower() == 'fin':
                break
            numero_vlan = input("Ingrese el número de la VLAN: ")
            vlans[nombre_vlan] = numero_vlan
        return vlans

if __name__ == "__main__":
    nombre_archivo = input("Ingrese el nombre del archivo para cargar o crear la información: ")
    administrador = AdministradorRedes(nombre_archivo)
    administrador.menu_principal()
