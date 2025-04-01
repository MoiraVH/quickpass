"""
URL configuration for quickpass project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from integer.views import AccessReportView, about_us_view, about_view, admin_dashboard_view, home_view, auth_view, logout_view, profile_admin_view, profile_view, start_view
from integer import views

urlpatterns = [
    path('', start_view, name='root'),
    path('admin/', admin.site.urls),
    path('login/', auth_view, name='login'),  # ✅ Maneja login y registro
    path('logout/', logout_view, name='logout'),
    path('start/', start_view, name='start'),
    path('home/', home_view, name='home'),
    path('profile/', profile_view, name='profile'),
    path('profile_admin/', profile_admin_view, name='profile_admin'),
    path('about_us/', about_us_view, name='about_us'), 
    path('admin_dashboard/', admin_dashboard_view, name='admin_dashboard'),
    path('api/access-report/', AccessReportView.as_view(), name='access_report'),
    path('about/', about_view, name='about'),
     path('casetas/', views.casetas_list_view, name='casetas_list'),
]