from db_con import db
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime, timezone
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

# Conexión a la colección de usuarios en MongoDB
user_collection = db['encargados']
caseta_collection = db['casetas']
# encargados_collection = db['encargados']
accesos = db['accesos']

class UserModel:
    def __init__(self, name, email, lastname, location, phone, password):
        self.name = name
        self.lastname = lastname
        self.email = email
        self.location = location
        self.phone = phone
        self.password = make_password(password)

    def save(self):
        """Guarda el usuario en MongoDB."""
        try:
            validate_email(self.email)  # Validar email
            if user_collection.find_one({"email": self.email}):
                raise ValidationError("El correo ya está registrado.")

            user_collection.insert_one({
                "name": self.name,
                "lastname": self.lastname,
                "location": self.location,
                "phone": self.phone,
                "email": self.email,
                "password": self.password,
            })

        except Exception as e:
            raise Exception(f"Error al guardar el usuario en MongoDB: {e}")
    
    @staticmethod
    def update_user(email, updated_data):
        """Actualiza el usuario en MongoDB."""
        try:
            # Filtro para encontrar al usuario por email
            filter_query = {"email": email}
            
            # Datos a actualizar
            update_query = {"$set": updated_data}
            
            # Actualizar el documento
            result = user_collection.update_one(filter_query, update_query)
            
            if result.matched_count == 0:
                raise Exception("Usuario no encontrado")
                
            return result.modified_count > 0
        except Exception as e:
            raise Exception(f"Error al actualizar el usuario en MongoDB: {e}")
        


    @staticmethod
    def get_user_by_email(email):
        """Busca un usuario por email."""
        return user_collection.find_one({"email": email})

    @staticmethod
    def check_credentials(email, password):
        """Verifica si las credenciales son correctas."""
        user = UserModel.get_user_by_email(email)
        if user and check_password(password, user["password"]):
             return user
        return None

class Casetas:
    def __init__(self, numCaseta, ubicacion, estado, encargado, celCaseta, controlE):
        self.numCaseta = numCaseta
        self.ubicacion = ubicacion
        self.estado = estado
        self.encargado = encargado
        self.celCaseta = celCaseta
        self.controlE = controlE

    def save(self):
        """Guarda la caseta en MongoDB."""
        try:
            if caseta_collection.find_one({"numCaseta": self.numCaseta}):
                raise ValidationError("La caseta ya está registrada.")
            caseta_collection.insert_one({
                "numCaseta": self.numCaseta,
                "ubicacion": self.ubicacion,
                "estado": self.estado,
                "encargado": self.encargado,
                "celCaseta": self.celCaseta,
                "controlE": self.controlE
            }) 
            
        except Exception as e:
            raise Exception(f"Error al guardar la caseta en MongoDB: {e}")
    
    @staticmethod
    def get_all_casetas():
        """Obtiene todas las casetas disponibles de la base de datos."""
        try:
            casetas = list(caseta_collection.find({}, {'_id': 0}))
            return casetas
        except Exception as e:
            raise Exception(f"Error al obtener las casetas de MongoDB: {e}")
    
    @staticmethod
    def get_caseta_by_num(numCaseta):
        """Obtiene una caseta específica por su número."""
        try:
            caseta = caseta_collection.find_one({"numCaseta": numCaseta}, {'_id': 0})
            return caseta
        except Exception as e:
            raise Exception(f"Error al obtener la caseta de MongoDB: {e}")
    
    @staticmethod
    def activar_caseta(numCaseta, user_id):
        """Actualiza el estado de la caseta a 'Activa' y la asocia con un usuario."""
        try:
            caseta_collection.update_one(
                {"numCaseta": numCaseta},
                {"$set": {"estado": "Activa", "active_user_id": user_id}}
            )
            return True
        except Exception as e:
            raise Exception(f"Error al activar la caseta: {e}")
        
