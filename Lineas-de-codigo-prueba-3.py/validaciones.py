import re
import ipaddress

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
