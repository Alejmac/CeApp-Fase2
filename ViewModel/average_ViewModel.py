from Model.average_Model import AverageModel

class AverageViewModel:
    def __init__(self):
        # Crear una instancia del modelo
        self.model = AverageModel()
        # Cargar los datos del modelo
        self.data = self.model.get_data()

    def get_promedios(self):
        promedios = []
        for nivel, contenido in self.data.items():
            if nivel != "promedio_general":  # Ignorar el promedio general
                promedios.append(contenido["promedio"])
        return promedios

    def get_promedio_general(self):
        return self.data.get("promedio_general", 0)

 