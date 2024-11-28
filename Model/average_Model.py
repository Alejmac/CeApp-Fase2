import json
import os

class AverageModel:
    def __init__(self):
        self.json_path = os.path.join(os.path.dirname(__file__), '..', 'Data', 'kardex.json')
        self.data = self.load_data()

    def load_data(self):
        if not os.path.exists(self.json_path):
            raise FileNotFoundError(f"El archivo {self.json_path} no existe.")
        
        with open(self.json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        return data

    def get_data(self):
        return self.data

# Ejemplo de uso
# if __name__ == "__main__":
#     model = AverageModel()
#     data = model.get_data()
#     print(data)