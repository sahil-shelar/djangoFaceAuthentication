from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.register,name="register"),
    path("authenticate",views.authenticate,name="authenticate")
]