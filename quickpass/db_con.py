from pymongo import MongoClient
from pymongo.server_api import ServerApi  # Asegúrate de que esta línea no cause error

# Conexión a MongoDB Atlas
client = MongoClient(
    "mongodb+srv://lgaxiola117:H4QJA8wJDY1BPCXo@quickpass.3zpme.mongodb.net/?retryWrites=true&w=majority",
    server_api=ServerApi('1')  # Usa la API correcta
)

db = client["users"]
