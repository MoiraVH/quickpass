from django.shortcuts import redirect
from functools import wraps

def role_required(*roles):
    """Decorador para restringir el acceso a usuarios con ciertos roles."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if "role" in request.session and request.session["role"] in roles:
                return view_func(request, *args, **kwargs)
            else:
                return redirect("unauthorized")  # Redirigir si no tiene permisos
        return wrapper
    return decorator
