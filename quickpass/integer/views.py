import csv
from datetime import datetime, timedelta, timezone
from json import dumps
import re
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views import View
from db_con import db
from django.contrib import messages as django_messages
from .models import UserModel, Casetas


def auth_view(request):

    if 'user_id' in request.session:
        return redirect('admin_dashboard')

    if request.method == "POST":
        if "login_submit" in request.POST:  # Inicio de sesión
            email = request.POST.get("email").strip()
            password = request.POST.get("password")

            user = UserModel.check_credentials(email, password)

            if user:
                request.session["user_id"] = str(user["_id"])
                request.session["name"] = user["name"]
                
                django_messages.success(request, f"Bienvenido {user['name']}!")
                return redirect('admin_dashboard')
            else:
                django_messages.error(request, "Credenciales incorrectas.")


        elif "register_submit" in request.POST:  # Registro
            name = request.POST.get("name").strip()
            lastname = request.POST.get("lastname").strip()
            email = request.POST.get("email").strip()
            location = request.POST.get("location").strip()
            phone = request.POST.get("phone").strip()
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")

            # Validaciones
            if not name or not email or not password:
                django_messages.error(request, "Todos los campos son obligatorios.")
            elif UserModel.get_user_by_email(email):
                django_messages.error(request, "El correo ya está registrado.")
            elif password != confirm_password:
                django_messages.error(request, "Las contraseñas no coinciden.")
            elif len(password) < 6:
                django_messages.error(request, "La contraseña debe tener al menos 6 caracteres.")
            else:
            
                try:
                    user = UserModel(name, email, lastname, location, phone, password)
                    user.save()
                    django_messages.success(request, "Registro exitoso, ahora inicia sesión.")
                    return redirect("login")
                except Exception as e:
                    django_messages.error(request, f"Error al guardar el usuario: {e}")

    return render(request, "login.html")  # Renderizar plantilla de login con mensajes

def logout_view(request):
    """Cierra la sesión del usuario."""
    if 'user_id' in request.session:
        request.session.flush()
        request.session.clear_expired()

    django_messages.success(request, "Sesión cerrada con éxito.")
    
    return redirect("start")

def home_view(request):
    return render(request, "home.html")


def start_view(request):
    return render(request, "start.html")

def profile_view(request):
    return render(request, "profile.html")

def profile_admin_view(request):
    if request.method == "POST" and "caseta_submit" in request.POST:
        numCaseta = request.POST.get("numCaseta", "").strip()
        ubicacion = request.POST.get("ubicacion", "").strip()
        estado = request.POST.get("estado", "").strip()
        celCaseta = request.POST.get("celCaseta", "").strip()
        encargado = request.POST.get("encargado", "").strip()
        controlE = request.POST.get("controlE", "").strip()
        
        try:
            caseta = Casetas(numCaseta, ubicacion, estado, encargado, celCaseta, controlE)
            caseta.save()
            
            # Guardar los datos en la sesión
            request.session['numCaseta'] = numCaseta
            request.session['ubicacion'] = ubicacion
            request.session['estado'] = estado
            request.session['celCaseta'] = celCaseta
            request.session['encargado'] = encargado
            request.session['controlE'] = controlE
            
            django_messages.success(request, "Registro de caseta exitoso")
            return redirect("profile_admin")
        except Exception as e:
            django_messages.error(request, f"Error al guardar la caseta: {e}")

    if request.method == "POST" and "actual_submit" in request.POST:
        # Obtener los datos del formulario
        name = request.POST.get("name", "").strip()
        lastname = request.POST.get("lastname", "").strip()
        puesto = request.POST.get("puesto", "").strip()
        language = request.POST.get("language", "").strip()
        
        # Obtener el email del usuario actual de la sesión
        email = request.session.get("email")
        
        if not email:
            django_messages.error(request, "No se pudo identificar el usuario. Por favor, inicie sesión nuevamente.")
            return redirect("login")  # Redirigir a la página de login
        
        try:
            # Crear diccionario con los datos a actualizar
            updated_data = {
                "name": name,
                "lastname": lastname,
                "puesto": puesto,
                "language": language
            }
            
            # Actualizar el usuario en la base de datos
            UserModel.update_user(email, updated_data)
            
            # Actualizar los datos en la sesión
            request.session["name"] = name
            request.session["lastname"] = lastname
            request.session["puesto"] = puesto
            request.session["language"] = language
            
            django_messages.success(request, "Perfil actualizado exitosamente")
            return redirect("profile")  # Redirigir a la misma página de perfil
            
        except Exception as e:
            django_messages.error(request, f"Error al actualizar el perfil: {e}")
    
    return render(request, "profile_admin.html")

