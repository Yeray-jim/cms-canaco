from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path("", views.index, name="index"),
    path("", views.base, name="base"),
    path("categoria/", views.categoria, name="categoria"),
    path("", views.contactanos,  name="contactanos"),
    path("crear_publicacion/", views.crear_publicacion, name="crear_publicacion"),
    path("crear_usuario/", views.crear_usuario, name="crear_usuario"),
    path("crud_cambiar_contraseña", views.crud_cambiar_contrasena, name="crud_cambiar_contrasena"),
    path("crud_categorias/", views.crud_categorias, name="crud_categorias"),
    path("crud_comentarios/", views.crud_comentarios, name="crud_comentarios"),
    path("crud_noticias/", views.crud_noticias, name="crud_noticias"),
    path("crud_perfil/", views.crud_perfil, name="crud_perfil"),
    path("crud_usuarios/", views.crud_usuarios, name="crud_usuarios"),
    path("", views.editar_categorias, name="editar_categorias"),
    path("login/", views.login, name="login"),
    path("noticia/", views.noticia, name="noticia"),
    path("perfil/", views.perfil, name="perfil"),
    path("sign_up/", views.sign_up, name="sign_up")
]