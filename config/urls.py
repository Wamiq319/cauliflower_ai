from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Live reload (optional — remove if not used)
    path('__reload__/', include('django_browser_reload.urls')),

    # Public pages (landing, login, etc.)
    path('', include('apps.pages.urls')),

    path('accounts/', include('apps.accounts.urls')),
    path('doctors/', include('apps.doctors.urls')),
    path('admin-panel/', include('apps.admin_panel.urls')),
    path('farmers/', include('apps.farmers.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