def about_us_view(request):
    return render(request, "about_us.html")

# En views.py
# En views.py
from .models import AccesosStats

def admin_dashboard_view(request):
    # Obtener el número de caseta desde la sesión
    caseta_num = request.session.get('numCaseta')
    
    # Crear instancia de la clase de estadísticas
    stats = AccesosStats(caseta_num)
    
    # Verificar datos para diagnóstico
    info_datos = stats.verificar_datos()
    print(f"Información de datos: {info_datos}")
    
    # Obtener estadísticas actualizadas con ingresos
    estadisticas = stats.obtener_estadisticas()
    
    # Crear contexto para la plantilla incluyendo ingresos
    context = {
        'accesos_hoy': estadisticas['accesos_hoy'],
        'accesos_mes': estadisticas['accesos_mes'],
        'accesos_denegados_dia': estadisticas['accesos_denegados_dia'],
        'accesos_denegados_mes': estadisticas['accesos_denegados_mes'],
        'ingresos_hoy': estadisticas['ingresos_hoy'],
        'ingresos_mes': estadisticas['ingresos_mes'],
        'precio_auto': stats.precio_auto,  # Pasar el precio del auto a la plantilla
        'info_debug': info_datos  # Opcional: puedes mostrarlo en desarrollo
    }
    
    return render(request, "admin_dashboard.html", context)

class AccessReportView(View):
    """Vista para generar y descargar un informe de accesos del último mes."""
    
    def get(self, request):
        try:

            collection = AccesosStats
            # Calcular fecha de hace un mes
            one_month_ago = datetime.now() - timedelta(days=30)
            
            # Consulta a MongoDB para obtener los registros del último mes
            access_logs = list(collection.find({
                "timestamp": {"$gte": one_month_ago}
            }).sort("timestamp", -1))
            
            # Generar el informe
            report = {
                "generatedAt": datetime.now().isoformat(),
                "period": {
                    "from": one_month_ago.isoformat(),
                    "to": datetime.now().isoformat()
                },
                "totalAccessCount": len(access_logs),
                "accessLogs": access_logs
            }
            
            # Convertir a JSON (usando bson.json_util.dumps para manejar tipos de MongoDB)
            json_report = dumps(report, indent=2)
            
            # Crear respuesta para descarga
            response = HttpResponse(json_report, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="access-report.json"'
            
            return response
            
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


from django.http import FileResponse
from django.conf import settings
import os

def download_apk(request):
    apk_path = os.path.join(settings.MEDIA_ROOT, 'apps', 'quickpass.apk')
    response = FileResponse(open(apk_path, 'rb'))
    response['Content-Disposition'] = 'attachment; filename="quickpass.apk"'
    return response

def about_view(request):
    return render(request, "about.html")

def casetas_list_view(request):
    """Vista para mostrar y seleccionar casetas disponibles."""
    
    # Verificar si el usuario está autenticado
    if 'user_id' not in request.session:
        django_messages.error(request, "Debe iniciar sesión para acceder a esta página.")
        return redirect('login')
    
    # Obtener todas las casetas
    try:
        casetas = Casetas.get_all_casetas()
    except Exception as e:
        casetas = []
        django_messages.error(request, f"Error al obtener las casetas: {e}")
    
    # Manejar la selección de caseta
    if request.method == "POST" and "seleccionar_caseta" in request.POST:
        numCaseta = request.POST.get("numCaseta")
        try:
            # Obtener los datos de la caseta seleccionada
            caseta = Casetas.get_caseta_by_num(numCaseta)
            if not caseta:
                django_messages.error(request, "La caseta seleccionada no existe.")
                return redirect('casetas_list')
            
            # Activar la caseta y asociarla al usuario actual
            Casetas.activar_caseta(numCaseta, request.session["user_id"])
            
            # Guardar los datos en la sesión
            for key, value in caseta.items():
                request.session[key] = value
            
            django_messages.success(request, f"Caseta #{numCaseta} seleccionada con éxito.")
            return redirect('admin_dashboard')
        except Exception as e:
            django_messages.error(request, f"Error al seleccionar la caseta: {e}")
    
    # Renderizar la plantilla con las casetas
    return render(request, "casetas_list.html", {"casetas": casetas})

