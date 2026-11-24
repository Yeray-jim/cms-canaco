# CMS Canaco — Blog de noticias con Django

Proyecto de un sitio de noticias desarrollado para los laboratorios 11, 12 y 13 de la materia de Desarrollo Web (TecNM). Incluye un frontend público, un panel de administración para operadores y despliegue en Azure App Service.

## Características

- **CRUD de noticias**: crear, editar, publicar/ocultar y eliminar publicaciones, con portada y galería de imágenes.
- **CRUD de categorías**: agregar, editar y eliminar categorías.
- **Gestión de comentarios**: los visitantes envían comentarios que quedan pendientes hasta que un operador los aprueba o bloquea.
- **Vistas públicas**: index con slider y noticias recientes, listado filtrable por categoría y detalle de noticia con galería, visitas y comentarios aprobados.
- **Panel de operadores**: perfiles, usuarios, cambio de contraseña y administración de noticias/comentarios/categorías (acceso restringido a `is_staff` o `is_superuser`).
- **Context processors**: categorías y noticias recientes inyectadas globalmente en todas las plantillas (footer y header).
- **Interfaz**: tema Untree/Bootstrap personalizado (paleta "editorial clásico": azul marino con acento rojo), botones redondeados y estados de foco accesibles.

## Stack técnico

- Python 3.13, Django 6.1.1
- MySQL/MariaDB (local: MariaDB en Docker; producción: Azure Database for MySQL Flexible Server)
- PyMySQL + django-mysql, Gunicorn, WhiteNoise
- Bootstrap 5 + CSS propio (`static/css/custom.css`)

## Estructura

```
canaco/                     # proyecto Django (manage.py está aquí)
├── canaco/                 # paquete del proyecto (settings.py, urls.py, wsgi.py)
├── home/                   # aplicación principal
│   ├── models.py           # Categoria, Archivo, Perfil, Publicacion, GaleriaPublicacion, Comentario
│   ├── views.py            # vistas públicas y CRUD
│   ├── urls.py             # rutas
│   ├── context_processors.py
│   ├── signals.py          # crea un Perfil al crear un User
│   ├── migrations/
│   ├── static/             # CSS/JS/imágenes (en canaco/static)
│   └── templates/          # plantillas (home/ y partials/)
├── docker/compose.yaml     # MariaDB local
├── requirements.txt
└── startup.sh              # comando de arranque en Azure
requirements.txt            # mismo listado, en la raíz del repo
promp.md                    # especificación de los laboratorios 11-13
```

## Ejecutar en local

1. Levantar la base de datos:

   ```bash
   docker compose -f canaco/docker/compose.yaml up -d
   ```

2. Crear/activar el entorno virtual e instalar dependencias:

   ```bash
   python3 -m venv canaco.venv
   source canaco.venv/bin/activate
   pip install -r requirements.txt
   ```

3. Aplicar migraciones y arrancar:

   ```bash
   cd canaco
   python manage.py migrate
   python manage.py runserver
   ```

4. Crear un administrador:

   ```bash
   python manage.py createsuperuser
   # o: python manage.py changepassword <usuario>
   ```

El sitio queda en `http://127.0.0.1:8000/`.

## Despliegue en Azure

El repo tiene un flujo de **GitHub Actions** (`.github/workflows/azure-webapps-python.yml`) que despliega automáticamente la carpeta `canaco/` en un App Service llamado `canaco-noticias` al hacer push a `main`.

1. Crear **Azure Database for MySQL Flexible Server** (MySQL 8.0, Burstable B1ms) y la base de datos `canaco_db`. En *Networking*, activar *Allow access from Azure services*.
2. Crear **App Service** en Linux con **Python 3.13** (plan B1 recomendado; el crédito Azure for Students lo cubre).
3. En *Deployment Center* → GitHub → `Yeray-jim/cms-canaco`, rama `main`, GitHub Actions. Guardar el *publish profile* como secreto `AZURE_WEBAPP_PUBLISH_PROFILE`.
4. Configurar los *App settings*:

   | Variable | Ejemplo |
   |---|---|
   | `DB_HOST` | `servidor.mysql.database.azure.com` |
   | `DB_NAME` | `canaco_db` |
   | `DB_USER` | `canacoadmin` |
   | `DB_PASSWORD` | `<contraseña>` |
   | `DJANGO_SECRET_KEY` | `<clave larga y aleatoria>` |
   | `DJANGO_DEBUG` | `False` |
   | `DJANGO_SUPERUSER_USERNAME` | `admin` |
   | `DJANGO_SUPERUSER_PASSWORD` | `<contraseña>` |
   | `SCM_DO_BUILD_DURING_DEPLOYMENT` | `1` |

5. En *Startup Command*: `bash startup.sh`. Este script aplica migraciones, recolecta estáticos, crea el superusuario si no existe y lanza Gunicorn.
6. Reiniciar el servicio. La URL pública será `https://canaco-noticias.azurewebsites.net`.

Si cambias el nombre del App Service, actualiza `app-name` en el workflow. Los errores se revisan en *Log stream* del App Service.

## Verificación

```bash
cd canaco
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py collectstatic --noinput --dry-run
```
