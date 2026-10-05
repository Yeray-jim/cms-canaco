from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path("", views.index, name="index"),
    path("", views.base, name="base"),
    path("", views.categorias, name="categorias"),
    path("", views.contactanos,  name="contactanos"),
    path("", views.crear_publicacion, name="crear_publicacion"),
    path("", views.crear_usuario, name="crear_usuario"),
    path("", views.crud_cambiar_contrasena, name="crud_cambiar_contrasena"),
    path("", views.crud_categorias, name="crud_categorias"),
    path("", views.crud_comentarios, name="crud_comentarios"),
    path("", views.crud_noticias, name="crud_noticias"),
    path("", views.crud_perfil, name="crud_perfil"),
    path("", views.crud_usuarios, name="crud_usuarios"),
    path("", views.editar_categorias, name="editar_categorias"),
    path("", views.login, name="login"),
    path("", views.noticia, name="noticia"),
    path("", views.perfil, name="pefil"),
    path("", views.sign_up, name="sign_up")
]