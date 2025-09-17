
from pathlib import Path
from decouple import config
from dj_database_url import parse
import cloudinary_storage

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('DJANGO_SECRET_KEY',cast=str,default=None)
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DJANGO_DEBUG', cast=bool, default=False)


CSRF_TRUSTED_ORIGINS = [
    'https://*.railway.app',
]

if DEBUG:
    ALLOWED_HOSTS = [
        '*',  # Tüm hostlar için
        'localhost',  # Yerel geliştirme için
    ]
else:
    ALLOWED_HOSTS = [
        '*',  # Railway ve tüm subdomain'ler için
        '.railway.app',  # Railway domainleri için
    ]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'products',
    'admin_side',
    'orders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = 'product_catalog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'product_catalog.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Railway/Production veritabanı konfigürasyonu
# # Railway için özel işleme
try:
    DATABASE_URL = config('DATABASE_URL', default='')
        
    # Database URL'nin string olduğundan emin olalım
    if isinstance(DATABASE_URL, bytes):
        DATABASE_URL = DATABASE_URL.decode('utf-8')
    
    # b'' formatını temizle
    if DATABASE_URL and DATABASE_URL.startswith("b'") and DATABASE_URL.endswith("'"):
        DATABASE_URL = DATABASE_URL[2:-1]
    
    # URL'de sadece '://' varsa ve başında bir scheme yoksa hata ver
    if DATABASE_URL and DATABASE_URL.startswith('://'):
        raise ValueError(f"Invalid DATABASE_URL format: {DATABASE_URL}")
    
    # Geçerli bir DATABASE_URL varsa kullan
    if DATABASE_URL:
        DATABASES = {
            'default': parse(DATABASE_URL, conn_max_age=600, conn_health_checks=True)
        }
   
except Exception as e:
    print(f"Veritabanı bağlantı hatası: {e}")
    # Fallback olarak SQLite kullan
   

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATIC_URL = 'static/'

# production static files
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (Uploads)

# Cloudinary için varsayılan değerleri belirle, bu sayede ortam değişkenleri yoksa bile çalışacak
CLOUDINARY_CLOUD_NAME = config('CLOUDINARY_CLOUD_NAME', default=None)
CLOUDINARY_API_KEY = config('CLOUDINARY_API_KEY', default=None)
CLOUDINARY_API_SECRET = config('CLOUDINARY_API_SECRET', default=None)

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': CLOUDINARY_CLOUD_NAME,
    'API_KEY': CLOUDINARY_API_KEY,
    'API_SECRET': CLOUDINARY_API_SECRET
}

MEDIA_URL = '/django_media/'  # or any prefix you choose
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'