# LABORATORIO DE DESARROLLO WEB DJANGO (TecNM)
## Guía Integrada: Laboratorios 11, 12 y 13

---

# LABORATORIO 11: Operaciones CRUD de Noticias, Comentarios y Categorías

**Objetivo:** Desarrollar la funcionalidad de los módulos de noticias, comentarios y categorías en Django.  
**Recursos:** Visual Studio Code.  
**Nivel:** Básico.  
**Tiempo estimado:** 30 minutos.

---

## Tarea 1: Crear el módulo dinámico de CRUD Categorías

### Paso 1.- Modificar `canaco/home/views.py` (método `crud_categorias`)
Sustituye la vista `crud_categorias` con el siguiente código para guardar las categorías en la base de datos:

```python
@operador_required
def crud_categorias(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        if nombre:
            Categoria.objects.create(nombre=nombre, fk_user=request.user)
            messages.success(request, 'Categoría agregada correctamente.')
            return redirect('home:crud_categorias')
    categorias = Categoria.objects.all().order_by('-createdat')
    return render(request, 'home/crud_categorias.html', {'categorias': categorias})
```

### Paso 2.- Agregar rutas en `canaco/home/urls.py`
Añade las siguientes rutas al arreglo `urlpatterns`:

```python
path("crud_categorias/<int:pk>/editar", views.editar_categoria, name="editar_categoria"),
path("crud_categorias/<int:pk>/eliminar", views.eliminar_categoria, name="eliminar_categoria"),
```

### Paso 3.- Agregar o modificar vistas de editar y eliminar en `canaco/home/views.py`
Añade las funciones `editar_categoria` y `eliminar_categoria`:

```python
@operador_required
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        if nombre:
            categoria.nombre = nombre
            categoria.save()
            messages.success(request, 'Categoría actualizada correctamente.')
            return redirect('home:crud_categorias')
    return render(request, 'home/editar_categoria.html', {'categoria': categoria})

@operador_required
def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada correctamente.')
        return redirect('home:crud_categorias')
```

### Paso 4.- Probar en el servidor web
Levanta el servidor web (`python manage.py runserver`) y añade categorías (ejemplo: "Tecnología", "Educación").

### Paso 5.- Crear/Modificar la plantilla `canaco/home/templates/home/editar_categoria.html`

```html
{% extends 'partials/sidebar_base.html' %}
{% load static %}
{% block title %}Editar Categoria{% endblock %}
{% block content %}
<div class="container mt-4">
  <div class="card shadow rounded">
    <div class="card-body">
      <h3 class="mb-4 text-center">Editar Categoría</h3>
      <form method="POST">
        {% csrf_token %}
        <div class="mb-3">
          <label for="nombre" class="form-label">Nombre</label>
          <input type="text" id="nombre" name="nombre" class="form-control" value="{{ categoria.nombre }}" required>
        </div>
        <div class="d-grid gap-2">
          <button type="submit" class="btn btn-primary">Guardar Cambios</button>
          <a href="{% url 'home:crud_categorias' %}" class="btn btn-outline-secondary">Cancelar</a>
        </div>
      </form>
    </div>
  </div>
</div>
{% endblock content %}
```

### Paso 6.- Probar edición de categorías
Ingresa al panel de administrar categorías y haz clic en el botón **EDITAR** para modificar un registro existente.

---

## Tarea 2: Crear el módulo de comentarios

### Paso 1.- Modificar `canaco/home/views.py` (método `crud_comentarios`)

```python
@operador_required
def crud_comentarios(request):
    comentarios = Comentario.objects.select_related('publicacion', 'user').order_by('-createdat')
    return render(request, 'home/crud_comentarios.html', {'comentarios': comentarios})
```

### Paso 2.- Agregar métodos de administración de comentarios en `canaco/home/views.py`
Añade los métodos `aprobar_comentario`, `bloquear_comentario` y `eliminar_comentario` debajo de `crud_comentarios`:

