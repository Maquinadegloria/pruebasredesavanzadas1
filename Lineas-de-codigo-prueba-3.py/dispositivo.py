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