class AccesosStats:
    def __init__(self, caseta_num=None):
        self.accesos_collection = db['accesos']
        self.caseta_num = caseta_num
        self.precio_auto = 120
    
    def _filtro_base(self):
        """Crea un filtro base según la caseta actual"""
        filtro = {"acceso_permitido": True}
        if self.caseta_num and self.caseta_num != "":
            filtro["numCaseta"] = self.caseta_num
        return filtro
    
    def contar_accesos_hoy(self):
        """Cuenta los accesos del día actual"""
        # Usa UTC para asegurar consistencia con MongoDB
        hoy = datetime.now(timezone.utc)
        inicio_dia = datetime(hoy.year, hoy.month, hoy.day, 0, 0, 0, tzinfo=timezone.utc)
        fin_dia = datetime(hoy.year, hoy.month, hoy.day, 23, 59, 59, 999999, tzinfo=timezone.utc)
        
        filtro = self._filtro_base()
        filtro["fecha_acceso"] = {
            "$gte": inicio_dia,
            "$lte": fin_dia
        }
        
        # Debug: imprimir el filtro y verificar que funciona
        print(f"Filtro día: {filtro}")
        resultados = list(self.accesos_collection.find(filtro))
        print(f"Encontrados hoy: {len(resultados)}")
        
        return len(resultados)
    
    def contar_accesos_mes(self):
        """Cuenta los accesos del mes actual"""
        hoy = datetime.now(timezone.utc)
        inicio_mes = datetime(hoy.year, hoy.month, 1, 0, 0, 0, tzinfo=timezone.utc)
        
        # Si estamos en diciembre, el siguiente mes es enero del próximo año
        if hoy.month == 12:
            fin_mes = datetime(hoy.year + 1, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        else:
            fin_mes = datetime(hoy.year, hoy.month + 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        
        filtro = self._filtro_base()
        filtro["fecha_acceso"] = {
            "$gte": inicio_mes,
            "$lt": fin_mes
        }
        
        # Debug: imprimir el filtro y verificar que funciona
        print(f"Filtro mes: {filtro}")
        resultados = list(self.accesos_collection.find(filtro))
        print(f"Encontrados mes: {len(resultados)}")
        
        return len(resultados)
    
    def _filtro_base_denegado(self):
        """Crea un filtro base según la caseta actual"""
        filtro = {"acceso_permitido": False}
        if self.caseta_num and self.caseta_num != "":
            filtro["numCaseta"] = self.caseta_num
        return filtro
    
    def contar_accesos_denegados_dia(self):
        """Cuenta los accesos del día actual"""
        # Usa UTC para asegurar consistencia con MongoDB
        hoy = datetime.now(timezone.utc)
        inicio_dia = datetime(hoy.year, hoy.month, hoy.day, 0, 0, 0, tzinfo=timezone.utc)
        fin_dia = datetime(hoy.year, hoy.month, hoy.day, 23, 59, 59, 999999, tzinfo=timezone.utc)
        
        filtro = self._filtro_base_denegado()
        filtro["fecha_acceso"] = {
            "$gte": inicio_dia,
            "$lte": fin_dia
        }
        
        # Debug: imprimir el filtro y verificar que funciona
        print(f"Filtro día: {filtro}")
        resultados = list(self.accesos_collection.find(filtro))
        print(f"Encontrados hoy: {len(resultados)}")
        
        return len(resultados)
    
    def contar_accesos_denegados_mes(self):
        """Cuenta los accesos del mes actual"""
        hoy = datetime.now(timezone.utc)
        inicio_mes = datetime(hoy.year, hoy.month, 1, 0, 0, 0, tzinfo=timezone.utc)
        
        # Si estamos en diciembre, el siguiente mes es enero del próximo año
        if hoy.month == 12:
            fin_mes = datetime(hoy.year + 1, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        else:
            fin_mes = datetime(hoy.year, hoy.month + 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        
        filtro = self._filtro_base_denegado()
        filtro["fecha_acceso"] = {
            "$gte": inicio_mes,
            "$lt": fin_mes
        }
        
        # Debug: imprimir el filtro y verificar que funciona
        print(f"Filtro mes: {filtro}")
        resultados = list(self.accesos_collection.find(filtro))
        print(f"Encontrados mes: {len(resultados)}")
        
        return len(resultados)

    def calcular_ingresos_hoy(self):
        """Calcula los ingresos del día actual basado en accesos permitidos"""
        accesos_hoy = self.contar_accesos_hoy()
        return accesos_hoy * self.precio_auto
    
    def calcular_ingresos_mes(self):
        """Calcula los ingresos del mes actual basado en accesos permitidos"""
        accesos_mes = self.contar_accesos_mes()
        return accesos_mes * self.precio_auto
    
    def obtener_estadisticas(self):
        """Retorna un diccionario con todas las estadísticas"""
        accesos_hoy = self.contar_accesos_hoy()
        accesos_mes = self.contar_accesos_mes()

        return {
            "accesos_hoy": self.contar_accesos_hoy(),
            "accesos_mes": self.contar_accesos_mes(),
            "accesos_denegados_dia": self.contar_accesos_denegados_dia(),
            "accesos_denegados_mes": self.contar_accesos_denegados_mes(),
            "ingresos_hoy": accesos_hoy * self.precio_auto,
            "ingresos_mes": accesos_mes * self.precio_auto
        }
    
    def verificar_datos(self):
        """Método de diagnóstico para verificar los datos en la colección"""
        # Contar todos los registros
        total = self.accesos_collection.count_documents({})
        
        # Contar registros con acceso permitido
        permitidos = self.accesos_collection.count_documents({"acceso_permitido": True})
        
        # Obtener rango de fechas
        primer_registro = self.accesos_collection.find_one({}, sort=[("fecha_acceso", 1)])
        ultimo_registro = self.accesos_collection.find_one({}, sort=[("fecha_acceso", -1)])
        
        primera_fecha = primer_registro.get("fecha_acceso") if primer_registro else "No hay registros"
        ultima_fecha = ultimo_registro.get("fecha_acceso") if ultimo_registro else "No hay registros"
        
        return {
            "total_registros": total,
            "accesos_permitidos": permitidos,
            "primera_fecha": primera_fecha,
            "ultima_fecha": ultima_fecha,   
        }
    
    