```python
@operador_required
def aprobar_comentario(request, pk):
    comentario = get_object_or_404(Comentario, pk=pk)
    comentario.estado = Comentario.ESTADO_APROBADO
    comentario.save()
    return redirect('home:crud_comentarios')

@operador_required
def bloquear_comentario(request, pk):
    comentario = get_object_or_404(Comentario, pk=pk)
    comentario.estado = Comentario.ESTADO_BLOQUEADO
    comentario.save()
    return redirect('home:crud_comentarios')

@operador_required
def eliminar_comentario(request, pk):
    comentario = get_object_or_404(Comentario, pk=pk)
    if request.method == 'POST':
        comentario.delete()
        return redirect('home:crud_comentarios')
```

### Paso 3.- Agregar rutas en `canaco/home/urls.py`

```python
path("crud_comentarios/<int:pk>/aprobar", views.aprobar_comentario, name="aprobar_comentario"),
path("crud_comentarios/<int:pk>/bloquear", views.bloquear_comentario, name="bloquear_comentario"),
path("crud_comentarios/<int:pk>/eliminar", views.eliminar_comentario, name="eliminar_comentario"),
```

> **Nota:** Las pruebas del módulo de comentarios se realizarán tras configurar la vista de detalle de noticias.

---

## Tarea 3: Crear el módulo de noticias (CRUD)

### Paso 1.- Modificar `canaco/home/templates/home/noticia.html`

```html
{% extends 'partials/base.html' %}
{% load static %}
{% block title %}{{ publicacion.titulo }}{% endblock %}
{% block content %}
<section class="section">
  <div class="container">
    {% if messages %}
      {% for message in messages %}
        <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
          {{ message }}
          <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Cerrar"></button>
        </div>
      {% endfor %}
    {% endif %}
    
    <div class="row blog-entries">
      <div class="col-md-12 col-lg-8 main-content">
        <h1 class="mb-4">{{ publicacion.titulo }}</h1>
        {% if publicacion.imagen_portada %}
          <img src="{{ publicacion.imagen_portada.display_url }}" alt="{{ publicacion.titulo }}" class="img-fluid rounded mb-4 publication-cover-image" style="max-height: 500px; width: 100%; object-fit: cover; object-position: center;">
        {% endif %}
        
        <div class="post-meta mb-4">
          <span>{{ publicacion.createdat|date:"d M Y H:i" }}</span>
          <span>&nbsp;-&nbsp; {% if publicacion.categoria %}{{ publicacion.categoria.nombre }}{% else %}Sin categoría{% endif %}</span>
          <span>&nbsp;-&nbsp; Visitas {{ publicacion.visitas }}</span>
        </div>

        <h3>Resumen de la noticia</h3>
        <p>{{ publicacion.resumen }}</p>

        <h3>Noticia</h3>
        <div class="post-content-body">
          {{ publicacion.contenido|safe }}
        </div>

        <h3 class="mt-5">Galería</h3>
        <div class="row my-4">
          {% for imagen in publicacion.galeria.all %}
            <div class="col-md-4 mb-4">
              <img src="{{ imagen.archivo.display_url }}" alt="Galería" class="img-fluid rounded publication-gallery-image" style="height: 250px; width: 100%; object-fit: cover; object-position: center;">
            </div>
          {% empty %}
            <div class="col-12"><p>Sin imágenes en galería.</p></div>
          {% endfor %}
        </div>

        <div class="pt-4 comment-wrap">
          <h3 class="mb-4">Comentarios</h3>
          {% for comentario in comentarios %}
            <div class="border-bottom pb-3 mb-3">
              <strong>{{ comentario.user.username }}</strong>
              <span class="text-muted">{{ comentario.createdat|date:"d M Y H:i" }}</span>
              <p class="mb-0">{{ comentario.contenido }}</p>
            </div>
          {% empty %}
            <p>No hay comentarios aprobados todavía.</p>
          {% endfor %}

          {% if request.user.is_authenticated %}
            <form method="POST" class="mt-4">
              {% csrf_token %}
              <div class="mb-3">
                <label for="contenido" class="form-label">Agregar comentario</label>
                <textarea name="contenido" id="contenido" rows="4" class="form-control" required></textarea>
              </div>
              <button type="submit" class="btn btn-primary">Agregar comentario</button>
            </form>
          {% else %}
            <a href="{% url 'home:login' %}" class="btn btn-primary mt-3">Inicia sesión para comentar</a>
          {% endif %}
        </div>
      </div>

      <!-- Sidebar -->
      <div class="col-md-12 col-lg-4 sidebar">
        <div class="sidebar-box">
          <h3 class="heading">Otras noticias</h3>
          <div class="post-entry-sidebar">
            <ul>
              {% for noticia in recientes %}
                <li>
                  <a href="{% url 'home:noticia_detalle' noticia.id %}">
                    {% if noticia.imagen_portada %}
                      <img src="{{ noticia.imagen_portada.display_url }}" alt="{{ noticia.titulo }}" class="me-4 rounded sidebar-post-image" style="width: 70px; height: 70px; object-fit: cover; object-position: center;">
                    {% endif %}
                    <div class="text">
                      <h4>{{ noticia.titulo }}</h4>
                      <div class="post-meta"><span>{{ noticia.createdat|date:"d M Y" }}</span></div>
                    </div>
                  </a>
                </li>
              {% endfor %}
            </ul>
          </div>
        </div>

        <div class="sidebar-box">
          <h3 class="heading">Categorías</h3>
          <ul class="categories">
            {% for categoria in categorias %}
              <li><a href="{% url 'home:categoria_detalle' categoria.id %}">{{ categoria.nombre }}</a></li>
            {% endfor %}
          </ul>
        </div>
      </div>

    </div>
  </div>
</section>
{% endblock content %}
```

