from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = "catalogo"
urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("registro/", views.registro, name="registro"),
    path("ingresar/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="iniciar_sesion"),
    path("salir/", auth_views.LogoutView.as_view(), name="salir"),
    path("favoritos/", views.favoritos, name="favoritos"),
    path("productos/<slug:slug>/favorito/", views.alternar_favorito, name="alternar_favorito"),
    path("productos/<slug:slug>/", views.detalle_producto, name="detalle_producto"),
]
