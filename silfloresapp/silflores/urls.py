import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('products/', include('products.urls')),
    path('user/', include('users.urls')),
    path('cart/', include('cart.urls')),
    path('getSoldProducts/', views.getSoldProducts, name="getSoldProducts"),
    path('getNewProducts/', views.getNewProducts, name="getNewProducts"),
    path('meme', views.meme, name='meme'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=os.path.join(settings.BASE_DIR, 'static')
    )