### Paso 2.- Agregar rutas en `canaco/home/urls.py`

```python
path("noticia/<int:pk>", views.noticia, name="noticia_detalle"),
path("crud_noticias/<int:pk>/editar", views.editar_publicacion, name="editar_publicacion"),
path("crud_noticias/<int:pk>/publicar", views.publicar_publicacion, name="publicar_publicacion"),
path("crud_noticias/<int:pk>/eliminar", views.eliminar_publicacion, name="eliminar_publicacion"),
path("categoria/<int:pk>", views.categoria, name="categoria_detalle"),
```

### Paso 3.- Modificar en `canaco/home/views.py` la función `crud_noticias`

```python
@operador_required
def crud_noticias(request):
    publicaciones = Publicacion.objects.select_related('categoria', 'autor').order_by('-createdat')
    return render(request, 'home/crud_noticias.html', {'publicaciones': publicaciones})
```

### Paso 4.- Agregar las funciones de publicaciones en `canaco/home/views.py`

Asegúrate de importar `F` en la parte superior del archivo:
```python
from django.db.models import F
```

Añade las siguientes funciones:

```python
def noticia(request, pk=None):
    if pk and es_operador(request.user):
        qs = Publicacion.objects.all()
    else:
        qs = Publicacion.objects.filter(estado=Publicacion.ESTADO_PUBLICADO)
    
    qs = qs.select_related('categoria', 'autor', 'imagen_portada')
    publicacion = get_object_or_404(qs, pk=pk) if pk else qs.order_by('-createdat').first()
    
    if not publicacion:
        messages.info(request, 'Todavía no hay noticias publicadas.')
        return redirect('home:index')
    
    Publicacion.objects.filter(pk=publicacion.pk).update(visitas=F('visitas') + 1)
    publicacion.refresh_from_db()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para comentar.')
            return redirect('home:login')
        
        contenido = request.POST.get('contenido', '').strip()
        if contenido:
            Comentario.objects.create(
                publicacion=publicacion,
                user=request.user,
                contenido=contenido
            )
            messages.success(request, 'Comentario enviado. Será visible cuando lo apruebe el administrador.')
            return redirect('home:noticia_detalle', pk=publicacion.pk)

    recientes = Publicacion.objects.filter(
        estado=Publicacion.ESTADO_PUBLICADO
    ).exclude(pk=publicacion.pk).order_by('-createdat')[:4]

    comentarios = publicacion.comentarios.filter(
        estado=Comentario.ESTADO_APROBADO
    ).select_related('user').order_by('-createdat')

    categorias = Categoria.objects.all().order_by('nombre')

    return render(request, 'home/noticia.html', {
        'publicacion': publicacion,
        'recientes': recientes,
        'comentarios': comentarios,
        'categorias': categorias,
    })

@operador_required
def crear_publicacion(request):
    categorias = Categoria.objects.all().order_by('nombre')
    if request.method == 'POST':
        publicacion = Publicacion.objects.create(
            titulo=request.POST.get('titulo', '').strip(),
            resumen=request.POST.get('resumen', '').strip(),
            contenido=request.POST.get('contenido', '').strip(),
            categoria_id=request.POST.get('categoria') or None,
            estado=request.POST.get('estado') or Publicacion.ESTADO_BORRADOR,
            autor=request.user,
        )
        portada = request.FILES.get('imagen_portada')
        if portada:
            publicacion.imagen_portada = guardar_archivo(portada, request.user)
            publicacion.save()
        for imagen in request.FILES.getlist('galeria'):
            GaleriaPublicacion.objects.create(
                publicacion=publicacion,
                archivo=guardar_archivo(imagen, request.user)
            )
        messages.success(request, 'Publicación creada correctamente.')
        return redirect('home:crud_noticias')
    return render(request, 'home/crear_publicacion.html', {'categorias': categorias})

@operador_required
def editar_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    categorias = Categoria.objects.all().order_by('nombre')
    if request.method == 'POST':
        publicacion.titulo = request.POST.get('titulo', '').strip()
        publicacion.resumen = request.POST.get('resumen', '').strip()
        publicacion.contenido = request.POST.get('contenido', '').strip()
        publicacion.categoria_id = request.POST.get('categoria') or None
        publicacion.estado = request.POST.get('estado') or Publicacion.ESTADO_BORRADOR
        
        portada = request.FILES.get('imagen_portada')
        if portada:
            publicacion.imagen_portada = guardar_archivo(portada, request.user)
        publicacion.save()

        for imagen in request.FILES.getlist('galeria'):
            GaleriaPublicacion.objects.create(
                publicacion=publicacion,
                archivo=guardar_archivo(imagen, request.user)
            )
        messages.success(request, 'Publicación actualizada correctamente.')
        return redirect('home:crud_noticias')
    return render(request, 'home/crear_publicacion.html', {
        'categorias': categorias,
        'publicacion': publicacion,
    })

@operador_required
def publicar_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    publicacion.estado = Publicacion.ESTADO_PUBLICADO if publicacion.estado != Publicacion.ESTADO_PUBLICADO else Publicacion.ESTADO_BORRADOR
    publicacion.save()
    return redirect('home:crud_noticias')

@operador_required
def eliminar_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    if request.method == 'POST':
        publicacion.delete()
        messages.success(request, 'Publicación eliminada correctamente.')
        return redirect('home:crud_noticias')
```

