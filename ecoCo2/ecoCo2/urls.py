"""ecoCo2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from emissions import views as emissions_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("co2_rates/", emissions_views.co2_interpollated_view),
    path("co2_rates/seasonal/", emissions_views.co2_rate_seasonal_view),
    path("co2_rates/week/", emissions_views.co2_rate_day_of_week_view),
]
