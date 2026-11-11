import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url
BASE_DIR=Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR/".env")
SECRET_KEY=os.getenv("SECRET_KEY","unsafe-dev-key-change-me")
DEBUG=os.getenv("DEBUG","True").lower()=="true"
ALLOWED_HOSTS=[x.strip() for x in os.getenv("ALLOWED_HOSTS","127.0.0.1,localhost").split(",") if x.strip()]
if os.getenv("RENDER_EXTERNAL_HOSTNAME"):
    ALLOWED_HOSTS.append(os.getenv("RENDER_EXTERNAL_HOSTNAME"))
INSTALLED_APPS=["django.contrib.admin","django.contrib.auth","django.contrib.contenttypes","django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles","rest_framework","rest_framework.authtoken","corsheaders","accounts","students","companies","jobs","applications"]
MIDDLEWARE=["django.middleware.security.SecurityMiddleware","whitenoise.middleware.WhiteNoiseMiddleware","corsheaders.middleware.CorsMiddleware","django.contrib.sessions.middleware.SessionMiddleware","django.middleware.common.CommonMiddleware","django.middleware.csrf.CsrfViewMiddleware","django.contrib.auth.middleware.AuthenticationMiddleware","django.contrib.messages.middleware.MessageMiddleware","django.middleware.clickjacking.XFrameOptionsMiddleware"]
ROOT_URLCONF="config.urls"
TEMPLATES=[{"BACKEND":"django.template.backends.django.DjangoTemplates","DIRS":[],"APP_DIRS":True,"OPTIONS":{"context_processors":["django.template.context_processors.debug","django.template.context_processors.request","django.contrib.auth.context_processors.auth","django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION="config.wsgi.application"
if os.getenv("DATABASE_URL"):
    DATABASES={"default":dj_database_url.parse(os.getenv("DATABASE_URL"),conn_max_age=600,ssl_require=not DEBUG)}
else:
    DATABASES={"default":{"ENGINE":"django.db.backends.sqlite3","NAME":BASE_DIR/"db.sqlite3"}}
AUTH_PASSWORD_VALIDATORS=[{"NAME":"django.contrib.auth.password_validation.MinimumLengthValidator"}]
LANGUAGE_CODE="en-us"; TIME_ZONE="Asia/Kolkata"; USE_I18N=True; USE_TZ=True
STATIC_URL="static/"; STATIC_ROOT=BASE_DIR/"staticfiles"
MEDIA_URL="/media/"; MEDIA_ROOT=BASE_DIR/"media"
STORAGES={"default":{"BACKEND":"django.core.files.storage.FileSystemStorage"},"staticfiles":{"BACKEND":"whitenoise.storage.CompressedManifestStaticFilesStorage"}}
DEFAULT_AUTO_FIELD="django.db.models.BigAutoField"
CORS_ALLOWED_ORIGINS=[x.strip() for x in os.getenv("CORS_ALLOWED_ORIGINS","http://127.0.0.1:5500,http://localhost:5500").split(",") if x.strip()]
REST_FRAMEWORK={"DEFAULT_AUTHENTICATION_CLASSES":["rest_framework.authentication.TokenAuthentication"],"DEFAULT_PERMISSION_CLASSES":["rest_framework.permissions.IsAuthenticated"]}

CSRF_TRUSTED_ORIGINS=[x.strip() for x in os.getenv("CSRF_TRUSTED_ORIGINS","").split(",") if x.strip()]
