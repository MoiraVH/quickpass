from django.shortcuts import redirect
from django.contrib import messages

class AuthRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs que no requieren autenticación
        exempt_urls = ['/login/', '/register/', '/about-us/', '/']
        
        # Verificar si la URL actual requiere autenticación
        if request.path_info not in exempt_urls and 'user_id' not in request.session:
            messages.error(request, "Debes iniciar sesión para acceder a esta página.")
            return redirect('login')
            
        response = self.get_response(request)
        return response