from pathlib import Path
import os

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-cambia-esta-clave-en-produccion")
DEBUG = os.environ.get("DEBUG", "True").lower() == "true"

hosts = os.environ.get("ALLOWED_HOSTS", "").split(",")
render_host = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "")
ALLOWED_HOSTS = [host.strip() for host in hosts if host.strip()]
if render_host:
    ALLOWED_HOSTS.append(render_host)
if DEBUG and not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes",
    "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles",
    "catalogo",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "glow_beauty.urls"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.request", "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]
WSGI_APPLICATION = "glow_beauty.wsgi.application"

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}", conn_max_age=600
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
LANGUAGE_CODE = "es-co"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "catalogo:iniciar_sesion"
LOGIN_REDIRECT_URL = "catalogo:inicio"
LOGOUT_REDIRECT_URL = "catalogo:inicio"

JAZZMIN_SETTINGS = {
    "site_title": "Glow Beauty Admin",
    "site_header": "Glow Beauty",
    "site_brand": "Glow Beauty",
    "welcome_sign": "Administración Glow Beauty",
    "copyright": "Glow Beauty",
    "site_logo": "catalogo/img/Logo.jpeg",
    "login_logo": "catalogo/img/Logo.jpeg",
    "site_icon": "catalogo/img/Logo.jpeg",
    "topmenu_links": [{"name": "Ver catálogo", "url": "/", "new_window": False}],
    "show_ui_builder": False,
}
JAZZMIN_UI_TWEAKS = {
    "theme": "flatly", "navbar": "navbar-pink", "accent": "accent-pink",
    "sidebar": "sidebar-dark-pink", "brand_colour": "navbar-pink",
}
