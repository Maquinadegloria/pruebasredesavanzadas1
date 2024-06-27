class Campus:
    """Representa un campus con una descripción y una lista de dispositivos."""
    def __init__(self, nombre, descripcion):
        self.nombre = nombre  # Nombre del campus
        self.descripcion = descripcion  # Descripción del campus
        self.dispositivos = []  # Lista de dispositivos en el campus