### Paso 5.- Probar la creación de noticias
Levanta el servidor y entra a la opción de crear publicación completando el título, resumen, contenido, categoría, imagen de portada y galería.

---

# LABORATORIO 12: Index y Comentarios Dinámicos

**Objetivo:** Activar los registros dinámicos en la sección de inicio (index) y la gestión interactiva de comentarios.

---

## Tarea 1: Crear la parte dinámica del index

### Paso 1.- Modificar la vista `categoria` en `canaco/home/views.py`

```python
def categoria(request, pk=None):
    categorias = Categoria.objects.all().order_by('nombre')
    categoria_actual = get_object_or_404(Categoria, pk=pk) if pk else None
    publicaciones = Publicacion.objects.filter(
        estado=Publicacion.ESTADO_PUBLICADO
    ).select_related('categoria', 'autor', 'imagen_portada')

    if categoria_actual:
        publicaciones = publicaciones.filter(categoria=categoria_actual)

    return render(request, 'home/categoria.html', {
        'categorias': categorias,
        'categoria_actual': categoria_actual,
        'publicaciones': publicaciones.order_by('-createdat'),
    })
```

### Paso 2.- Modificar `canaco/home/templates/home/index.html`

```html
{% extends 'partials/base.html' %}
{% load static %}
{% block title %}Inicio{% endblock %}
{% block content %}

{% if slider %}
<section class="home-carousel-section bg-light">
  <div id="homeCarousel" class="carousel slide home-carousel" data-bs-ride="carousel">
    <div class="carousel-indicators">
      {% for noticia in slider %}
        <button type="button" data-bs-target="#homeCarousel" data-bs-slide-to="{{ forloop.counter0 }}" class="{% if forloop.first %}active{% endif %}" aria-current="{% if forloop.first %}true{% endif %}" aria-label="Noticia {{ forloop.counter }}"></button>
      {% endfor %}
    </div>
    <div class="carousel-inner">
      {% for noticia in slider %}
        <div class="carousel-item {% if forloop.first %}active{% endif %}" data-bs-interval="4500">
          <a href="{% url 'home:noticia_detalle' noticia.id %}" class="home-carousel-link">
            {% if noticia.imagen_portada %}
              <img src="{{ noticia.imagen_portada.display_url }}" class="d-block w-100 home-carousel-image" style="height: 400px; object-fit: cover; object-position: center;" alt="{{ noticia.titulo }}">
            {% else %}
              <img src="{% static 'images/hero_1.jpg' %}" class="d-block w-100 home-carousel-image" style="height: 400px; object-fit: cover; object-position: center;" alt="{{ noticia.titulo }}">
            {% endif %}
          </a>
          <div class="carousel-caption home-carousel-caption text-start">
            <span>{{ noticia.createdat|date:"d M Y" }}</span>
            <h2>{{ noticia.titulo }}</h2>
            {% if noticia.resumen %}
              <p>{{ noticia.resumen|truncatewords:20 }}</p>
            {% endif %}
          </div>
        </div>
      {% endfor %}
    </div>
    <button class="carousel-control-prev" type="button" data-bs-target="#homeCarousel" data-bs-slide="prev">
      <span class="carousel-control-prev-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Anterior</span>
    </button>
    <button class="carousel-control-next" type="button" data-bs-target="#homeCarousel" data-bs-slide="next">
      <span class="carousel-control-next-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Siguiente</span>
    </button>
  </div>
</section>
{% endif %}

<section class="section recent-news-section">
  <div class="container">
    <div class="row mb-4 justify-content-center">
      <div class="col-lg-8 text-center">
        <h2 class="posts-entry-title">Noticias recientes</h2>
        <a href="{% url 'home:categoria' %}" class="read-more">Ver todas</a>
      </div>
    </div>
    <div class="row justify-content-center">
      {% for noticia in publicaciones %}
        <div class="col-lg-4 mb-4">
          <div class="post-entry-alt">
            <a href="{% url 'home:noticia_detalle' noticia.id %}" class="img-link">
              {% if noticia.imagen_portada %}
                <img src="{{ noticia.imagen_portada.display_url }}" alt="{{ noticia.titulo }}" class="img-fluid publication-card-image" style="height: 200px; width: 100%; object-fit: cover; object-position: center;">
              {% else %}
                <img src="{% static 'images/img_1_horizontal.jpg' %}" alt="{{ noticia.titulo }}" class="img-fluid publication-card-image" style="height: 200px; width: 100%; object-fit: cover; object-position: center;">
              {% endif %}
            </a>
            <div class="excerpt">
              <h2><a href="{% url 'home:noticia_detalle' noticia.id %}">{{ noticia.titulo }}</a></h2>
              <div class="post-meta align-items-center text-left clearfix">
                <span>{{ noticia.createdat|date:"d M Y" }}</span>
                <span>&nbsp;-&nbsp; {% if noticia.categoria %}{{ noticia.categoria.nombre }}{% else %}Sin categoría{% endif %}</span>
              </div>
              <p>{{ noticia.resumen }}</p>
              <p><a href="{% url 'home:noticia_detalle' noticia.id %}" class="read-more">Saber más</a></p>
              <small>Visitas: {{ noticia.visitas }}</small>
            </div>
          </div>
        </div>
      {% empty %}
        <div class="col-12">
          <p>No hay noticias publicadas todavía.</p>
        </div>
      {% endfor %}
    </div>
  </div>
</section>
{% endblock content %}
```

