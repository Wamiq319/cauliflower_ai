from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Live reload (optional — remove if not used)
    path('__reload__/', include('django_browser_reload.urls')),

    # Public pages (landing, login, etc.)
    path('', include('apps.pages.urls')),

    path('accounts/', include('apps.accounts.urls')),
     path('doctors/', include('apps.doctors.urls')),


]
