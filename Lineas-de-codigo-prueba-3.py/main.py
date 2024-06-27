from administrador_redes import AdministradorRedes

if __name__ == "__main__":
    archivo_datos = "datos_red.json"
    admin_redes = AdministradorRedes(archivo_datos)
    admin_redes.menu_principal()