### Paso 3.- Modificar la vista `index` en `canaco/home/views.py`

```python
def index(request):
    publicaciones = Publicacion.objects.filter(
        estado=Publicacion.ESTADO_PUBLICADO,
    ).select_related('categoria', 'autor', 'imagen_portada').order_by('-createdat')
    
    return render(request, 'home/index.html', {
        'slider': publicaciones[:3],
        'publicaciones': publicaciones[:3],
    })
```

---

## Tarea 2: Configurar la vista categoría en el frontend

### Paso 1.- Modificar `canaco/home/templates/home/categoria.html`

```html
{% extends 'partials/base.html' %}
{% load static %}
{% block title %}Categorías{% endblock %}
{% block content %}
<section class="section">
  <div class="container">
    <div class="row mb-4">
      <div class="col-lg-8">
        <h2 class="posts-entry-title">
          {% if categoria_actual %}Categoría: {{ categoria_actual.nombre }}{% else %}Todas las noticias{% endif %}
        </h2>
      </div>
      <div class="col-lg-4">
        <select class="form-control" onchange="if (this.value) window.location.href=this.value;">
          <option value="{% url 'home:categoria' %}">Todas las categorías</option>
          {% for categoria in categorias %}
            <option value="{% url 'home:categoria_detalle' categoria.id %}" {% if categoria_actual and categoria_actual.id == categoria.id %}selected{% endif %}>
              {{ categoria.nombre }}
            </option>
          {% endfor %}
        </select>
      </div>
    </div>

    {% for noticia in publicaciones %}
      <div class="row mb-5 align-items-center">
        <div class="col-lg-3">
          <a href="{% url 'home:noticia_detalle' noticia.id %}" class="img-link">
            {% if noticia.imagen_portada %}
              <img src="{{ noticia.imagen_portada.display_url }}" alt="{{ noticia.titulo }}" class="img-fluid category-post-image">
            {% else %}
              <img src="{% static 'images/img_1_horizontal.jpg' %}" alt="{{ noticia.titulo }}" class="img-fluid category-post-image">
            {% endif %}
          </a>
        </div>
        <div class="col-lg-8">
          <span class="date">{{ noticia.createdat|date:"d M Y" }} &bullet; {% if noticia.categoria %}{{ noticia.categoria.nombre }}{% else %}Sin categoría{% endif %}</span>
          <h2><a href="{% url 'home:noticia_detalle' noticia.id %}">{{ noticia.titulo }}</a></h2>
          <p>{{ noticia.resumen }}</p>
          <p><a href="{% url 'home:noticia_detalle' noticia.id %}" class="btn btn-sm btn-outline-primary">Leer más</a></p>
        </div>
      </div>
    {% empty %}
      <p>No hay noticias para esta categoría.</p>
    {% endfor %}
  </div>
</section>
{% endblock content %}
```

