# Glow Beauty

Catálogo web para Glow Beauty, construido con Django. Incluye catálogo público, filtros por categoría, vista individual de producto, cuentas de usuario, favoritos y panel Jazzmin en `/admin/`.

La identidad visual toma el logo de `img/Logo.jpeg`: rosa empolvado y claro, cereza, blanco cálido y acentos vino.

## Instalación local

Desde `C:\Users\Migue\Documents\Prpoyecto_Ana`, en PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Abre `http://127.0.0.1:8000/` para ver el catálogo, crear una cuenta y guardar favoritos. El superusuario creado con `createsuperuser` puede usar **Ingresar** con sus credenciales y después acceder a `/admin/` para administrar categorías y productos. Las cuentas creadas desde el catálogo son cuentas normales; no obtienen permisos de administración.

Configura las variables de `.env` en la terminal o desde tu editor. El proyecto funciona localmente sin `DATABASE_URL`, usando SQLite (`db.sqlite3`).

## PostgreSQL

Cuando exista `DATABASE_URL`, Django usa PostgreSQL automáticamente. Ejemplo:

```text
DATABASE_URL=postgresql://usuario:contraseña@host:5432/glowbeauty
```

Antes de producción, define también:

```text
SECRET_KEY=una-clave-larga-unica-y-secreta
DEBUG=False
ALLOWED_HOSTS=tudominio.com
```

En Render no hace falta añadir manualmente el host generado: `RENDER_EXTERNAL_HOSTNAME` se incorpora automáticamente a `ALLOWED_HOSTS`.

## Despliegue en Render

1. Sube este proyecto a un repositorio Git y conéctalo a Render.
2. Crea un nuevo **Blueprint** y selecciona el repositorio; Render leerá `render.yaml`.
3. Confirma la creación del servicio web y de PostgreSQL. `DATABASE_URL` se conecta automáticamente desde la base creada por el Blueprint.
4. Render ejecutará `bash build.sh`, que instala dependencias, recopila estáticos y ejecuta migraciones.
5. En el panel de Render, crea un superusuario desde el Shell:

   ```bash
   python manage.py createsuperuser
   ```

6. Visita `https://tu-servicio.onrender.com/admin/` e inicia sesión para crear categorías y productos.

## Imágenes en producción

`MEDIA_ROOT` está configurado para desarrollo local y permite subir imágenes desde el panel de Django. El sistema de archivos efímero de Render no conserva las imágenes subidas tras un redeploy o reinicio. Para producción configura Cloudinary, Amazon S3, Cloudflare R2, u otro almacenamiento persistente (o un disco persistente compatible con tu plan).

## Comprobaciones

```powershell
python manage.py check
python manage.py migrate
python manage.py test
```

## Estructura principal

- `catalogo/models.py`: categorías y productos.
- `catalogo/admin.py`: configuración del panel de administración.
- `catalogo/templates/`: catálogo, tarjetas y detalle.
- `catalogo/static/catalogo/css/styles.css`: diseño responsive.
- `glow_beauty/settings.py`: base de datos, archivos estáticos, media y seguridad.