---

## Tarea 3: Flujo de prueba para comentarios

1. **Crear usuario estándar:** Registrar un usuario nuevo (diferente a `superadmin`).
2. **Navegar a la noticia:** Ingresar al detalle de una noticia y presionar en **"INICIA SESIÓN PARA COMENTAR"** (o escribir el comentario si ya estás autenticado).
3. **Enviar comentario:** Redactar un comentario y presionar **"AGREGAR COMENTARIO"**. Quedará con estado pendiente.
4. **Modo administrador:** Cerrar sesión, iniciar como `superadmin` y abrir el panel `/crud_comentarios`.
5. **Aprobar:** Dar clic en el botón **APROBAR**.
6. **Verificación:** Regresar a la noticia en la vista pública para constatar que el comentario ahora es visible.

---

# LABORATORIO 13: Context Processors en Django

**Objetivo:** Configurar un Context Processor para inyectar globalmente datos de categorías y noticias recientes en todas las plantillas.

---

## Tarea 1: Modificar el archivo `footer.html`

Modifica el archivo `canaco/home/templates/partials/footer.html`:

```html
{% load static %}
<footer class="site-footer">
  <div class="container">
    <div class="row">
      <!-- Columna 1: Acerca de -->
      <div class="col-lg-4">
        <div class="widget">
          <h3 class="mb-4">Acerca de</h3>
          <p>Muy muy lejos, detrás de las montañas de palabras, lejos de los países Vokalia y Consonantia, viven los textos ciegos.</p>
        </div>
        <div class="widget">
          <h3>Redes Sociales</h3>
          <ul class="list-unstyled social">
            <li><a href="#"><span class="icon-instagram"></span></a></li>
            <li><a href="#"><span class="icon-twitter"></span></a></li>
            <li><a href="#"><span class="icon-facebook"></span></a></li>
            <li><a href="#"><span class="icon-linkedin"></span></a></li>
            <li><a href="#"><span class="icon-pinterest"></span></a></li>
            <li><a href="#"><span class="icon-dribbble"></span></a></li>
          </ul>
        </div>
      </div>

      <!-- Columna 2: Links de Empresa -->
      <div class="col-lg-4 ps-lg-5">
        <div class="widget">
          <h3 class="mb-4">Empresa</h3>
          <ul class="list-unstyled float-start links">
            <li><a href="#">Sobre nosotros</a></li>
            <li><a href="#">Servicios</a></li>
            <li><a href="#">Visión</a></li>
            <li><a href="#">Misión</a></li>
            <li><a href="#">Términos</a></li>
            <li><a href="#">Privacidad</a></li>
          </ul>
          <ul class="list-unstyled float-start links">
            <li><a href="#">Socios</a></li>
            <li><a href="#">Negocios</a></li>
            <li><a href="#">Empleos</a></li>
            <li><a href="#">Blog</a></li>
            <li><a href="#">Preguntas Frecuentes</a></li>
            <li><a href="#">Creativos</a></li>
          </ul>
        </div>
      </div>

      <!-- Columna 3: Entradas Recientes (Globales) -->
      <div class="col-lg-4">
        <div class="widget">
          <h3 class="mb-4">Entradas Recientes</h3>
          <div class="post-entry-footer">
            <ul>
              {% for noticia in global_recientes %}
                <li>
                  <a href="{% url 'home:noticia_detalle' noticia.id %}">
                    {% if noticia.imagen_portada %}
                      <img src="{{ noticia.imagen_portada.display_url }}" alt="{{ noticia.titulo }}" class="me-4 rounded" style="width: 70px; height: 70px; object-fit: cover;">
                    {% else %}
                      <img src="{% static 'images/img_1_sq.jpg' %}" alt="{{ noticia.titulo }}" class="me-4 rounded" style="width: 70px; height: 70px; object-fit: cover;">
                    {% endif %}
                    <div class="text">
                      <h4>{{ noticia.titulo }}</h4>
                      <div class="post-meta">
                        <span class="mr-2">{{ noticia.createdat|date:"d M, Y" }}</span>
                      </div>
                    </div>
                  </a>
                </li>
              {% empty %}
                <li><span class="text-white-50">No hay noticias recientes.</span></li>
              {% endfor %}
            </ul>
          </div>
        </div>
      </div>

    </div>

    <!-- Copyright -->
    <div class="row mt-5">
      <div class="col-12 text-center">
        <p>Copyright &copy; <script>document.write(new Date().getFullYear());</script>. Todos los derechos reservados. &mdash; Diseñado con amor por <a href="https://untree.co">Untree.co</a> Distribuido por <a href="https://themewagon.com">ThemeWagon</a></p>
      </div>
    </div>
  </div>
</footer>
```

---

## Tarea 2: Crear el archivo `context_processors.py`

Crea un archivo llamado `context_processors.py` dentro de la carpeta de la app `canaco/home/`:

```python
from home.models import Categoria, Publicacion

def global_categorias(request):
    return {
        'global_categorias': Categoria.objects.all().order_by('nombre'),
        'global_recientes': Publicacion.objects.filter(
            estado=Publicacion.ESTADO_PUBLICADO
        ).order_by('-createdat')[:3]
    }
```

---

## Tarea 3: Registrar el Context Processor en `settings.py`

Abre el archivo de configuración global `canaco/settings.py` y agrega la ruta del nuevo Context Processor dentro del bloque `TEMPLATES -> OPTIONS -> context_processors`:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'home.context_processors.global_categorias',
            ],
        },
    },
]
```

---

## Verificación Final
1. Reinicia el servidor web (`python manage.py runserver`).
2. Revisa cualquier página del sitio; la sección **Entradas Recientes** del pie de página (`footer`) debe renderizar automáticamente las últimas 3 publicaciones activas sin necesidad de pasarlas explícitamente desde cada vista.